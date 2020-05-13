import sqlite3
from polical import TareaClass
from polical import configuration

import logging
logging.basicConfig(filename=configuration.get_file_location('Running.log'), level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def getdb():
    db = sqlite3.connect(configuration.get_file_location('tasks.db'))
    return db


def getCur():
    cur = getdb().cursor()
    return cur


def exec(command):
    # Use all the SQL you like
    cur = getdb().cursor()
    cur.execute(command)
    getdb().commit()
    # db.close()
    return cur


def saveTask(task, username):
    cur = getdb().cursor()
    checker = "select count(TarUID) from Tareas where TarUID = \'" + \
        task.id + "\'"
    cur.execute(checker, ())
    exists = 0
    for row in cur.fetchall():
        exists = row[0]
        # print(exists)
    if exists == 0:
        logging.info("Ejecutando..." + str(exists))
        cur.execute("INSERT INTO Tareas(TarUID, TarTitulo, TarDescripcion, TarFechaLim, Materias_idMaterias) VALUES (?, ?, ?, ?, ?);",
                    (task.id, task.title, task.description.replace('\\n', '\n'), task.due_date, task.subjectID))
        cur.connection.commit()
        idTareas = getTaskID(task.id)
        idUsuarios = getUserID(username)
        cur.execute("INSERT INTO TareasUsuarios(TarUsrEstado, idTareas, idUsuarios) VALUES (?,?,?);",
                    ("N", idTareas, idUsuarios))
    cur.connection.commit()
    return cur


def saveSubjects(subject):
    query = "INSERT INTO Materias (MatNombre, MatCodigo, MatID) values (?, ?, ?);"
    cur = getdb().cursor()
    cur.execute(query, (subject.name, subject.codigo, subject.id))
    cur.connection.commit()
    # db.close()
    return cur


def saveUser(username):
    query = "INSERT INTO Usuarios (UsrNombre) values (?);"
    cur = getdb().cursor()
    cur.execute(query, (username,))
    cur.connection.commit()
    return cur


def saveSubjectID(subject):
    cur = getdb().cursor()
    cur.execute("UPDATE Materias SET MatID = ? WHERE MatCodigo = ?;",
                (subject.id, subject.codigo))
    cur.connection.commit()
    # db.close()
    return cur


def getCardsdb(db):
    cur = exec(
        "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Tareas';", getCur(db))
    # print all the first cell of all the rows
    cards = []
    for row in cur.fetchall():
        cards.append(row[0])
    db.close()
    return cards


def getSubjectID(subjCod):
    query = "select idMaterias from Materias where MatCodigo = \'" + subjCod + "\'"
    cur = getdb().cursor()
    cur.execute(query)
    # print all the first cell of all the rows
    sbjID = ''

    for row in cur.fetchall():
        sbjID = row[0]
    cur.connection.close()
    return sbjID


def getTaskID(TarUID):
    query = "select idTareas from Tareas where TarUID = \'" + TarUID + "\'"
    cur = getdb().cursor()
    cur.execute(query)

    idTareas = ''
    for row in cur.fetchall():
        idTareas = row[0]
    cur.connection.close()
    return str(idTareas)


def getUserID(username):
    query = "select idUsuarios from Usuarios where UsrNombre = \'" + username + "\'"
    cur = getdb().cursor()
    cur.execute(query)

    idUsuarios = ''
    for row in cur.fetchall():
        idUsuarios = row[0]
    cur.connection.close()
    return str(idUsuarios)


def getSubjectName(subjCod):
    query = "select MatNombre from Materias where MatCodigo = \'" + subjCod + "\'"
    cur = getdb().cursor()
    cur.execute(query)
    # print all the first cell of all the rows
    sbjName = ''

    for row in cur.fetchall():
        sbjName = row[0]
    cur.connection.close()
    return sbjName


def addTarTID(TarUID, TarTID, username):
    cur = getdb().cursor()
    idTareas = getTaskID(TarUID)
    idUsuarios = getUserID(username)
    cur.execute(
        "UPDATE TareasUsuarios SET TarUsrTID = ?, TarUsrEstado = ? WHERE idUsuarios = ? AND idTareas = ?;", (TarTID, "E", idUsuarios, idTareas))
    cur.connection.commit()
    # db.close()
    return cur


def getTasks(username):
    idUsuarios = getUserID(username)
    query = "select TarUsrEstado, TarUID, TarTitulo, TarDescripcion, TarFechaLim, MatID from Materias, Tareas, TareasUsuarios where Tareas.Materias_idMaterias = Materias.idMaterias AND TareasUsuarios.TarUsrEstado = 'N' AND TareasUsuarios.idTareas = Tareas.idTareas AND TareasUsuarios.idUsuarios = \'" + idUsuarios + "\';"
    cur = getdb().cursor()
    cur.execute(query)
    tasks = []
    for row in cur.fetchall():
        tasks.append(TareaClass.Tarea(row[1], row[2], row[3], row[4], row[5]))
    cur.connection.close()
    return tasks


def check_no_subjectID(subjCod):
    query = "select count(MatCodigo) from Materias where MatCodigo=\'" + \
        subjCod + "\'AND MatID=\"\";"
    cur = getdb().cursor()
    cur.execute(query)
    for row in cur.fetchall():
        result = row[0]
    cur.connection.close()
    return result


def check_user_existence(username):
    query = "select count(UsrNombre) from Usuarios where UsrNombre=\'" + \
        username + "\';"
    cur = getdb().cursor()
    cur.execute(query)
    for row in cur.fetchall():
        result = row[0]
    cur.connection.close()
    return result
