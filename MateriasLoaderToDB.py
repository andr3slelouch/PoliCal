import MateriaClass
import csv
import connectSQLite
import configuration

try:
    with open(configuration.get_file_location('materias.csv')) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                subject = MateriaClass.Materia(row[1], row[0])
                print(subject.print())
                sql = connectSQLite.saveSubjects(subject)
                for row in sql.fetchall():
                    print(row)
                sql = connectSQLite.getdb().close()
except:
    print("FALSE")
#            line_count += 1
#    print(f'Processed {line_count} lines.')
