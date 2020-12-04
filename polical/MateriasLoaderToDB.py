from polical import MateriaClass
import csv
from polical import connectSQLite
from polical import configuration
import logging

logging.basicConfig(
    filename=configuration.get_file_location("Running.log"),
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


def load_subject_to_db():
    """This function loads any subject located on materias.csv to the database."""
    try:
        with open(configuration.get_file_location("materias.csv")) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    logging.info(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    subject = MateriaClass.Materia(row[1], row[0])
                    logging.info(subject.print())
                    sql = connectSQLite.save_subject(subject)
                    for row in sql.fetchall():
                        logging.info(row)
                    sql = connectSQLite.get_db().close()
    except Exception as error:
        logging.info("FALSE, exception ocurred")
        print(error)
    #            line_count += 1
    #    print(f'Processed {line_count} lines.')


load_subject_to_db()
