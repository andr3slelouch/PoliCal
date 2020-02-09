from trello import TrelloClient
import connectSQLite
import configuration
from datetime import datetime

import logging
logging.basicConfig(filename='Running.log',level=logging.INFO, format = '%(asctime)s:%(levelname)s:%(message)s')


config = configuration.load_config_file('polical.yaml')
client = TrelloClient(
    api_key=config['api_key'],
    api_secret=config['api_secret'],
    token=config['oauth_token'],
    token_secret=config['oauth_token_secret'],
)
member_id = config['owner_id']


def SendTaskToTrello():
    subjectsBoard = client.get_board(config['board_id'])
    tasks = connectSQLite.getTasks()
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
            connectSQLite.addTarTID(x.id, subjectList.list_cards()[-1].id)
