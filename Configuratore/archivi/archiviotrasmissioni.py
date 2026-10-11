from dati.creadati import crea_trasmissione

class ArchivioTrasmissioni:
    def __init__(self):
        self.elementi = {}

    def carica(self):

        self.elementi["catena_riduttore"] = crea_trasmissione("catena_riduttore","Trasmissione a catena")
        self.elementi["catena"] = crea_trasmissione("catena","Trasmissione a catena")
        self.elementi["cinghia"] = crea_trasmissione("cinghia","Trasmissione a cinghia dentata")
        self.elementi["poly_v"] = crea_trasmissione("poly_v","Trasmissione a cinghia poly-V")
        self.elementi["xxx"] = crea_trasmissione("xxx","Trasmissione da definire")

    def get_trasmissione(self, trasmissione):
        return self.elementi.get(trasmissione)
            
    def elenco(self):
        return self.elementi