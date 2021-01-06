import sqlite3
from mysql.connector import MySQLConnection, Error
from polical import TareaClass
from polical import configuration

import logging


def get_db():
    """This function returns the database connection. Selects between sqlite3 or mysql

    Returns:
        db (Connection): Database connection that access to tasks and subjects.
    """
    if (
        configuration.get_preferred_dbms(
            configuration.get_file_location("db_selector.yaml")
        )
        == "default"
    ):
        db = sqlite3.connect(configuration.get_file_location("tasks.db"))
        return db
    elif (
        configuration.get_preferred_dbms(
            configuration.get_file_location("db_selector.yaml")
        )
        == "mysql"
    ):
        mysql_credentials = configuration.get_mysql_credentials(
            configuration.get_file_location("db_selector.yaml")
        )
        if mysql_credentials:
            db = MySQLConnection(
                host=mysql_credentials["host"],
                database=mysql_credentials["database"],
                user=mysql_credentials["user"],
                password=mysql_credentials["password"],
            )
            return db


def get_cur():
    """This function returns the database cursor

    Returns:
        cur (Cursor): Database cursor that access to tasks and subjects.
    """
    conn = get_db()
    cur = conn.cursor()
    return cur


def exec(command: str):
    """This function executes a coomand in the database.

    Args:
        command (str): Query that needs to be executed on the database.

    Returns:
        cur (Cursor): Database cursor that access to tasks and subjects.
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute(command)
    conn.commit()
    return cur


def save_task(task):
    """This function saves a task into the database

    Args:
        task (Tarea): Tasks that would be added to the database.
    """

    conn = get_db()
    cur = conn.cursor()
    query = configuration.prepare_mysql_query(
        "INSERT INTO Tareas(TarUID, TarTitulo, TarDescripcion, TarFechaLim, Materias_idMaterias) VALUES (?, ?, ?, ?, ?);"
    )
    if not check_task_existence(task):
        cur.execute(
            query,
            (
                task.id,
                task.title,
                task.description.replace("\\n", "\n"),
                task.due_date,
                task.subject_id,
            ),
        )
        conn.commit()
    conn.close()


def save_user_task(task, username: str):
    """This function saves a task from a user into the database

    Args:
        task (Tarea): Tasks that would be added to the database.
        username(str): User owner of the task.
    """
    save_task(task)
    conn = get_db()
    cur = conn.cursor()
    tarea_id = get_task_id(task.id)
    usuario_id = get_user_id(username)
    query = configuration.prepare_mysql_query(
        "INSERT INTO TareasUsuarios(TarUsrEstado, idTareas, idUsuarios) VALUES (?,?,?);"
    )
    if not check_user_task_existence(task, username):
        cur.execute(
            query,
            ("N", tarea_id, usuario_id),
        )
        conn.commit()
    conn.close()


def check_user_task_existence(task, username: str):
    """This function checks if a task exists in the database

    Args:
        task (Tarea): Tasks that would be added to the database.
        username(str): User owner of the task.
    """
    conn = get_db()
    cur = conn.cursor()
    tarea_id = get_task_id(task.id)
    usuario_id = get_user_id(username)
    checker = (
        "select count(TarUsrEstado) from TareasUsuarios where idTareas = '"
        + tarea_id
        + "' and idUsuarios = '"
        + usuario_id
        + "'"
    )
    cur.execute(checker, ())
    exists = 0
    for row in cur.fetchall():
        exists = row[0]
    if exists == 0:
        return False
    else:
        return True


def check_task_existence(task) -> bool:
    """This function checks if a task exists in the database

    Args:
        task (Tarea): Tasks that would be added to the database.
    """
    conn = get_db()
    cur = conn.cursor()
    checker = "select count(TarUID) from Tareas where TarUID = '" + task.id + "'"
    cur.execute(checker, ())
    exists = 0
    for row in cur.fetchall():
        exists = row[0]
    if exists == 0:
        return False
    else:
        return True


def save_subject(subject):
    """This function saves a subject into the database

    Args:
        subject (Materia): Subject that would be added to the database.

    Returns:
        cur (Cursor): Database cursor that access to tasks and subjects.
    """
    query = configuration.prepare_mysql_query(
        "INSERT INTO Materias (MatNombre, MatCodigo) values (?, ?);"
    )
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, (subject.name, subject.codigo))
    conn.commit()
    return cur


def save_user_subject(subject, username: str):
    """This function saves a subject and associates to a user into the database

    Args:
        subject (Materia): Subject that would be added to the database.
        username(str): User owner of the task.
    Returns:
        cur (Cursor): Database cursor that access to tasks and subjects.
    """
    materia_id = get_subject_id(subject.codigo)
    usuario_id = get_user_id(username)
    print(subject.codigo, username, materia_id, usuario_id)
    if not check_user_subject_existence(materia_id, username):
        query = configuration.prepare_mysql_query(
            "INSERT INTO MateriasUsuarios (idMateria, idUsuario, MatID) values (?, ?, ?);"
        )
        conn = get_db()
        cur = conn.cursor()
        cur.execute(query, (materia_id, usuario_id, subject.id))
        conn.commit()
        conn.close()
    else:
        query = configuration.prepare_mysql_query(
            "UPDATE MateriasUsuarios SET MatID = ? WHERE idMateria = ? AND idUsuario = ?;"
        )
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            query,
            (subject.id, materia_id, usuario_id),
        )
        conn.commit()
        conn.close()


def check_user_subject_existence(subject_id, username: str):
    """This function checks if a subject exists in the database

    Args:
        task (Tarea): Tasks that would be added to the database.
        username(str): User owner of the task.
    """
    conn = get_db()
    cur = conn.cursor()
    usuario_id = get_user_id(username)
    checker = (
        "select count(MatID) from MateriasUsuarios where idMateria = '"
        + subject_id
        + "' and idUsuario = '"
        + usuario_id
        + "'"
    )
    cur.execute(checker, ())
    exists = 0
    for row in cur.fetchall():
        exists = row[0]
    if exists == 0:
        return False
    else:
        return True


def save_user(username: str):
    """This function saves a user into the database

    Args:
        username (str): User to be added into the database

    Returns:
        cur (Cursor): Database cursor that access to tasks and subjects.
    """
    query = configuration.prepare_mysql_query(
        "INSERT INTO Usuarios(UsrNombre) VALUES (?)"
    )
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, (username,))
    conn.commit()
    return cur


def save_subject_id(subject):
    """DEPRECATED This function saves the trello list ID into the database

    Args:
        subject (Materia): Subject that owns the ID that would be added to the database.

    """
    query = configuration.prepare_mysql_query(
        "UPDATE Materias SET MatID = ? WHERE MatCodigo = ?;"
    )
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        query,
        (subject.id, subject.codigo),
    )
    conn.commit()
    conn.close()


def get_subject_id(subject_code: str) -> str:
    """This function gets the subject ID from the database

    Args:
        subject_code (str): Subject code from the subject to get the ID.

    Returns:
        subject_id (str): Subject ID from the subject.
    """
    query = "select idMaterias from Materias where MatCodigo = '" + subject_code + "'"
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query)
    subject_id = ""

    for row in cur.fetchall():
        subject_id = row[0]
    conn.close()
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
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query)

    task_id = ""
    for row in cur.fetchall():
        task_id = row[0]
    conn.close()
    task_id = str(task_id)
    return task_id


def get_user_id(username: str) -> str:
    """This function gets the User ID from the database

    Args:
        username (str): Username to get his ID.

    Returns:
        idUsuarios (str): The user id from the database.
    """
    username = str(username)
    if check_user_existence(username):
        save_user(username)
    query = "select idUsuarios from Usuarios where UsrNombre = '" + username + "'"
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query)

    user_id = ""
    for row in cur.fetchall():
        user_id = row[0]
    conn.close()
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
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query)
    subject_name = ""

    for row in cur.fetchall():
        subject_name = row[0]
    conn.close()
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
    query = configuration.prepare_mysql_query(
        "UPDATE TareasUsuarios SET TarUsrTID = ?, TarUsrEstado = ? WHERE idUsuarios = ? AND idTareas = ?;"
    )
    conn = get_db()
    cur = conn.cursor()
    task_id = get_task_id(task_uid)
    user_id = get_user_id(username)
    cur.execute(
        query,
        (task_tid, "E", user_id, task_id),
    )
    conn.commit()
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
        "select TarUsrEstado, TarUID, TarTitulo, TarDescripcion, TarFechaLim, MateriasUsuarios.MatID "
        + "from Materias, Tareas, TareasUsuarios, MateriasUsuarios "
        + "where Tareas.Materias_idMaterias = Materias.idMaterias AND "
        + "TareasUsuarios.TarUsrEstado = 'N' AND "
        + "TareasUsuarios.idTareas = Tareas.idTareas AND "
        + "MateriasUsuarios.idMateria = Materias.idMaterias AND "
        + "MateriasUsuarios.idUsuario = TareasUsuarios.idUsuarios AND "
        + "TareasUsuarios.idUsuarios = '"
        + user_id
        + "';"
    )
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query)
    tasks = []
    for row in cur.fetchall():
        tasks.append(TareaClass.Tarea(row[1], row[2], row[3], row[4], row[5]))
    conn.close()
    return tasks


def check_no_subject_id(subject_code: str, username: str) -> bool:
    """This function checks if the subject code is registered and has an ID in the database.

    Args:
        subject_code (str): Subject code from the database to check if it has ID or not.

    Returns:
        (bool): Returns 'False' if does not has the ID and 'True' if it has it.
    """
    usuario_id = get_user_id(username)
    query = (
        "select count(MatCodigo) from Materias, MateriasUsuarios "
        + "where MatCodigo='"
        + subject_code
        + "'AND "
        + "Materias.idMaterias = MateriasUsuarios.idMateria AND "
        + "MateriasUsuarios.MatID='' AND "
        + "MateriasUsuarios.idUsuario='"
        + usuario_id
        + "';"
    )
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query)
    for row in cur.fetchall():
        result = row[0]
    conn.close()
    if result == 0:
        return False
    else:
        return True


def check_user_existence(username: str):
    """This function checks if the username has an ID in the database.

    Args:
        username (str): username from the database to check if it has ID or not.

    Returns:
        result (str): Returns '0' if does not has the ID and '1' if it has it.
    """
    query = "select count(UsrNombre) from Usuarios where UsrNombre='" + username + "';"
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query)
    for row in cur.fetchall():
        result = row[0]
    conn.close()
    if result:
        return True
    else:
        return False
