import logging
logging.basicConfig(filename='Running.log',level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


class Materia:
    def __init__(self, name, codigo, id=""):
        self.id = id
        self.name = name
        self.codigo = codigo

    def print(self):
        logging.info(self.id, self.name, self.codigo)
