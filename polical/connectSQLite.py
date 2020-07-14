import sqlite3
from polical import TareaClass
from polical import configuration

import logging
logging.basicConfig(filename=configuration.get_file_location('Running.log'), level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def getdb():
    """This function returns the sqlite3 database connection that storages all tasks and subjects.
  
    Returns:
        db (Connection): Database connection that access to tasks and subjects.
    """
    db = sqlite3.connect(configuration.get_file_location('tasks.db'))
    return db


def getCur():
    """This function returns the database cursor
  
    Returns:
        cur (Cursor): Database cursor that access to tasks and subjects.
    """
    cur = getdb().cursor()
    return cur


def exec(command):
    """This function executes a coomand in the database.

    Args:
        command (str): Query that needs to be executed on the database.
    
    Returns:
        cur (Cursor): Database cursor that access to tasks and subjects.
    """
    # Use all the SQL you like
    cur = getdb().cursor()
    cur.execute(command)
    getdb().commit()
    # db.close()
    return cur


def saveTask(task, username):
    """This function saves a task from a user into the database

    Args:
        task (Tarea): Tasks that would be added to the database.
        username(str): User owner of the task.
    
    Returns:
        cur (Cursor): Database cursor that access to tasks and subjects.
    """
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
    """This function saves a subject into the database

    Args:
        subject (Materia): Subject that would be added to the database.
    
    Returns:
        cur (Cursor): Database cursor that access to tasks and subjects.
    """
    query = "INSERT INTO Materias (MatNombre, MatCodigo, MatID) values (?, ?, ?);"
    cur = getdb().cursor()
    cur.execute(query, (subject.name, subject.codigo, subject.id))
    cur.connection.commit()
    # db.close()
    return cur


def saveUser(username):
    """This function saves a user into the database

    Args:
        username (str): User to be added into the database
    
    Returns:
        cur (Cursor): Database cursor that access to tasks and subjects.
    """
    print("Agregando usuario, "+username+"a la base de datos")
    query = "INSERT INTO Usuarios (UsrNombre) values (?);"
    cur = getdb().cursor()
    cur.execute(query, (username,))
    cur.connection.commit()
    return cur


def saveSubjectID(subject):
    """This function saves the trello list ID into the database

    Args:
        subject (Materia): Subject that owns the ID that would be added to the database.
    
    Returns:
        cur (Cursor): Database cursor that access to tasks and subjects.
    """
    cur = getdb().cursor()
    cur.execute("UPDATE Materias SET MatID = ? WHERE MatCodigo = ?;",
                (subject.id, subject.codigo))
    cur.connection.commit()
    # db.close()
    return cur


def getCardsdb(db):
    """This function get all cards from Tareas table.

    Args:
        db (Connection): Database connection.
    
    Returns:
        cards (list): List contanining all cards from Tareas table.
    """
    cur = exec(
        "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Tareas';", getCur(db))
    # print all the first cell of all the rows
    cards = []
    for row in cur.fetchall():
        cards.append(row[0])
    db.close()
    return cards


def getSubjectID(subjCod):
    """This function gets the subject ID from the database

    Args:
        subjCod (str): Subject code from the subject to get the ID.
    
    Returns:
        sbjID (str): Subject ID from the subject.
    """
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
    """This function gets the task ID from the database

    Args:
        TarUID (str): Task UID from the task to get the ID.
    
    Returns:
        idTareas (str): Task ID from the task.
    """
    query = "select idTareas from Tareas where TarUID = \'" + TarUID + "\'"
    cur = getdb().cursor()
    cur.execute(query)

    idTareas = ''
    for row in cur.fetchall():
        idTareas = row[0]
    cur.connection.close()
    idTareas = str(idTareas)
    return idTareas


def getUserID(username):
    """This function gets the User ID from the database

    Args:
        username (str): Username to get his ID.
    
    Returns:
        idUsuarios (str): The user id from the database.
    """
    query = "select idUsuarios from Usuarios where UsrNombre = \'" + username + "\'"
    cur = getdb().cursor()
    cur.execute(query)

    idUsuarios = ''
    for row in cur.fetchall():
        idUsuarios = row[0]
    cur.connection.close()
    idUsuarios = str(idUsuarios)
    return idUsuarios


def getSubjectName(subjCod):
    """This function gets the subject Name from the database

    Args:
        subjCod (str): Subject code for get the subject name.
    
    Returns:
        sbjName (str): The subject name from the subject code.
    """
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
    """This function adds the task trello ID into the database

    Args:
        TarUID (str): Task UID from ICS file.
        TarTID (str): New Task Trello ID from trello.
        username (str): Username from the user that owns the task
    
    Returns:
        cur (Cursor): Database cursor that access to tasks and subjects.
    """
    cur = getdb().cursor()
    idTareas = getTaskID(TarUID)
    idUsuarios = getUserID(username)
    cur.execute(
        "UPDATE TareasUsuarios SET TarUsrTID = ?, TarUsrEstado = ? WHERE idUsuarios = ? AND idTareas = ?;", (TarTID, "E", idUsuarios, idTareas))
    cur.connection.commit()
    # db.close()
    return cur


def getTasks(username):
    """This function gets all unsended tasks from the user.

    Args:
        username (str): Username from the user that owns the task
    
    Returns:
        tasks (list): Database cursor that access to tasks and subjects.
    """
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
    """This function checks if the subject has an ID in the database.

    Args:
        subjCod (str): Subject code from the database to check if it has ID or not.
    
    Returns:
        result (str): Returns '0' if does not has the ID and '1' if it has it.
    """
    query = "select count(MatCodigo) from Materias where MatCodigo=\'" + \
        subjCod + "\'AND MatID=\"\";"
    cur = getdb().cursor()
    cur.execute(query)
    for row in cur.fetchall():
        result = row[0]
    cur.connection.close()
    return result


def check_user_existence(username):
    """This function checks if the username has an ID in the database.

    Args:
        username (str): username from the database to check if it has ID or not.
    
    Returns:
        result (str): Returns '0' if does not has the ID and '1' if it has it.
    """
    query = "select count(UsrNombre) from Usuarios where UsrNombre=\'" + \
        username + "\';"
    cur = getdb().cursor()
    cur.execute(query)
    for row in cur.fetchall():
        result = row[0]
    cur.connection.close()
    return result
