from polical import TareasCSVToBD
from polical import SendTaskToTrello
from polical import SimpleIcsToCSV
from polical import configuration
import sys
from polical import Get_Trello_MoodleEPN_Keys
from polical import tasks_processor
from polical import todo_generator
from polical import configuration
from polical.bot import policalbot
from polical import MateriasLoaderToDB


def main(argv):
    configuration.set_preffered_dbms("default")
    if len(argv) == 2:
        argument = argv[1]
        if argument == "--addUser":
            Get_Trello_MoodleEPN_Keys.onboard(False)
        if argument == "--todo":
            todo_generator.generate_todo_txt()
        if argument == "--bot":
            policalbot.run()
        if argument == "--load_subjects_from_csv":
            MateriasLoaderToDB.load_subjects_to_db()
        if argument == "--update_subjects_from_csv":
            MateriasLoaderToDB.update_subjects_to_db()
    else:
        users = None
        while users is None:
            users = configuration.load_config_file("polical.yaml")
            if users is None:
                Get_Trello_MoodleEPN_Keys.onboard(False)
        for user in users.keys():
            tasks_processor.save_tasks_to_db(
                users[user]["calendar_url"], user, users[user]
            )
            tasks_processor.send_tasks_to_trello(user, users[user])


if __name__ == "__main__":
    main(sys.argv)
