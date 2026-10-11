from dati.creadati import crea_corsa

class ArchivioCorse:
    def __init__(self):
        self.elementi = {}

    def carica(self):

        self.elementi ["50"] = crea_corsa("50", "Corsa 50mm")
        self.elementi ["60"] = crea_corsa("60", "Corsa 60mm")
        self.elementi ["75"] = crea_corsa("75", "Corsa 75mm")
        self.elementi ["80"] = crea_corsa("80", "Corsa 80mm")
        self.elementi ["90"] = crea_corsa("90", "Corsa 90mm")
        self.elementi ["100"] = crea_corsa("100", "Corsa 100mm")
        self.elementi ["115"] = crea_corsa("115", "Corsa 100mm")
        self.elementi ["120"] = crea_corsa("120", "Corsa 120mm")
        self.elementi ["130"] = crea_corsa("130", "Corsa 130mm")
        self.elementi ["150"] = crea_corsa("150", "Corsa 150mm")
        self.elementi ["160"] = crea_corsa("160", "Corsa 160mm")
        self.elementi ["200"] = crea_corsa("200", "Corsa 200mm")
        self.elementi ["250"] = crea_corsa("250", "Corsa 250mm")
        self.elementi ["300"] = crea_corsa("300", "Corsa 300mm")
        self.elementi ["400"] = crea_corsa("400", "Corsa 400mm")
        self.elementi ["600"] = crea_corsa("600", "Corsa 600mm")

    def get_corsa(self, corsa):
        return self.elementi.get(corsa)

    def elenco(self):
        return self.elementi
