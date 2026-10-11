import copy

class Velocita:
    def __init__(self):
        self.codice = ""
        self.descrizione = ""

    def clona(self):
        return copy.copy(self)
        