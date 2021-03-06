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
class Tracing(dj.Manual):
    definition = """
    -> FOV
    tracing_name            : varchar(32) # name of reconstruction swc
    ---
    tracing_type = 'Cell'   : enum('Cell', 'Cell bodies', 'Other')
    comments                : varchar(1024)     # tuning, other remarks
    """


@schema
class SessionTypes(dj.Lookup):
    definition = """
    # Session types
    session_type : varchar(30)             # session type
    ---    
    """

    class Files(dj.Part):
        definition = """
        # required files
        -> SessionTypes
        filename : varchar(256)
        """


@schema
class Session(dj.Manual):
    definition = """
    -> FOV
    session_id                  : smallint unsigned # running session id
    ---
    -> lab.Person = 'boazmohar'
    -> lab.Rig = 'spine_2p'
    -> [nullable] Tracing
    date = CURRENT_TIMESTAMP    : timestamp         # start date and time
    run = 1                     : int unsigned      # run number
    excitation_wavelength = 960 : int               # in nm
    power                       : decimal(6,3)      # in percent
    anesthesia = 'None'         : enum('None','ISO')
    pitch = 0                   : decimal(6,3)
    roll = 0                    : decimal(6,3)
    comments = "None"           : varchar(256)
    """

    class SessionTypes(dj.Part):
        definition = """
        # Session types
        -> Session
        -> SessionTypes
        """


@schema
class Registration(dj.Manual):
    definition = """
    registration_id : smallint
    """

    class Sessions(dj.Part):
        definition = """
        # Sessions to register together
        -> Registration
        -> Session
        """


@schema
class Step1(dj.Computed):
    definition = """
    -> Registration
    """

    def make(self, key, sc):
        print(key)
        print(sc.defaultParallelism)


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