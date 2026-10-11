from modelli.prodotto import Prodotto
from modelli.corsa import Corsa

class PrezzoBaseSlitta:
    def __init__(self):
        self.prezzo = 0
        self.consegna = 0
        self.corsa = Corsa()
        self.prodotto = Prodotto()
        