import MateriaClass
from trello import TrelloClient
import connectSQLite
import configuration


def create(subjCod, task_title):
    config = configuration.load_config_file('polical.yaml')
    client = TrelloClient(
        api_key=config['api_key'],
        api_secret=config['api_secret'],
        token=config['oauth_token'],
        token_secret=config['oauth_token_secret'],
    )
    subjectsBoard = client.get_board(config['board_id'])
    if(connectSQLite.check_no_subjectID(subjCod) == 1):
        subject_name = connectSQLite.getSubjectName(subjCod)
        print(subject_name)
        id = ""
        Add_Subject_To_Trello_List(subjectsBoard, subject_name, subjCod)
    elif(connectSQLite.getSubjectName(subjCod) == ""):
        print("\n Nombre de materia no encontrado, titulo de la tarea:"+ task_title)
        subject_name = input("Por favor agregue el nombre de la materia:")
        response = "N"
        while response == "N" or response == "n":
            print("¿El nombre de la materia " + subject_name+" es correcto?")
            response = input("¿Guardar? S/N:")
        subject = MateriaClass.Materia(subject_name, subjCod)
        sql = connectSQLite.saveSubjects(subject)
        Add_Subject_To_Trello_List(subjectsBoard, subject_name, subjCod)


def Add_Subject_To_Trello_List(subjectsBoard, subject_name, subjCod):
    for x in subjectsBoard.list_lists():
        if x.name == subject_name:
            id = x.id
    if id == "":
        subjectsBoard.add_list(subject_name)
        for x in subjectsBoard.list_lists():
            if x.name == subject_name:
                id = x.id
    subject = MateriaClass.Materia(subject_name, subjCod, id)
    print(subject.print())
    sql = connectSQLite.saveSubjectID(subject)
    for row in sql.fetchall():
        print(row)
    sql = connectSQLite.getdb().close()
