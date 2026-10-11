from dati.creadati import crea_cuscinetto

class ArchivioCuscinetti:
    def __init__(self):
        self.elementi = {}

    def carica(self):

        self.elementi["RC"] = crea_cuscinetto("RC", "Cuscinetti a rulli conici")
        self.elementi["CO"] = crea_cuscinetto("CO", "Cuscinetti a contatto obliquo precaricati")

    def get_cuscinetto(self, cuscinetto):
            return self.elementi.get(cuscinetto)
    
    def elenco(self):
        return self.elementi