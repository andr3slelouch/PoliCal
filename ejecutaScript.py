from scheduler import Scheduler
import polycal

def ejecutaScript():	#Define la funcion
    python polycal.py    

scheduler = Scheduler()
scheduler.add(3600, 0, ejecutaScript)  # Agrega una tarea.

while True:
    scheduler.run()