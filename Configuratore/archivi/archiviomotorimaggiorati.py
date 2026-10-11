from dati.creadati import crea_motore

class ArchivioMotoriMaggiorati:
    def __init__(self):
        self.elementi = {}

    def carica(self):
        
        self.elementi["80MB2"] = crea_motore("80MB2", "80", "80", "0,75kW", "2p")
        self.elementi["80ME4"] = crea_motore("80ME4", "80", "80", "0,75kW", "4p")
        self.elementi["90LD6"] = crea_motore("90LD6", "90", "90", "0,75kW", "6p")
        self.elementi["80MC2"] = crea_motore("80MC2", "80", "80", "1,1kW", "2p")
        self.elementi["90LC4"] = crea_motore("90LC4", "90", "90", "1,1kW", "4p")
        self.elementi["100LE6"] = crea_motore("100LE6", "100", "100", "1,1kW", "6p")
        self.elementi["90LB2"] = crea_motore("90LB2", "90", "90", "1,5kW", "2p")
        self.elementi["90LD4"] = crea_motore("90LD4", "90", "90", "1,5kW", "4p")
        self.elementi["100LF6"] = crea_motore("100LF6", "100", "100", "1,5kW", "6p")
        self.elementi["90LC2"] = crea_motore("90LC2", "90", "90", "2,2kW", "2p")
        self.elementi["100LE4"] = crea_motore("100LE4", "100", "100", "2,2kW", "4p")
        self.elementi["112MC6"] = crea_motore("112MC6", "112", "112", "2,2kW", "6p")
        self.elementi["90LD2"] = crea_motore("90LD2", "90", "90", "2,75kW", "2p")
        self.elementi["100LC2"] = crea_motore("100LC2", "100", "100", "3kW", "2p")
        self.elementi["100LF4"] = crea_motore("100LF4", "100", "100", "3kW", "4p")
        self.elementi["132MC6"] = crea_motore("132MC6", "132", "132", "3kW", "6p")        
        self.elementi["112MB2"] = crea_motore("112MB2", "112", "112", "4kW", "2p")
        self.elementi["100LD2"] = crea_motore("100LD2", "100", "100", "4kW", "2p")
        self.elementi["112MB4"] = crea_motore("112MB4", "112", "112", "4kW", "4p")
        self.elementi["132MD6"] = crea_motore("132MD6", "132", "132", "4kW", "6p")        
        self.elementi["132SB2"] = crea_motore("132SB2", "132", "132", "5,5kW", "2p")
        self.elementi["112MC2"] = crea_motore("112MC2", "112", "112", "5,5kW", "2p")
        self.elementi["132MB4"] = crea_motore("132MB4", "132", "132", "5,5kW", "4p")
        self.elementi["112MC4"] = crea_motore("112MC4", "112", "112", "5,5kW", "4p")
        self.elementi["132ME6"] = crea_motore("132ME6", "132", "132", "5,5kW", "6p")
        self.elementi["132SC2"] = crea_motore("132SC2", "132", "132", "7,5kW", "2p")
        self.elementi["132MC4"] = crea_motore("132MC4", "132", "132", "7,5kW", "4p")     
        self.elementi["160MLA6"] = crea_motore("160MLA6", "160", "160", "7,5kW", "6p")     
        self.elementi["132SD2"] = crea_motore("132SD2", "132", "132", "9,2kW", "2p")
        self.elementi["132MD4"] = crea_motore("132MD4", "132", "132", "9,2kW", "4p")
        self.elementi["160MLA2"] = crea_motore("160MLA2", "160", "160", "11kW", "2p")
        self.elementi["132SME2"] = crea_motore("132SME2", "132", "132", "11kW", "2p")
        self.elementi["160MLA4"] = crea_motore("160MLA4", "160", "160", "11kW", "4p")
        self.elementi["132SME4"] = crea_motore("132SME4", "132", "132", "11kW", "4p")
        self.elementi["160MLB6"] = crea_motore("160MLB6", "160", "160", "11kW", "6p")       
        self.elementi["132SMF2"] = crea_motore("132SMF2", "132", "132", "15kW", "2p")
        self.elementi["160MLB4"] = crea_motore("160MLB4", "160", "160", "15kW", "4p")
        self.elementi["132SMF4"] = crea_motore("132SMF4", "132", "132", "15kW", "4p")
        self.elementi["160MLB2"] = crea_motore("160MLB2", "160", "160", "15W", "2p")
        self.elementi["180MLA6"] = crea_motore("180MLA6", "180", "180", "15kW", "6p")        
        self.elementi["160MLC2"] = crea_motore("160MLC2", "160", "160", "18,5W", "2p")
        self.elementi["180MLA4"] = crea_motore("180MLA4", "180", "180", "18,5kW", "4p")
        self.elementi["160MLC4"] = crea_motore("160MLC4", "160", "160", "18,5kW", "4p")
        self.elementi["180MLB6"] = crea_motore("180MLB6", "180", "180", "18,5kW", "6p") 
        self.elementi["180MLA2"] = crea_motore("180MLA2", "180", "180", "22kW", "2p")
        self.elementi["160MLD2"] = crea_motore("160MLD2", "160", "160", "22kW", "2p")
        self.elementi["180MLB4"] = crea_motore("180MLB4", "180", "180", "22kW", "4p")
        self.elementi["180MLC4"] = crea_motore("180MLC4", "180", "180", "28W", "4p")
        self.elementi["180MLB2"] = crea_motore("180MLB2", "180", "180", "30kW", "2p")
        self.elementi["180MLC2"] = crea_motore("180MLC2", "180", "180", "37kW", "2p")

    def get_motore(self, motore):
        return self.elementi.get(motore)
            
    def elenco(self):
        return self.elementi