from modelli.elencovariabili import ElencoVariabili
from modelli.famiglia import Famiglia

class MacroCategoria:
    def __init__(self):
        self.nome = ""
        self.famiglie = {}
        self.tipo = None
        self.layout_variabili = ElencoVariabili()

    def aggiungi_famiglia(self, famiglia: Famiglia):
        self.famiglie[famiglia.codice] = famiglia
        famiglia.macro_categoria = self

    def get_famiglia(self, codice):
        return self.famiglie.get(codice)

