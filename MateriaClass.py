class Materia:
    def __init__(self, id, name, codigo):
        self.id = id
        self.name = name
        self.codigo = codigo
    def print(self):
        print(self.id, self.name, self.codigo)
