import copy

class Motore:
    def __init__(self):
        self.codice = ""
        self.grandezza = ""
        self.grandezza_descr = ""
        self.potenza = ""
        self.poli = ""
        self.freno = ""
        self.descrizione = ""
        self.testo_agg = ""

    def dati_motore(self):
        if not self.freno == "":
            caratteristiche = "Motore " + self.testo_agg + " grandezza " + self.grandezza_descr + " " + self.potenza + " " + self.poli + \
            self.freno
        else:
            caratteristiche = "Motore " + self.testo_agg + " grandezza " + self.grandezza_descr + " " + self.potenza + " " + self.poli

        return caratteristiche

    def clona(self):
        return copy.copy(self)
    
            
            