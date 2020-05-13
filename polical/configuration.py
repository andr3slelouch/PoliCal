import yaml
import os
import re
import sys
import logging
from shutil import copyfile
from pathlib import Path


def get_working_directory():
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
    workingDirectory = get_working_directory()
    return os.path.join(workingDirectory, filename)


logging.basicConfig(filename=get_file_location('Running.log'), level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def load_config_file(config_file_path):
    while(True):
        try:
            with open(get_file_location(config_file_path), 'r') as config_yaml:
                file_config = yaml.safe_load(config_yaml)
                return file_config
        except IOError:
            logging.error(
                "Archivo de configuración no encontrado, generando llaves")
            return None


def check_for_url(url):
    checker = re.search("^https.*recentupcoming$", url)
    if (checker):
        return True
    else:
        return False
