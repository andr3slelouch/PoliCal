from trello import TrelloClient
from trello.member import Member
import connectSQLite
import create_subject
import configuration
from datetime import datetime, timedelta
config = configuration.load_config_file('polical.yaml')
client = TrelloClient(
    api_key=config['api_key'],
    api_secret=config['api_secret'],
    token=config['oauth_token'],
    token_secret=config['oauth_token_secret'],
)
member_id=config['owner_id']
def SendTaskToTrello():
    boards = client.list_boards()
    subjectsBoard = client.get_board(config['board_id'])
    tasks = connectSQLite.getTasks()
    if len(tasks) == 0:
        print("No existen tareas nuevas, verifique consultando el calendario")
    else:
        for x in tasks:
            print("Agregando Tarea:")
            x.print()
            #create_subject.create(x.subjectID)
            subjectList = subjectsBoard.get_list(x.subjectID)
            card = subjectList.add_card(x.title,x.description)
            card.assign(member_id)
            x.due_date = x.due_date[0:10] + " 19:00:00"
            card.set_due(datetime.strptime(x.due_date, '%Y-%m-%d %H:%M:%S'))
            #print(x.due_date)
            #card.set_due(x.due_date)
            updateTID = connectSQLite.addTarTID(x.id, subjectList.list_cards()[-1].id)
