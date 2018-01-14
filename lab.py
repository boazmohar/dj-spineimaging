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
class Rig(dj.Lookup):
    definition = """
    rig  : varchar(16)
    ---
    room            : varchar(20) # example 2w.342
    rig_description : varchar(1024) 
    """
    contents = [('Spine2P', '2c.382', '3D resonant high NA 2P microscope for dendrite and spine imaging')]


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
class Strain(dj.Lookup):
    definition = """
    # Mouse strain
    strain : varchar(30) # mouse strain
    """
    contents = zip(['Syt17 (NO14)', 'Chrna2 OE25', 'wt'])


@schema
class GeneModification(dj.Lookup):
    definition = """
    gene_modification   : varchar(60)
    """
    contents = zip(['Syt17-cre', 'ACTB-tTa', 'Chrna2-cre', 'CamK2a-tTA', 'TITL-GCaMP6f'])


@schema
class Subject(dj.Manual):
    definition = """
    subject_id          : int                     # institution animal ID
    ---
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
    contents = zip(['Janelia', 'UPenn', 'Addgene', 'UNC'])


@schema
class Virus(dj.Lookup):
    definition = """
    virus_id : int unsigned
    ---
    -> VirusSource 
    virus_name      : varchar(64)
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
    date_of_surgery     : date
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
