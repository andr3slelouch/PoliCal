from ics import Calendar
from trello import TrelloClient
from polical import TareaClass, configuration, connectSQLite, MateriaClass
from datetime import datetime, timezone
import requests
import time


def save_tasks_to_db(url: str, username: str, user_dict: dict, trello_account=True):
    """Save incoming tasks to the database

    Args:
        url (str): ICS url for look for new tasks
        username (str): User owner of the tasks
        user_dict (dict): Dictionary that has user configurations
        trello_account (bool, optional): If tasks will be sended to trello. Defaults to True.
    """
    START_BOT_DATETIME = datetime.now(timezone.utc)
    virtual_class_calendar = Calendar(requests.get(url).text)
    events = []
    for temp_event in virtual_class_calendar.events:
        if temp_event.end.to("America/Guayaquil").datetime > START_BOT_DATETIME:
            events.append(temp_event)
    for task_event in events:
        event_category = list(task_event.categories)[0]
        task_subject = configuration.get_subject_name_from_ics_event_category(
            event_category
        )
        configuration.create_subject(
            task_subject, task_event.name, user_dict, username, trello_account
        )  # Crea lista a Trello
        subject_id = connectSQLite.get_subject_id(task_subject)
        task = TareaClass.Tarea(
            task_event.uid,
            task_event.name,
            task_event.description.replace("\t*", "*"),
            task_event.end.to("America/Guayaquil").datetime,
            subject_id,
        )
        connectSQLite.save_user_task(task, username)


def send_tasks_to_trello(username: str, user_dict: dict):
    """This function sends tasks from database that are stored as not sended to trello.

    Args:
        username (str): The username for the owner of the tasks.
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
        print("No existen tareas nuevas, verifique consultando el calendario")
    else:
        for task in tasks:
            print("Agregando Tarea:")
            task.print()
            subject_list = subjects_board.get_list(task.subject_id)
            card = subject_list.add_card(
                task.title, task.description.replace("\\n", "\n")
            )
            card.assign(member_id)
            card.set_due(datetime.strptime(task.due_date, "%Y-%m-%d %H:%M:%S%z"))
            connectSQLite.add_task_tid(
                task.id, subject_list.list_cards()[-1].id, username
            )
