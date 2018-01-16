import datajoint as dj

schema = dj.schema('boazmohar_lab', locals())


@schema
class Person(dj.Manual):
    definition = """
    username : varchar(12) 
    ----
    fullname : varchar(60)
    """
    contents = [('boazmohar', 'Boaz Mohar')]


@schema
class Rig(dj.Manual):
    definition = """
    rig  : varchar(16)
    ---
    room            : varchar(20) # example 2w.342
    rig_description : varchar(1024) 
    """


@schema
class AnimalSource(dj.Lookup):
    definition = """
    animal_source       : varchar(30)
    """
    contents = zip(['Jackson Labs', 'Charles River', 'MMRRC', 'Taconic', 'Other'])


@schema
class Species(dj.Lookup):
    definition = """
    species   : varchar(60)
    """
    contents = zip(['mus musculus'])


@schema
class Strain(dj.Manual):
    definition = """
    # Mouse strain
    strain : varchar(30) # mouse strain
    """


@schema
class GeneModification(dj.Manual):
    definition = """
    gene_modification   : varchar(60)
    """


@schema
class Subject(dj.Manual):
    definition = """
    subject_id          : int                     # institution animal ID
    ---
    cage_number         : int
    -> Species 
    date_of_birth       : date
    date_of_surgery     : date
    sex                 : enum('M','F','Unknown')
    ->  [nullable]   AnimalSource
    """

    class GeneModification(dj.Part):
        definition = """
        # Subject gene modifications
        -> Subject
        -> GeneModification
        """

    class Strain(dj.Part):
        definition = """
        -> Subject
        -> Strain
        """


@schema
class WaterRestriction(dj.Manual):
    definition = """
    -> Subject
    water_restriction_number    : varchar(16)   # WR number
    ---
    wr_start_date               : date
    wr_start_weight             : Decimal(6,3)
    """


@schema
class VirusSource(dj.Lookup):
    definition = """
    virus_source   : varchar(60)
    """
    contents = zip(['Janelia', 'UPenn', 'Addgene', 'UNC', 'Other'])


@schema
class Serotype(dj.Manual):
    definition = """
    serotype   : varchar(60)
    """


@schema
class Virus(dj.Manual):
    definition = """
    virus_id : int unsigned
    ---
    -> VirusSource 
    -> Serotype
    -> Person
    virus_name      : varchar(255)
    titer           : Decimal(20,1)
    order_date      : date
    remarks         : varchar(256)
    """


@schema
class VirusReference(dj.Lookup):
    definition = """
    virus_reference   : varchar(60)
    """
    contents = zip(['Bregma', 'lambda'])


@schema
class Surgery(dj.Manual):
    definition = """
    -> Subject
    surgery_id          : int                     # surgery number
    ---
    -> Person
    start_time          : datetime # start time
    end_time            : datetime # end time
    description         : varchar(256)
    """

    class VirusInjection(dj.Part):
        definition = """
        # Virus injections
        -> Surgery
        injection_id : int
        ---
        -> Virus
        -> VirusReference
        ml_location     : Decimal(8,3) # um from ref left is positive
        ap_location     : Decimal(8,3) # um from ref anterior is positive
        dv_location     : Decimal(8,3) # um from dura dorsal is positive
        location_name   : varchar(60)
        volume          : Decimal(10,3) # in nl
        dilution        : Decimal (10, 2) # 1 to how much
        """

    class Procedure(dj.Part):
        definition = """
        # Other things you did to the animal
        -> Surgery
        procedure_id : int
        ---
        description     : varchar(60)
        ml_location     : Decimal(8,3) # um from ref left is positive
        ap_location     : Decimal(8,3) # um from ref anterior is positive
        dv_location     : Decimal(8,3) # um from dura dorsal is positive
        location_name   : varchar(60)
        """


