from scheduler import Scheduler

import SimpleIcsToCSV
import TareasCSVToBD
import SendTaskToTrello

def ejecutaScript():	#Define la funcion
    SimpleIcsToCSV.convertICStoCSV()
    TareasCSVToBD.LoadCSVTasktoDB()
    SendTaskToTrello.SendTaskToTrello()    

scheduler = Scheduler()
scheduler.add(3600, 0, ejecutaScript)  # Agrega una tarea.

while True:
    scheduler.run()