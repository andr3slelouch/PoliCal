import TareaClass
import csv
import connectSQLite
import create_subject
import configuration
from datetime import datetime
import logging
logging.basicConfig(filename='Running.log',level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def LoadCSVTasktoDB(username, user_dict):
    with open(configuration.get_file_location('calendar.csv')) as csv_file:
        logging.info("CSV abierto.")
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            elif len(row) > 9 and not line_count == 0:
                # print(len(row))
                create_subject.create(
                    Get_Subject_Name_From_CSV(row[9]),row[2])
                sbjID = connectSQLite.getSubjectID(
                    Get_Subject_Name_From_CSV(row[9]))
                # print(row[0])
                # Siempre se extraera la fecha aun cuando pueda tener un
                # formato YMDTXXX
                task = TareaClass.Tarea(
                    row[1], row[2], row[3], datetime.strptime(row[7][0:8], '%Y%m%d'), sbjID)
                sql = connectSQLite.saveTask(task, username)
                # print("Las tareas nuevas se agregaron a la BD")
                logging.info("Las tareas nuevas se agregaron a la BD")
                sql.connection.close()


def Get_Subject_Name_From_CSV(full_subject_name):
    list = full_subject_name.split("_", 3)
    return list[1]
