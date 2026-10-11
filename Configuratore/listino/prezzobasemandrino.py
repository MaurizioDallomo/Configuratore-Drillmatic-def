from modelli.prodotto import Prodotto
from modelli.cuscinetto import Cuscinetto

class PrezzoBaseMandrino:
    def __init__(self):
        self.gr_motore = 0
        self.prezzo = 0
        self.consegna = 0
        self.prodotto = Prodotto()
        self.cuscinetto = Cuscinetto()
        
