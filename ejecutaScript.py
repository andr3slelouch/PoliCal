from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

#import os
import SimpleIcsToCSV
import TareasCSVToBD
import SendTaskToTrello

def ejecutaScript():	#Define la funcion
    SimpleIcsToCSV.convertICStoCSV()
    TareasCSVToBD.LoadCSVTasktoDB()
    SendTaskToTrello.SendTaskToTrello()

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_executor('processpool')
    scheduler.add_job(ejecutaScript, 'interval', seconds=3600)
    #print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass