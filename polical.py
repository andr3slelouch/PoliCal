import TareasCSVToBD
import SendTaskToTrello
import SimpleIcsToCSV
import configuration
import sys
import Get_Trello_MoodleEPN_Keys


def main(argv):
    if len(argv) == 2:
        argument = argv[1]
        if argument == "--addUser":
            Get_Trello_MoodleEPN_Keys.onboard(True)
    else:
        users = configuration.load_config_file("polical.yaml")
        for user in users.keys():
            SimpleIcsToCSV.convertICStoCSV(users[user]['calendar_url'])
            TareasCSVToBD.LoadCSVTasktoDB(user, users[user])
            SendTaskToTrello.SendTaskToTrello(user, users[user])


if __name__ == "__main__":
    main(sys.argv)
