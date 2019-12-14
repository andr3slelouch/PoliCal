import MateriaClass
import TareaClass
import csv
from trello import TrelloClient
#f = open("calendar.csv","r")
client = TrelloClient(api_key='6fb47d30d0303eeaa0b4aa2f5ae07370',
                      token='2a453ae9ffbd78256fa1f7386978a3c1af7f9b5c5140878fd7f9d58b7d8420ba')
all_boards = client.list_boards()
last_board = all_boards[-2]
id = ''
try:
    with open('materias2.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                # print(last_board.name)
                for x in last_board.list_lists():
                    if x.name == row[1]:
                        id = x.id
                        #print(x.name, x.id)
                #my_list = last_board.get_list(id)
                subject = MateriaClass.Materia(id, row[1], row[0])
                print(subject.print())
                sql = connectMySql.saveSubjects(subject)
                #sql = connectMySql.exec("COMMIT;",connectMySql.getCur())
                for row in sql.fetchall():
                    print(row)
                sql = connectMySql.getdb().close()
except:
    print("FALSE")
#            line_count += 1
#    print(f'Processed {line_count} lines.')
