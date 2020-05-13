from polical import TareasCSVToBD
from polical import SendTaskToTrello
from polical import SimpleIcsToCSV
from polical import configuration
import sys
from polical import Get_Trello_MoodleEPN_Keys


def main(argv):
    if len(argv) == 2:
        argument = argv[1]
        if argument == "--addUser":
            Get_Trello_MoodleEPN_Keys.onboard(False)
    else:
        users = None
        while(users == None):
            users = configuration.load_config_file("polical.yaml")
            if users == None:
                Get_Trello_MoodleEPN_Keys.onboard(False)
        for user in users.keys():
            SimpleIcsToCSV.convertICStoCSV(users[user]['calendar_url'])
            TareasCSVToBD.LoadCSVTasktoDB(user, users[user])
            SendTaskToTrello.SendTaskToTrello(user, users[user])


if __name__ == "__main__":
    main(sys.argv)
