from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# import os
from polical import SimpleIcsToCSV
from polical import TareasCSVToBD
from polical import SendTaskToTrello


def ejecutaScript():  # Define la funcion
    SimpleIcsToCSV.convert_ics_to_csv()
    TareasCSVToBD.load_csv_tasks_to_db()
    SendTaskToTrello.SendTaskToTrello()


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_executor("processpool")
    scheduler.add_job(ejecutaScript, "interval", seconds=3600)
    # print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
