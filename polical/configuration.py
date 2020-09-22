"""
.. module:: configuration
   :platform: Unix, Windows
   :synopsis: This module gets paths for files, and adds lists for the subjects in trello.

.. moduleauthor:: Luis Andrade <andr3slelouch@github.com>


"""
import yaml
import os
import re
import sys
import logging
from shutil import copyfile
from pathlib import Path
from polical import MateriaClass
from trello import TrelloClient
from polical import connectSQLite
import logging
from polical import configuration


def get_working_directory() -> str:
    """This functions gets the working directory path.

    Returns:
        working_directory (str): The directory where database and yaml are located.
    """
    db_filename = "tasks.db"
    userdir = os.path.expanduser("~")
    working_directory = os.path.join(userdir, "PoliCal")
    tasks_db = Path(os.path.join(working_directory, db_filename))
    # Check for existence
    if not os.path.exists(working_directory):
        os.makedirs(working_directory)
    # Check for existence
    if not tasks_db.is_file():
        dir_path = os.path.dirname(__file__)
        tasks_src = os.path.join(dir_path, db_filename)
        tasks_dst = os.path.join(working_directory, db_filename)
        copyfile(tasks_src, tasks_dst)
    return working_directory


def get_file_location(filename: str) -> str:
    """This function is for getting full path location of a file from its filename

    Args:
        filename (str): Filename that needs the full path location

    Returns:
        full_path_file_location (str): Full path location of the file
    """
    working_directory = get_working_directory()
    full_path_file_location = os.path.join(working_directory, filename)
    return full_path_file_location


logging.basicConfig(
    filename=get_file_location("Running.log"),
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


def load_config_file(config_file_path: str) -> dict:
    """This function is for loading yaml config file

    Args:
        config_file_path (str): File path for the config file to be loaded

    Returns:
        file_config (dict): Dictionary with config keys.

    Raises:
        IOError
    """
    try:
        with open(get_file_location(config_file_path), "r") as config_yaml:
            file_config = yaml.safe_load(config_yaml)
            return file_config
    except IOError:
        logging.error("Archivo de configuración no encontrado, generando llaves")


def check_for_url(url: str) -> bool:
    """This function is for checking moodle calendar url

    Args:
        url (str): Moodle Calendar Address to be checked

    Returns:
        bool.  The return code::

          False -- If the url does not start with https and ends with recentupcoming
          True -- If the url starts with https and ends with recentupcoming
    """
    checker = re.search("^https.*recentupcoming$", url)
    if checker:
        return True
    else:
        return False


def create_subject(subject_code: str, task_title: str, user_dict: str):
    """This function creates a subject in Trello and adds it to local database.

    Args:
        subject_code (str): Subject Code to check with local database and trello.
        task_title (str): Subject title for showing to the user if subject is not founded in local database.
        user_dict (dict): User dictionary with keys to connect to trello.
    """
    client = TrelloClient(
        api_key=user_dict["api_key"],
        api_secret=user_dict["api_secret"],
        token=user_dict["oauth_token"],
        token_secret=user_dict["oauth_token_secret"],
    )
    subjects_board = client.get_board(user_dict["board_id"])
    if connectSQLite.check_no_subject_id(subject_code) == 1:
        subject_name = connectSQLite.get_subject_name(subject_code)
        logging.info(subject_name)
        print(subject_name)
        add_subject_to_trello_list(subjects_board, subject_name, subject_code)
    elif connectSQLite.get_subject_name(subject_code) == "":
        logging.info(
            "Nombre de materia no encontrado, titulo de la tarea:" + str(task_title)
        )
        print("\n Nombre de materia no encontrado, titulo de la tarea:" + task_title)
        logging.info("Por favor agregue el nombre de la materia:")
        subject_name = input("Por favor agregue el nombre de la materia:")
        logging.info(subject_name)
        response = "N"
        while response == "N" or response == "n":
            logging.info("¿El nombre de la materia " + subject_name + " es correcto?")
            print("¿El nombre de la materia " + subject_name + " es correcto?")
            logging.info("¿Guardar? S/N:")
            response = input("¿Guardar? S/N:")
            logging.info(response)
        subject = MateriaClass.Materia(subject_name, subject_code)
        connectSQLite.save_subject(subject)
        add_subject_to_trello_list(subjects_board, subject_name, subject_code)


def add_subject_to_trello_list(subjects_board, subject_name: str, subject_code: str):
    """This function adds a list to trello board with subject name.

    Args:
        subjects_board (Trello.Board): Tareas Poli's Board object from Trello library
        subject_name (str): Subject name to create new list.
        subject_code (str): Subject code to add it to name list.
    """
    trello_list_id = ""
    for trello_list in subjects_board.list_lists():
        if trello_list.name == subject_name:
            trello_list_id = trello_list.id
    if trello_list_id == "":
        subjects_board.add_list(subject_name)
        for trello_list in subjects_board.list_lists():
            if trello_list.name == subject_name:
                trello_list_id = trello_list.id
    subject = MateriaClass.Materia(subject_name, subject_code, trello_list_id)
    logging.info(subject.print())
    connectSQLite.save_subject_id(subject)


def get_subject_name_from_ics_event_category(full_subject_name):
    """This function gets subject name from the categories in ics event

    Args:
        full_subject_name (str): Full subject name with format XXX_YYY_ZZZ

    Return:
        subject_name (str): Subject name
    """
    full_subject_name_list = full_subject_name.split("_", 3)
    subject_name = full_subject_name_list[1]
    return subject_name
