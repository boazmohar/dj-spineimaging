import datajoint as dj
import animal
import lab

schema = dj.schema('boazmohar_experiment', locals())


@schema
class Task(dj.Lookup):
    definition = """
    # Type of tasks
    task            : varchar(12)                  # task type
    ----
    task_description : varchar(4000)
    """
    contents = [
         ('audio delay', 'auditory delayed response task (2AFC)'),
         ('audio mem', 'auditory working memory task'),
         ('s1 stim', 'S1 photostimulation task (2AFC)'),
         ('s1 delay', 'Somatosensory delayed response task (2AFC)')]


@schema
class Session(dj.Manual):
    definition = """
    -> animal.Subject
    session : smallint 
    ---
    session_date  : date
    -> lab.Person
    -> lab.Rig
    """

    class Trial(dj.Part):
        definition = """
        -> Session
        trial   : smallint
        ---
        start_time : decimal(9,3)  # (s)
        end_time : decimal(9,3)  # (s)
        """
