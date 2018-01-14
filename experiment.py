import datajoint as dj
import lab

schema = dj.schema('boazmohar_experiment', locals())


@schema
class FOV(dj.Manual):
    definition = """
    -> lab.Subject
    fov_id : smallint #
    ---
    stack_date  : date          # when it was imaged for reference
    description : varchar(128)  # location in the craniotomy
    """


@schema
class SessionTypes(dj.Lookup):
    definition = """
    # Session types
    session_type              : varchar(30)             # session type
    """
    contents = zip(['Stacks', 'MROI-SP', 'MROI-Manual', 'Spines', 'Cell-Body', 'Vision', 'Pole'])


@schema
class Session(dj.Manual):
    definition = """
    -> FOV
    run : smallint 
    ---
    date        : date
    -> lab.Person
    -> lab.Rig
    """

    class SessionTypes(dj.Part):
        definition = """
        # Session types
        -> Session
        -> SessionTypes
        """


@schema
class Trial(dj.Imported):
    definition = """
    -> Session
    trial   : smallint
    ---
    filename : varchar(256)
    timepoints : int unsigned
    start_frame : int unsigned
    end_frame : int unsigned
    """