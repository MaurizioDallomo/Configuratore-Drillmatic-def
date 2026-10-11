class Famiglia:
    def __init__(self):
        self.codice = ""
        self.descrizione_base = ""
        self.opzioni = {}
        self.descrizioni = {}
        self.macro_categoria: 'MacroCategoria' = None

    def aggiungi_opzione(self, opzione):
        self.opzioni[opzione.codice] = opzione

    def aggiungi_descrizione(self, descrizione):
        self.descrizioni[descrizione.codice] = descrizione

    def get_opzione(self, codice):
        return self.opzioni.get(codice)

    def get_descrizione(self, codice):
        return self.descrizioni.get(codice)

    def numero_opzioni(self):
        return len(self.opzioni)

    def numero_descrizioni(self):
        return len(self.descrizioni)

    