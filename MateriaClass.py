class Materia:
    def __init__(self, name, codigo, id=""):
        self.id = id
        self.name = name
        self.codigo = codigo

    def print(self):
        print(self.id, self.name, self.codigo)