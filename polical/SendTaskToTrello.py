from trello import TrelloClient
from polical import connectSQLite
from polical import configuration
from datetime import datetime
import logging
logging.basicConfig(filename=configuration.get_file_location('Running.log'),level=logging.INFO, format = '%(asctime)s:%(levelname)s:%(message)s')


def SendTaskToTrello(username, user_dict):
    #user_dict = configuration.load_config_file('polical.yaml')
    client = TrelloClient(
        api_key=user_dict['api_key'],
        api_secret=user_dict['api_secret'],
        token=user_dict['oauth_token'],
        token_secret=user_dict['oauth_token_secret'],
    )
    member_id = user_dict['owner_id']
    subjectsBoard = client.get_board(user_dict['board_id'])
    tasks = connectSQLite.getTasks(username)
    if len(tasks) == 0:
        logging.info("No existen tareas nuevas, verifique consultando el calendario")
        print("No existen tareas nuevas, verifique consultando el calendario")
    else:
        for x in tasks:
            logging.info("Agregando Tarea:" + x.subjectID +" "+ x.title + " " + x.description + " " + x.due_date)
            print("Agregando Tarea:")
            x.print()
            subjectList = subjectsBoard.get_list(x.subjectID)
            card = subjectList.add_card(
                x.title, x.description.replace('\\n', '\n'))
            card.assign(member_id)
            x.due_date = x.due_date[0:10] + " 07:00:00"
            card.set_due(datetime.strptime(x.due_date, '%Y-%m-%d %H:%M:%S'))
            # print(x.due_date)
            # card.set_due(x.due_date)
            connectSQLite.addTarTID(x.id, subjectList.list_cards()[-1].id, username)
