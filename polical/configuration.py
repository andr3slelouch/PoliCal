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


def get_working_directory():
    """This functions gets the working directory path.
    
    Returns:
        workingDirectory (str): The directory where database and yaml are located.
    """
    userdir = os.path.expanduser("~")
    workingDirectory = os.path.join(userdir, "PoliCal")
    tasks_db = Path(os.path.join(workingDirectory, "tasks.db"))
    # Check for existence
    if not os.path.exists(workingDirectory):
        os.makedirs(workingDirectory)
    # Check for existence
    if not tasks_db.is_file():
        dir = os.path.dirname(__file__)
        tasks_src = os.path.join(dir, "tasks.db")
        tasks_dst = os.path.join(workingDirectory, "tasks.db")
        copyfile(tasks_src, tasks_dst)
    return workingDirectory


def get_file_location(filename):
    """This function is for getting full path location of a file from its filename

    Args:
        filename (str): Filename that needs the full path location
    
    Returns:
        full_path_file_location (str): Full path location of the file
    """
    workingDirectory = get_working_directory()
    full_path_file_location = os.path.join(workingDirectory, filename)
    return full_path_file_location


logging.basicConfig(filename=get_file_location('Running.log'), level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def load_config_file(config_file_path):
    """This function is for loading yaml config file

    Args:
        config_file_path (str): File path for the config file to be loaded
    
    Returns:
        file_config (dict): Dictionary with config keys.
        
    Raises:
        IOError
    """
    try:
        with open(get_file_location(config_file_path), 'r') as config_yaml:
            file_config = yaml.safe_load(config_yaml)
            return file_config
    except IOError:
        logging.error(
            "Archivo de configuración no encontrado, generando llaves")
        return None


def check_for_url(url):
    """This function is for checking moodle calendar url

    Args:
        url (str): Moodle Calendar Address to be checked
    
    Returns:
        bool.  The return code::

          False -- If the url does not start with https and ends with recentupcoming 
          True -- If the url starts with https and ends with recentupcoming
    """
    checker = re.search("^https.*recentupcoming$", url)
    if (checker):
        return True
    else:
        return False


def create_subject(subjCod, task_title, user_dict):
    """This function creates a subject in Trello and adds it to local database.

    Args:
        subjCod (str): Subject Code to check with local database and trello.
        task_title (str): Subject title for showing to the user if subject is not founded in local database.
        user_dict (dict): User dictionary with keys to connect to trello.
    """
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
            "Nombre de materia no encontrado, titulo de la tarea:" + str(task_title))
        print("\n Nombre de materia no encontrado, titulo de la tarea:" + task_title)
        logging.info("Por favor agregue el nombre de la materia:")
        subject_name = input("Por favor agregue el nombre de la materia:")
        logging.info(subject_name)
        response = "N"
        while response == "N" or response == "n":
            logging.info("¿El nombre de la materia " +
                         subject_name + " es correcto?")
            print("¿El nombre de la materia " + subject_name + " es correcto?")
            logging.info("¿Guardar? S/N:")
            response = input("¿Guardar? S/N:")
            logging.info(response)
        subject = MateriaClass.Materia(subject_name, subjCod)
        connectSQLite.saveSubjects(subject)
        Add_Subject_To_Trello_List(subjectsBoard, subject_name, subjCod)


def Add_Subject_To_Trello_List(subjectsBoard, subject_name, subjCod):
    """This function adds a list to trello board with subject name.

    Args:
        subjectsBoard (Trello.Board): Tareas Poli's Board object from Trello library
        subject_name (str): Subject name to create new list.
        subjCode (str): Subject code to add it to name list.
    """
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
