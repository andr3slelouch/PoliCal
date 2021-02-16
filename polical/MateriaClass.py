class Materia:
    """Class that stores subject attributes like code and id"""

    def __init__(self, name: str, codigo: str, id: str = ""):
        """Constructor of the class

        Args:
            name (str): Name of the Subject
            codigo (str): Code of the subject
            id (str, optional): Id of the subject in the database. Defaults to "".
        """
        self.id = id
        self.name = name
        self.codigo = codigo

    def print(self):
        """Prints a summary of the main attributes of the class"""
        print(self.id, self.name, self.codigo)