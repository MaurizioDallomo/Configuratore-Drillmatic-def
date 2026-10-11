class Descrizione:
    def __init__(self):
        self.codice = ""
        self.descrizione_base = ""

    def associa_descrizione(self, prodotto, descrizione_base_originale=None):
        descrizione_composta = ""
        match self.codice:
            case "capacita_foratura":
                descrizione_composta += f"{self.descrizione_base} {prodotto.capacita_foratura}"
            case "capacita_maschiatura":
                descrizione_composta += f"{self.descrizione_base}{prodotto.capacita_maschiatura}"
            case "spinta":
                descrizione_composta += f"{self.descrizione_base}{prodotto.spinta}"
            case "carico_assiale":
                descrizione_composta += f"{self.descrizione_base}{prodotto.carico_assiale}"
            case "concentricita":
                descrizione_composta += f"{self.descrizione_base}{prodotto.concentricita}"
            case "vite":
                if descrizione_base_originale is not None:
                    descrizione_composta += f"{self.descrizione_base}"
                else:
                    descrizione_composta += f"{self.descrizione_base}{prodotto.vite}"
            case "cilindro_pneumatico":
                descrizione_composta += f"{self.descrizione_base}{prodotto.cilindro_pneumatico}"
            case "cilindro_idraulico":
                descrizione_composta += f"{self.descrizione_base}{prodotto.cilindro_idraulico}"
            case _:
                descrizione_composta += f"{self.descrizione_base}"
        return descrizione_composta
    
                
