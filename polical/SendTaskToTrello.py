"""
.. module:: SendTaskToTrello
   :platform: Unix, Windows
   :synopsis: This module sends tasks from the database to trello.

.. moduleauthor:: Luis Andrade <andr3slelouch@github.com>


"""
from trello import TrelloClient
from polical import connectSQLite
from polical import configuration
from datetime import datetime
import logging

logging.basicConfig(
    filename=configuration.get_file_location("Running.log"),
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


def send_task_to_trello(username: str, user_dict: dict):
    """This function sends tasks from database that are stored as not sended to trello.

    Args:
        username (str): The username for the current task.
        user_dict (dict): User dictionary with keys to acces to trello.
    """
    client = TrelloClient(
        api_key=user_dict["api_key"],
        api_secret=user_dict["api_secret"],
        token=user_dict["oauth_token"],
        token_secret=user_dict["oauth_token_secret"],
    )
    member_id = user_dict["owner_id"]
    subjects_board = client.get_board(user_dict["board_id"])
    tasks = connectSQLite.get_unsended_tasks(username)
    if len(tasks) == 0:
        logging.info("No existen tareas nuevas, verifique consultando el calendario")
        print("No existen tareas nuevas, verifique consultando el calendario")
    else:
        for task in tasks:
            logging.info(
                "Agregando Tarea:"
                + task.subject_id
                + " "
                + task.title
                + " "
                + task.description
                + " "
                + task.due_date
            )
            print("Agregando Tarea:")
            task.print()
            subject_list = subjects_board.get_list(task.subject_id)
            card = subject_list.add_card(
                task.title, task.description.replace("\\n", "\n")
            )
            card.assign(member_id)
            task.due_date = task.due_date[0:10] + " 07:00:00"
            card.set_due(datetime.strptime(task.due_date, "%Y-%m-%d %H:%M:%S"))
            connectSQLite.add_task_tid(
                task.id, subject_list.list_cards()[-1].id, username
            )
