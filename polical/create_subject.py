from polical import MateriaClass
from trello import TrelloClient
from polical import connectSQLite
import logging
from polical import configuration
logging.basicConfig(filename=configuration.get_file_location('Running.log'),level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def create(subjCod, task_title, user_dict):
    # config = configuration.load_config_file('polical.yaml')
    client = TrelloClient(
        api_key=user_dict['api_key'],
        api_secret=user_dict['api_secret'],
        token=user_dict['oauth_token'],
        token_secret=user_dict['oauth_token_secret'],
    )
    subjectsBoard = client.get_board(user_dict['board_id'])
    if(connectSQLite.check_no_subjectID(subjCod) == 1):
        subject_name = connectSQLite.getSubjectName(subjCod)
        logging.info(subject_name)
        print(subject_name)
        id = ""
        Add_Subject_To_Trello_List(subjectsBoard, subject_name, subjCod)
    elif(connectSQLite.getSubjectName(subjCod) == ""):
        logging.info(
            "Nombre de materia no encontrado, titulo de la tarea:"+ str(task_title))
        print("\n Nombre de materia no encontrado, titulo de la tarea:"+ task_title)
        logging.info("Por favor agregue el nombre de la materia:")
        subject_name = input("Por favor agregue el nombre de la materia:")
        logging.info(subject_name)
        response = "N"
        while response == "N" or response == "n":
            logging.info("¿El nombre de la materia " + subject_name +" es correcto?")
            print("¿El nombre de la materia " + subject_name +" es correcto?")
            logging.info("¿Guardar? S/N:")
            response = input("¿Guardar? S/N:")
            logging.info(response)
        subject = MateriaClass.Materia(subject_name, subjCod)
        connectSQLite.saveSubjects(subject)
        Add_Subject_To_Trello_List(subjectsBoard, subject_name, subjCod)


def Add_Subject_To_Trello_List(subjectsBoard, subject_name, subjCod):
    id = ""
    for x in subjectsBoard.list_lists():
        if x.name == subject_name:
            id = x.id
    if id == "":
        subjectsBoard.add_list(subject_name)
        for x in subjectsBoard.list_lists():
            if x.name == subject_name:
                id = x.id
    subject = MateriaClass.Materia(subject_name, subjCod, id)
    logging.info(subject.print())
    sql = connectSQLite.saveSubjectID(subject)
    for row in sql.fetchall():
        logging.info("fila: " + str(row))
    sql = connectSQLite.getdb().close()
