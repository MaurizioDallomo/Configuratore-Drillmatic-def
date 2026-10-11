from modelli.preventivo_riga import Preventivo_riga
from modelli.cliente import Cliente

class Preventivo:
    def __init__(self):
        self.numero = 0
        self.anno = 0
        self.data_creazione = ""
        self.cliente = Cliente()
        self.consegna = ""
        self.imballo = ""
        self.validita = ""
        self.revisione = 0
        self.righe = {}

    def aggiungi_riga_preventivo(self, riga):
        self.righe[riga.numero_riga] = riga
        riga.preventivo = self
        
    def get_riga(self, numero_riga):
        return self.righe.get(numero_riga)

