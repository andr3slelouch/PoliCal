import yaml
import os
import Get_Trello_MoodleEPN_Keys


def load_config_file(config_file):
    while(True):
        try:
            with open(get_file_location(config_file), 'r') as config_yaml:
                file_config = yaml.safe_load(config_yaml)
                return file_config
        except IOError:
            print("Archivo de configuración no encontrado, generando llaves")
            Get_Trello_MoodleEPN_Keys.onboard(False)


def get_file_location(filename):
    workingDirectory = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(workingDirectory, filename)
