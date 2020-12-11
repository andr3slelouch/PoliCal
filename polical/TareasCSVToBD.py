"""
.. module:: TareasCSVtoBD
   :platform: Unix, Windows
   :synopsis: This module reads csv tasks and writes to the database

.. moduleauthor:: Luis Andrade <andr3slelouch@github.com>


"""
from polical import TareaClass
import csv
from polical import connectSQLite
from polical import configuration
from datetime import datetime
import logging

logging.basicConfig(
    filename=configuration.get_file_location("Running.log"),
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


def load_csv_tasks_to_db(username: str, user_dict: dict):
    """This function loads csv tasks to the database

    Args:
        username (str): The username for the current task.
        user_dict (dict): User dictionary with keys to acces to trello.

    Raises:
        FileNotFoundError
    """
    try:
        with open(configuration.get_file_location("calendar.csv")) as csv_file:
            logging.info("CSV abierto.")
            csv_reader = csv.reader(csv_file, delimiter=";")
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                elif len(row) > 9 and not line_count == 0:
                    # print(len(row))
                    configuration.create_subject(
                        get_subject_name_from_csv(row[9]), row[2], user_dict
                    )
                    subject_id = connectSQLite.get_subject_id(
                        get_subject_name_from_csv(row[9])
                    )
                    # print(row[0])
                    # Siempre se extraera la fecha aun cuando pueda tener un
                    # formato YMDTXXX
                    task = TareaClass.Tarea(
                        row[1],
                        row[2],
                        row[3],
                        datetime.strptime(row[7][0:8], "%Y%m%d"),
                        subject_id,
                    )
                    connectSQLite.save_user_task(task, username)
                    # print("Las tareas nuevas se agregaron a la BD")
                    logging.info("Las tareas nuevas se agregaron a la BD")
    except (FileNotFoundError):
        print("!FNF")


def get_subject_name_from_csv(full_subject_name):
    """This function gets subject name from csv

    Args:
        full_subject_name (str): Full subject name with format XXX_YYY_ZZZ

    Return:
        subject_name (str): Subject name
    """
    full_subject_name_list = full_subject_name.split("_", 3)
    subject_name = full_subject_name_list[1]
    return subject_name
