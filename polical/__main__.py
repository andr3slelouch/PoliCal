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
import argparse


def define_args():
    """This function defines the arguments for cli

    Returns:
        args(Namespace): The namespace with the defined arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--add_user",
        "-au",
        help="Add a new user with interactive cli",
        action="store_true",
    )
    parser.add_argument(
        "--todo",
        "-t",
        help="Look for tasks adn write to todo.txt and done.txt",
        action="store_true",
    )
    parser.add_argument(
        "--bot",
        "-b",
        help="Executes the bot for telegram it requires a mysql database executing and a token for Telegram Bot",
        action="store_true",
    )
    parser.add_argument(
        "--load_subjects_from_csv",
        "-lcsv",
        help="Load new subjects to the sqlite3 database from materias.csv located in working directory",
        action="store_true",
    )
    parser.add_argument(
        "--update_subjects_from_csv",
        "-ucsv",
        help="Updates subjects to the sqlite3 database from materias.csv located in working directory",
        action="store_true",
    )
    parser.add_argument(
        "--show_directory",
        "-sd",
        help="Prints the working directory address where the config files are saved",
        action="store_true",
    )
    parser.add_argument(
        "--set_telegram_token",
        "-tk",
        help="Save the telegram token to config.yaml configuration file",
    )
    args = parser.parse_args()
    return args


def main(argv):
    configuration.set_preffered_dbms("default")
    args = define_args()
    if args.add_user:
        Get_Trello_MoodleEPN_Keys.onboard(False)
    elif args.todo:
        todo_generator.generate_todo_txt()
    elif args.bot:
        policalbot.run()
    elif args.load_subjects_from_csv:
        MateriasLoaderToDB.load_subjects_to_db()
    elif args.update_subjects_from_csv:
        MateriasLoaderToDB.update_subjects_to_db()
    elif args.show_directory:
        print("Working directory in: " + configuration.get_working_directory())
    elif args.set_telegram_token:
        token = configuration.get_bot_token("config.yaml")
        if token:
            answer = input(
                "Found existing Telegram Token: " + token + ", overwrite? (y/n): "
            )
            if answer == "y" or answer == "yes" or answer == "Y" or answer == "YES":
                configuration.set_bot_token(
                    configuration.get_file_location("config.yaml"),
                    args.set_telegram_token,
                )
            else:
                print("Operation Canceled")
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
