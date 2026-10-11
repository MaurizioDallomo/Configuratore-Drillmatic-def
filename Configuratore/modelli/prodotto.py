from modelli.famiglia import Famiglia
from modelli.motorizzazione import Motorizzazione
from modelli.corsa import Corsa
from modelli.mandrino import Mandrino
from modelli.motore import Motore
from modelli.velocita import Velocita
from modelli.cuscinetto import Cuscinetto
from modelli.opzione import Opzione
from modelli.descrizione import Descrizione

class Prodotto:
    def __init__(self):
        self.codice = ""
        self.capacita_foratura = ""
        self.capacita_maschiatura = ""
        self.spinta = ""
        self.carico_assiale = ""
        self.concentricita = ""
        self.vite = ""
        self.cilindro_pneumatico = ""
        self.cilindro_idraulico = ""
        self.max_taglia_motore = ""
        self.opzioni_extra = {}
        self.corse = {}
        self.mandrini = {}
        self.cuscinetti = {}
        self.motorizzazioni = {}
        self.famiglia = Famiglia()

    def aggiungi_opzione_extra(self, opzione):
        self.opzioni_extra[opzione.codice] = opzione

    def aggiungi_corsa(self, corsa):
        self.corse[corsa.codice] = corsa

    def aggiungi_mandrino(self, mandrino):
        self.mandrini[mandrino.codice] = mandrino

    def aggiungi_cuscinetto(self, cuscinetto):
        self.cuscinetti[cuscinetto.codice] = cuscinetto

    def aggiungi_motorizzazione(self, motorizzazione):
        self.motorizzazioni[f"{motorizzazione.motore} | {motorizzazione.velocita} | {motorizzazione.trasmissione}"] = motorizzazione

    def get_opzione_extra(self, codice):
        return self.opzioni_extra.get(codice)

    def get_corsa(self, codice):
        return self.corse.get(codice)

    def get_mandrino(self, codice):
        return self.mandrini.get(codice)

    def get_cuscinetto(self, codice):
        return self.cuscinetti.get(codice)

    def get_motorizzazione(self, codice):
        return self.motorizzazioni.get(codice)

    def opzioni_totali(self) -> dict:
        return self.opzioni_extra | self.famiglia.opzioni

    def descrizioni(self, descrizione_base_originale=None) -> list:
        lista_descrizioni = []
        for d in self.famiglia.descrizioni.values():
            lista_descrizioni.append(d.associa_descrizione(self, descrizione_base_originale))
        return lista_descrizioni
    
    def motori(self, catalogo):
        mot = {}
        for m in self.motorizzazioni.values():
            if m.motore.codice not in mot:
                mot[m.motore.codice] = m.motore
        mot["xxx"] = catalogo.motori.get_motore("xxx")
        return mot

    def motori_selezionabili(self, catalogo, velocita_selezionata):
        mot = {}
        for m in self.motorizzazioni.values():
            if m.velocita.codice == velocita_selezionata:
                if m.motore.codice not in mot:
                    mot[m.motore.codice] = m.motore
        mot["xxx"] = catalogo.motori.get_motore("xxx")
        return mot

    def velocita(self, catalogo):
        vel = {}
        for v in self.motorizzazioni.values():
            if v.velocita.codice not in vel:
                vel[v.velocita.codice] = v.velocita
        vel["xxx"] = catalogo.velocita.get_velocita("xxx")
        return vel

    def velocita_selezionabili(self, catalogo, motore_selezionato):
        vel = {}
        for v in self.motorizzazioni.values():
            if v.motore.codice == motore_selezionato:
                if v.velocita.codice not in vel:
                    vel[v.velocita.codice] = v.velocita
        vel["xxx"] = catalogo.velocita.get_velocita("xxx")
        return vel

    def velocita_selezionabili_da_taglia(self, catalogo, taglia):
        vel = {}
        for v in self.motorizzazioni.values():
            if v.motore.grandezza == taglia:
                if v.velocita.codice not in vel:
                    vel[v.velocita.codice] = v.velocita
        vel["xxx"] = catalogo.velocita.get_velocita("xxx")
        return vel

