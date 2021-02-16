from datetime import datetime
from polical import MateriaClass
from polical import connectSQLite


class Tarea:
    """Main class of PoliCal it manages the task its owner and its subject associated"""

    def __init__(
        self, id: str, title: str, description: str, due_date: datetime, subject_id: str
    ):
        """Class constructor

        Args:
            id (str): ID that comes from ICS file
            title (str): Title of the tasks
            description (str): Description of the task
            due_date (datetime): When is due to the task
            subject_id (str): Subject id that is associated to the task
        """
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.subject_id = subject_id
        self.subject = MateriaClass.Materia("Desconocido", subject_id)
        self.tid = None

    def print(self):
        """Prints a summary ofthe main elements of the task"""
        print(self.id, self.title, self.due_date, self.subject_id)

    def define_subject(self, subject: MateriaClass.Materia):
        """Defines a subject object for the task

        Args:
            subject (MateriaClass.Materia): [description]
        """
        self.subject = subject
        unknown_name = (
            str(self.subject.codigo)
            + ", registre esta materia usando /subject NOMBRE DE LA MATERIA (CODIGO)"
        )
        if self.subject.name == "Desconocido":
            temp_subject_name = connectSQLite.get_user_subject_name(
                str(self.subject.id), str(self.username)
            )
            self.subject.name = (
                temp_subject_name if temp_subject_name != None else unknown_name
            )

    def define_username(self, username: str):
        """Defines task owner username

        Args:
            username (str): The username of the user that owns the task
        """
        self.username = username

    def define_tid(self, tid: str):
        """Defines Trello o Telegram ID associated to this task

        Args:
            tid (str): Trello o Telegram ID associated to this task
        """
        self.tid = tid

    def summary(self):
        """Generate a Summary of the main elements of the task

        Returns:
            str: Summary of the task generaly for being sended as Telegram Message
        """
        summary = "*Título*: " + str(self.title)
        summary += "\n*Descripción*: " + str(self.description).replace(
            "_", "\_"
        ).replace("*", "\*").replace("`", "\`").replace("[", "\[")
        summary += "\n*Fecha de Entrega*: " + str(self.due_date)
        summary += "\n*Materia*: " + str(self.subject.name)
        return summary
