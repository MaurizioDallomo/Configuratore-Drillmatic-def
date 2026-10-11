from dati.creadati import crea_motore

class ArchivioMotori:
    def __init__(self):
        self.elementi = {}

    def carica(self):
        
        self.elementi["203"] = crea_motore("203", "80", "80", "0,75kW", "2p")
        self.elementi["205"] = crea_motore("205", "90", "90", "1,5kW", "2p")
        self.elementi["207"] = crea_motore("207", "100", "100", "3kW", "2p")
        self.elementi["209"] = crea_motore("209", "132", "132", "5,5kW", "2p")
        self.elementi["210"] = crea_motore("210", "180", "180", "22kW", "2p")
        self.elementi["213"] = crea_motore("213", "132", "132", "7,5kW", "2p")
        self.elementi["303"] = crea_motore("303", "80", "80", "0,75kW", "2p", "autofrenante")
        self.elementi["403"] = crea_motore("403", "80", "80", "0,55kW", "4p")
        self.elementi["406"] = crea_motore("406", "90", "90", "1,5kW", "4p")
        self.elementi["407"] = crea_motore("407", "100", "100", "2,2kW", "4p")
        self.elementi["408"] = crea_motore("408", "100", "100", "3kW", "4p")
        self.elementi["410"] = crea_motore("410", "132", "132", "5,5kW", "4p")
        self.elementi["411"] = crea_motore("411", "180", "180", "18kW", "4p")
        self.elementi["412"] = crea_motore("412", "132", "132", "7,5kW", "4p")
        self.elementi["503"] = crea_motore("503", "80", "80", "0,55kW", "4p", "autofrenante")
        self.elementi["506"] = crea_motore("506", "90", "90", "1,5kW", "4p", "autofrenante")
        self.elementi["508"] = crea_motore("508", "100", "100", "3kW", "4p", "autofrenante")
        self.elementi["604"] = crea_motore("604", "80", "80", "0,55kW", "6p")
        self.elementi["606"] = crea_motore("606", "90", "90", "1,1kW", "6p")
        self.elementi["607"] = crea_motore("607", "100", "100", "1,5kW", "6p")
        self.elementi["609"] = crea_motore("609", "112", "112", "2,2kW", "6p")
        self.elementi["611"] = crea_motore("611", "132", "132", "4kW", "6p")
        self.elementi["612"] = crea_motore("612", "180", "180", "15kW", "6p")
        self.elementi["704"] = crea_motore("704", "80", "80", "0,55kW", "6p", "autofrenante")
        self.elementi["706"] = crea_motore("706", "90", "90", "1,1kW", "6p", "autofrenante")
        self.elementi["709"] = crea_motore("709", "112", "112", "2,2kW", "6p", "autofrenante")
        self.elementi["901"] = crea_motore("901", "80", "80", "0,8kW / 0,6kW", "2/4p")
        self.elementi["902"] = crea_motore("902", "80", "80", "0,55kW / 0,45kW", "4/6p")
        self.elementi["903"] = crea_motore("903", "90", "90", "1,3kW / 1,1kW", "2/4p")
        self.elementi["904"] = crea_motore("904", "90", "90", "1,1kW / 0,75kW", "4/6p")
        self.elementi["xxx"] = crea_motore("xxx", "", "", "", "")

    def get_motore(self, motore):
        return self.elementi.get(motore)
            
    def elenco(self):
        return self.elementi