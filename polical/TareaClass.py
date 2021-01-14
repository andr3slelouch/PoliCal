from datetime import datetime
from polical import MateriaClass


class Tarea:
    def __init__(self, id, title, description, due_date, subject_id):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.subject_id = subject_id
        self.subject = MateriaClass.Materia("Desconocido", subject_id)

    def print(self):
        print(self.id, self.title, self.due_date, self.subject_id)

    def define_subject(self, subject):
        self.subject = subject

    def summary(self):
        summary = "*Titulo*: " + str(self.title)
        summary += "\n*Descripción*: " + str(self.description).replace(
            "_", "\_"
        ).replace("*", "\*").replace("`", "\`").replace("[", "\[")
        summary += "\n*Fecha de Entrega*: " + str(self.due_date)
        if self.subject.name == "Desconocido":
            summary += (
                "\n*Materia*: "
                + str(self.subject.codigo)
                + " ,registre esta materia usando /subject NOMBRE DE LA MATERIA (CODIGO)"
            )
        else:
            summary += "\n*Materia*: " + str(self.subject.name)
        return summary
