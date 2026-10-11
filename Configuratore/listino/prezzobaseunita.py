from modelli.corsa import Corsa
from modelli.prodotto import Prodotto

class PrezzoBaseUnita:
    def __init__(self):
        self.prezzo = 0
        self.consegna = 0
        self.corsa = Corsa()
        self.prodotto = Prodotto()
                