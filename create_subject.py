import MateriaClass
import TareaClass
import csv
from trello import TrelloClient
import connectSQLite
#f = open("calendar.csv","r")
def create(subjCod):
    client = TrelloClient(api_key='6fb47d30d0303eeaa0b4aa2f5ae07370',
                          token='2a453ae9ffbd78256fa1f7386978a3c1af7f9b5c5140878fd7f9d58b7d8420ba')
    all_boards = client.list_boards()
    last_board = all_boards[-2]
    id = ''
    subjectsBoard = all_boards[-2]
    if not subjectsBoard.id == "5a58b05cd33b764906df27bd":
        for x in all_boards:
            if x.id == "5a58b05cd33b764906df27bd":
                subjectsBoard = x
    else:
        print("yes")

    if(connectSQLite.check_subject_existence(subjCod) == 0):
        subject_name = input("Se ha detectado una nueva materia, ingrese el nombre de la materia:")
        subjectsBoard.add_list(subject_name)
        for x in subjectsBoard.list_lists():
            if x.name == row[1]:
                id = x.id
        subject = MateriaClass.Materia(id,subject_name,subjCod)
        print(subject.print())
        sql = connectSQLite.saveSubjects(subject)
        for row in sql.fetchall():
            print(row)
        sql = connectSQLite.getdb().close()
