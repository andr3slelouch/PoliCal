class Tarea:
    def __init__(self, id, title, description, due_date, subject_id):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.subject_id = subject_id

    def print(self):
        print(self.id, self.title, self.due_date, self.subject_id)
