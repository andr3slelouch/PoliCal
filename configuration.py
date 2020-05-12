import yaml
import os
import Get_Trello_MoodleEPN_Keys
import re

import logging
logging.basicConfig(filename='Running.log',level=logging.INFO,
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
            Get_Trello_MoodleEPN_Keys.onboard(False)


def get_file_location(filename):
    workingDirectory = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(workingDirectory, filename)


def check_for_url(url):
    checker = re.search("^https.*recentupcoming$", url)
    if (checker):
        return True
    else:
        return False
