import yaml
import Get_Trello_MoodleEPN_Keys
def load_config_file(config_file):
    while(True):
        try:
            with open(config_file, 'r') as config_yaml:
                file_config = yaml.safe_load(config_yaml)
                return file_config
        except:
            print("Archivo de configuración no encontrado, generando llaves")
            Get_Trello_MoodleEPN_Keys.onboard(False)
