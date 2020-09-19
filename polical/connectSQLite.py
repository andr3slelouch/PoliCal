import sqlite3
from polical import TareaClass
from polical import configuration

import logging

logging.basicConfig(
    filename=configuration.get_file_location("Running.log"),
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


def get_db():
    """This function returns the sqlite3 database connection that storages all tasks and subjects.

    Returns:
        db (Connection): Database connection that access to tasks and subjects.
    """
    db = sqlite3.connect(configuration.get_file_location("tasks.db"))
    return db


def get_cur():
    """This function returns the database cursor

    Returns:
        cur (Cursor): Database cursor that access to tasks and subjects.
    """
    cur = get_db().cursor()
    return cur


def exec(command: str):
    """This function executes a coomand in the database.

    Args:
        command (str): Query that needs to be executed on the database.

    Returns:
        cur (Cursor): Database cursor that access to tasks and subjects.
    """
    cur = get_db().cursor()
    cur.execute(command)
    get_db().commit()
    return cur


def save_task(task, username: str):
    """This function saves a task from a user into the database

    Args:
        task (Tarea): Tasks that would be added to the database.
        username(str): User owner of the task.

    Returns:
        cur (Cursor): Database cursor that access to tasks and subjects.
    """
    cur = get_db().cursor()
    checker = "select count(TarUID) from Tareas where TarUID = '" + task.id + "'"
    cur.execute(checker, ())
    exists = 0
    for row in cur.fetchall():
        exists = row[0]
    if exists == 0:
        logging.info("Ejecutando..." + str(exists))
        cur.execute(
            "INSERT INTO Tareas(TarUID, TarTitulo, TarDescripcion, TarFechaLim, Materias_idMaterias) VALUES (?, ?, ?, ?, ?);",
            (
                task.id,
                task.title,
                task.description.replace("\\n", "\n"),
                task.due_date,
                task.subject_id,
            ),
        )
        cur.connection.commit()
        tarea_id = get_task_id(task.id)
        usuario_id = get_user_id(username)
        cur.execute(
            "INSERT INTO TareasUsuarios(TarUsrEstado, idTareas, idUsuarios) VALUES (?,?,?);",
            ("N", tarea_id, usuario_id),
        )
    cur.connection.commit()
    return cur


def save_subject(subject):
    """This function saves a subject into the database

    Args:
        subject (Materia): Subject that would be added to the database.

    Returns:
        cur (Cursor): Database cursor that access to tasks and subjects.
    """
    query = "INSERT INTO Materias (MatNombre, MatCodigo, MatID) values (?, ?, ?);"
    cur = get_db().cursor()
    cur.execute(query, (subject.name, subject.codigo, subject.id))
    cur.connection.commit()
    return cur


def save_user(username: str):
    """This function saves a user into the database

    Args:
        username (str): User to be added into the database

    Returns:
        cur (Cursor): Database cursor that access to tasks and subjects.
    """
    print("Agregando usuario, " + username + "a la base de datos")
    query = "INSERT INTO Usuarios (UsrNombre) values (?);"
    cur = get_db().cursor()
    cur.execute(query, (username,))
    cur.connection.commit()
    return cur


def save_subject_id(subject):
    """This function saves the trello list ID into the database

    Args:
        subject (Materia): Subject that owns the ID that would be added to the database.

    """
    cur = get_db().cursor()
    cur.execute(
        "UPDATE Materias SET MatID = ? WHERE MatCodigo = ?;",
        (subject.id, subject.codigo),
    )
    cur.connection.commit()
    for row in cur.fetchall():
        logging.info("fila: " + str(row))
    cur.close()


def get_cards_from_db() -> list:
    """This function get all cards from Tareas table.

    Returns:
        cards (list): List contanining all cards from Tareas table.
    """
    cur = exec(
        "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Tareas';",
        get_cur(),
    )
    cards = []
    for row in cur.fetchall():
        cards.append(row[0])
    return cards


def get_subject_id(subject_code: str) -> str:
    """This function gets the subject ID from the database

    Args:
        subject_code (str): Subject code from the subject to get the ID.

    Returns:
        subject_id (str): Subject ID from the subject.
    """
    query = "select idMaterias from Materias where MatCodigo = '" + subject_code + "'"
    cur = get_db().cursor()
    cur.execute(query)
    subject_id = ""

    for row in cur.fetchall():
        subject_id = row[0]
    cur.connection.close()
    subject_id = str(subject_id)
    return subject_id


def get_task_id(task_uid: str) -> str:
    """This function gets the task ID from the database

    Args:
        task_uid (str): Task UID from the task to get the ID.

    Returns:
        task_id (str): Task ID from the task.
    """
    query = "select idTareas from Tareas where TarUID = '" + task_uid + "'"
    cur = get_db().cursor()
    cur.execute(query)

    task_id = ""
    for row in cur.fetchall():
        task_id = row[0]
    cur.connection.close()
    task_id = str(task_id)
    return task_id


def get_user_id(username: str) -> str:
    """This function gets the User ID from the database

    Args:
        username (str): Username to get his ID.

    Returns:
        idUsuarios (str): The user id from the database.
    """
    query = "select idUsuarios from Usuarios where UsrNombre = '" + username + "'"
    cur = get_db().cursor()
    cur.execute(query)

    user_id = ""
    for row in cur.fetchall():
        user_id = row[0]
    cur.connection.close()
    user_id = str(user_id)
    return user_id


def get_subject_name(subject_code: str):
    """This function gets the subject Name from the database

    Args:
        subject_code (str): Subject code for get the subject name.

    Returns:
        subject_name (str): The subject name from the subject code.
    """
    query = "select MatNombre from Materias where MatCodigo = '" + subject_code + "'"
    cur = get_db().cursor()
    cur.execute(query)
    subject_name = ""

    for row in cur.fetchall():
        subject_name = row[0]
    cur.connection.close()
    return subject_name


def add_task_tid(task_uid: str, task_tid: str, username: str):
    """This function adds the task trello ID into the database

    Args:
        task_uid (str): Task UID from ICS file.
        task_tid (str): New Task Trello ID from trello.
        username (str): Username from the user that owns the task

    Returns:
        cur (Cursor): Database cursor that access to tasks and subjects.
    """
    cur = get_db().cursor()
    task_id = get_task_id(task_uid)
    user_id = get_user_id(username)
    cur.execute(
        "UPDATE TareasUsuarios SET TarUsrTID = ?, TarUsrEstado = ? WHERE idUsuarios = ? AND idTareas = ?;",
        (task_tid, "E", user_id, task_id),
    )
    cur.connection.commit()
    return cur


def get_unsended_tasks(username: str) -> list:
    """This function gets all unsended tasks from the user.

    Args:
        username (str): Username from the user that owns the task

    Returns:
        tasks (list): Database cursor that access to tasks and subjects.
    """
    user_id = get_user_id(username)
    query = (
        "select TarUsrEstado, TarUID, TarTitulo, TarDescripcion, TarFechaLim, MatID from Materias, Tareas, TareasUsuarios where Tareas.Materias_idMaterias = Materias.idMaterias AND TareasUsuarios.TarUsrEstado = 'N' AND TareasUsuarios.idTareas = Tareas.idTareas AND TareasUsuarios.idUsuarios = '"
        + user_id
        + "';"
    )
    cur = get_db().cursor()
    cur.execute(query)
    tasks = []
    for row in cur.fetchall():
        tasks.append(TareaClass.Tarea(row[1], row[2], row[3], row[4], row[5]))
    cur.connection.close()
    return tasks


def check_no_subject_id(subject_code: str) -> str:
    """This function checks if the subject has an ID in the database.

    Args:
        subject_code (str): Subject code from the database to check if it has ID or not.

    Returns:
        result (str): Returns '0' if does not has the ID and '1' if it has it.
    """
    query = (
        "select count(MatCodigo) from Materias where MatCodigo='"
        + subject_code
        + '\'AND MatID="";'
    )
    cur = get_db().cursor()
    cur.execute(query)
    for row in cur.fetchall():
        result = row[0]
    cur.connection.close()
    return result


def check_user_existence(username: str):
    """This function checks if the username has an ID in the database.

    Args:
        username (str): username from the database to check if it has ID or not.

    Returns:
        result (str): Returns '0' if does not has the ID and '1' if it has it.
    """
    query = "select count(UsrNombre) from Usuarios where UsrNombre='" + username + "';"
    cur = get_db().cursor()
    cur.execute(query)
    for row in cur.fetchall():
        result = row[0]
    cur.connection.close()
    return result
