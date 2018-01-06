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
    rig  : varchar(8)
    ---
    rig_description : varchar(1024) 
    """
    contents = [('Spine2P', '3D resonant high NA 2P microscope for dendrite and spine imaging')]
