import MateriaClass
import TareaClass
import csv
from trello import TrelloClient
import connectSQLite
import configuration
#f = open("calendar.csv","r")
def create(subjCod):
    config = configuration.load_config_file('polical.yaml')
    client = TrelloClient(
        api_key=config['api_key'],
        api_secret=config['api_secret'],
        token=config['oauth_token'],
        token_secret=config['oauth_token_secret'],
    )
    member_id=config['owner_id']
    subjectsBoard = client.get_board(config['board_id'])
    if(connectSQLite.check_subject_existence(subjCod) == 0):
        subject_name = connectSQLite.getSubjectName(subjCod)
        id = ""
        for x in subjectsBoard.list_lists():
            if x.name == subject_name:
                id = x.id
        if id == "":
            subjectsBoard.add_list(subject_name)
            for x in subjectsBoard.list_lists():
                if x.name == subject_name:
                    id = x.id
        subject = MateriaClass.Materia(subject_name,subjCod,id)
        print(subject.print())
        sql = connectSQLite.saveSubjectID(subject)
        for row in sql.fetchall():
            print(row)
        sql = connectSQLite.getdb().close()
