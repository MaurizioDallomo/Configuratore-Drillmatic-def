from dati.creadati import crea_velocita

class ArchivioVelocita:
    def __init__(self):
        self.elementi = {}

    def carica(self):
        
        self.elementi["A2"] = crea_velocita("A2", "Velocità di rotazione 100rpm")
        self.elementi["A"] = crea_velocita("A", "Velocità di rotazione 160rpm")
        self.elementi["B"] = crea_velocita("B", "Velocità di rotazione 200rpm")
        self.elementi["C"] = crea_velocita("C", "Velocità di rotazione 250rpm")
        self.elementi["D"] = crea_velocita("D", "Velocità di rotazione 300rpm")
        self.elementi["E"] = crea_velocita("E", "Velocità di rotazione 400rpm")
        self.elementi["F"] = crea_velocita("F", "Velocità di rotazione 500rpm")
        self.elementi["G"] = crea_velocita("G", "Velocità di rotazione 600rpm")
        self.elementi["H"] = crea_velocita("H", "Velocità di rotazione 800rpm")
        self.elementi["I"] = crea_velocita("I", "Velocità di rotazione 1000rpm")
        self.elementi["J"] = crea_velocita("J", "Velocità di rotazione 1200rpm")
        self.elementi["K"] = crea_velocita("K", "Velocità di rotazione 1500rpm")
        self.elementi["L"] = crea_velocita("L", "Velocità di rotazione 1800rpm")
        self.elementi["M"] = crea_velocita("M", "Velocità di rotazione 2000rpm")
        self.elementi["N"] = crea_velocita("N", "Velocità di rotazione 2400rpm")
        self.elementi["O"] = crea_velocita("O", "Velocità di rotazione 3000rpm")
        self.elementi["P"] = crea_velocita("P", "Velocità di rotazione 3600rpm")
        self.elementi["Q"] = crea_velocita("Q", "Velocità di rotazione 4000rpm")
        self.elementi["R"] = crea_velocita("R", "Velocità di rotazione 4500rpm")
        self.elementi["S"] = crea_velocita("S", "Velocità di rotazione 5400rpm")
        self.elementi["T"] = crea_velocita("T", "Velocità di rotazione 6400rpm")
        self.elementi["U"] = crea_velocita("U", "Velocità di rotazione 7500rpm")
        self.elementi["V"] = crea_velocita("V", "Velocità di rotazione 8400rpm")
        self.elementi["Z1"] = crea_velocita("Z1", "Velocità di rotazione 750rpm / 1200rpm")
        self.elementi["Z2"] = crea_velocita("Z2", "Velocità di rotazione 1200rpm / 2400rpm")
        self.elementi["Z3"] = crea_velocita("Z3", "Velocità di rotazione 2000rpm / 4000 rpm")
        self.elementi["xxx"] = crea_velocita("xxx", "Velocità di rotazione da definire")

    def get_velocita(self, velocita):
        return self.elementi.get(velocita)
            
    def elenco(self):
        return self.elementi