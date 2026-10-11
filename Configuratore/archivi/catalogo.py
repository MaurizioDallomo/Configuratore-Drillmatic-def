from archivi.archiviomacrocategorie import ArchivioMacrocategorie
from archivi.archivioprodotti import ArchivioProdotti
from archivi.archiviofamiglie import ArchivioFamiglie
from listino.listino import Listino
from archivi.archiviocorse import ArchivioCorse
from archivi.archiviomandrini import ArchivioMandrini
from archivi.archiviomotori import ArchivioMotori
from archivi.archiviomotorimaggiorati import ArchivioMotoriMaggiorati
from archivi.archiviocuscinetti import ArchivioCuscinetti
from archivi.archiviovelocita import ArchivioVelocita
from archivi.archiviotrasmissioni import ArchivioTrasmissioni
from archivi.archiviodescrizioni import ArchivioDescrizioni
from archivi.archivioopzioni import ArchivioOpzioni
from archivi.archiviolistini import ArchivioListini
from archivi.archivioaccessori import ArchivioAccessori

class Catalogo:
    def __init__(self):
        self.macrocategorie = ArchivioMacrocategorie()
        self.prodotti = ArchivioProdotti()
        self.famiglie = ArchivioFamiglie()
        self.listini = ArchivioListini()
        self.corse = ArchivioCorse()
        self.mandrini = ArchivioMandrini()
        self.motori = ArchivioMotori()
        self.motori_maggiorati = ArchivioMotoriMaggiorati()
        self.cuscinetti = ArchivioCuscinetti()
        self.velocita = ArchivioVelocita()
        self.trasmissioni = ArchivioTrasmissioni()
        self.descrizioni = ArchivioDescrizioni()
        self.opzioni = ArchivioOpzioni()
        self.accessori = ArchivioAccessori()
        self.listino = Listino()

    def carica(self):
       
        self.corse.carica()
        self.cuscinetti.carica()
        self.descrizioni.carica()
        self.mandrini.carica()
        self.motori.carica()
        self.motori_maggiorati.carica()
        self.opzioni.carica()
        self.trasmissioni.carica()
        self.velocita.carica()
        self.accessori.carica()
        self.famiglie.carica(catalogo=self)
        self.prodotti.carica(catalogo=self)
        self.macrocategorie.carica(catalogo=self)
        self.listino.carica(catalogo=self)
        


