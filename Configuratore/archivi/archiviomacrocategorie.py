from modelli.macrocategoria import MacroCategoria
from modelli.enums import MacroCategorie, TipovariabileObbligatoria

class ArchivioMacrocategorie:
    def __init__(self):
        self.elementi = {}

    def carica(self, catalogo):

        mc = MacroCategoria()
        
        mc.nome = "unita"
        mc.tipo = MacroCategorie.Unita
        mc.aggiungi_famiglia(catalogo.famiglie.get_famiglia("DXP"))
        mc.aggiungi_famiglia(catalogo.famiglie.get_famiglia("DXE"))
        mc.aggiungi_famiglia(catalogo.famiglie.get_famiglia("TX"))
        mc.aggiungi_famiglia(catalogo.famiglie.get_famiglia("DTX"))
        mc.layout_variabili.opzione1 = TipovariabileObbligatoria.Corse
        mc.layout_variabili.opzione2 = TipovariabileObbligatoria.Mandrini
        mc.layout_variabili.opzione3 = TipovariabileObbligatoria.Motori
        mc.layout_variabili.opzione4 = TipovariabileObbligatoria.Velocita

        self.elementi[mc.nome] = mc

        mc = MacroCategoria()

        mc.nome = "mandrino"
        mc.tipo = MacroCategorie.Mandrino
        mc.aggiungi_famiglia(catalogo.famiglie.get_famiglia("DX"))
        mc.layout_variabili.opzione1 = TipovariabileObbligatoria.Velocita
        mc.layout_variabili.opzione2 = TipovariabileObbligatoria.Motori
        mc.layout_variabili.opzione3 = TipovariabileObbligatoria.Mandrini
        mc.layout_variabili.opzione4 = TipovariabileObbligatoria.Cuscinetti

        self.elementi[mc.nome] = mc

        mc = MacroCategoria()

        mc.nome = "slitta"
        mc.tipo = MacroCategorie.Slitta
        mc.layout_variabili.opzione1 = TipovariabileObbligatoria.Corse
        mc.aggiungi_famiglia(catalogo.famiglie.get_famiglia("EX"))
        mc.aggiungi_famiglia(catalogo.famiglie.get_famiglia("HX"))

        self.elementi[mc.nome] = mc

    def get_macrocategoria(self, macrocategoria):
        return self.elementi.get(macrocategoria)
            
    def elenco(self):
        return self.elementi

    