from dati.creadati import crea_accessorio

class ArchivioAccessori:
    def __init__(self):
        self.elementi = {}

    def carica(self):
        self.elementi["D0801F60"] = crea_accessorio("D0801F60", "F60", 0, 320, "Base")
        self.elementi["D0801F85"] = crea_accessorio("D0801F85", "F85", 0, 430, "Base")

        self.elementi["DA102-HF050"] = crea_accessorio("DA102-HF050", "Freno idraulico corsa 50mm", 0, 480, "Freno")
        self.elementi["DA102-HF075"] = crea_accessorio("DA102-HF075", "Freno idraulico corsa 75mm", 0, 530, "Freno")
        self.elementi["DA102-HF100"] = crea_accessorio("DA102-HF100", "Freno idraulico corsa 100mm", 0, 580, "Freno")

        self.elementi["F.KD50"] = crea_accessorio("F.KD50", "Dispositivo scarico trucioli corsa 50mm", 4, 700, "Accessorio")
        self.elementi["F.KD75"] = crea_accessorio("F.KD75", "Dispositivo scarico trucioli corsa 75mm", 4, 800, "Accessorio")
        self.elementi["F.KD100"] = crea_accessorio("F.KD100", "Dispositivo scarico trucioli corsa 100mm", 4, 900, "Accessorio")
        self.elementi["F.KD100.24"] = crea_accessorio("F.KD100.24", "Dispositivo scarico trucioli corsa 100mm", 4, 900, "Accessorio")

        self.elementi["D0441-0.350D"] = crea_accessorio("D0441-0.350D", "Patrona std corsa 50mm passo 0.35", 1, 380, "Patrona")
        self.elementi["D0441-0.400D"] = crea_accessorio("D0441-0.400D", "Patrona std corsa 50mm passo 0.40", 1, 380, "Patrona")
        self.elementi["D0441-0.450D"] = crea_accessorio("D0441-0.450D", "Patrona std corsa 50mm passo 0.45", 1, 380, "Patrona")
        self.elementi["D0441-0.500D"] = crea_accessorio("D0441-0.500D", "Patrona std corsa 50mm passo 0.50", 1, 380, "Patrona")
        self.elementi["D0441-0.600D"] = crea_accessorio("D0441-0.600D", "Patrona std corsa 50mm passo 0.60", 1, 380, "Patrona")
        self.elementi["D0441-0.700D"] = crea_accessorio("D0441-0.700D", "Patrona std corsa 50mm passo 0.70", 1, 380, "Patrona")
        self.elementi["D0441-0.800D"] = crea_accessorio("D0441-0.800D", "Patrona std corsa 50mm passo 0.80", 1, 380, "Patrona")
        self.elementi["D0441-1.000D"] = crea_accessorio("D0441-1.000D", "Patrona std corsa 50mm passo 1.00", 1, 380, "Patrona")
        self.elementi["D0441-1.250D"] = crea_accessorio("D0441-1.250D", "Patrona std corsa 50mm passo 1.25", 1, 380, "Patrona")
        self.elementi["D0441-1.500D"] = crea_accessorio("D0441-1.500D", "Patrona std corsa 50mm passo 1.50", 1, 380, "Patrona")
        self.elementi["D0441-1.750D"] = crea_accessorio("D0441-1.750D", "Patrona std corsa 50mm passo 1.75", 1, 380, "Patrona")
        self.elementi["D0441-2.000D"] = crea_accessorio("D0441-2.000D", "Patrona std corsa 50mm passo 2.00", 1, 380, "Patrona")
        self.elementi["D0442-0.350D"] = crea_accessorio("D0442-0.350D", "Patrona std corsa 80mm passo 0.35", 1, 380, "Patrona")
        self.elementi["D0442-0.400D"] = crea_accessorio("D0442-0.400D", "Patrona std corsa 80mm passo 0.40", 1, 380, "Patrona")
        self.elementi["D0442-0.450D"] = crea_accessorio("D0442-0.450D", "Patrona std corsa 80mm passo 0.45", 1, 380, "Patrona")
        self.elementi["D0442-0.500D"] = crea_accessorio("D0442-0.500D", "Patrona std corsa 80mm passo 0.50", 1, 380, "Patrona")
        self.elementi["D0442-0.600D"] = crea_accessorio("D0442-0.600D", "Patrona std corsa 80mm passo 0.60", 1, 380, "Patrona")
        self.elementi["D0442-0.700D"] = crea_accessorio("D0442-0.700D", "Patrona std corsa 80mm passo 0.70", 1, 380, "Patrona")
        self.elementi["D0442-0.800D"] = crea_accessorio("D0442-0.800D", "Patrona std corsa 80mm passo 0.80", 1, 380, "Patrona")
        self.elementi["D0442-1.000D"] = crea_accessorio("D0442-1.000D", "Patrona std corsa 80mm passo 1.00", 1, 380, "Patrona")
        self.elementi["D0442-1.250D"] = crea_accessorio("D0442-1.250D", "Patrona std corsa 80mm passo 1.25", 1, 380, "Patrona")
        self.elementi["D0442-1.500D"] = crea_accessorio("D0442-1.500D", "Patrona std corsa 80mm passo 1.50", 1, 380, "Patrona")
        self.elementi["D0442-1.750D"] = crea_accessorio("D0442-1.750D", "Patrona std corsa 80mm passo 1.75", 1, 380, "Patrona")
        self.elementi["D0442-2.000D"] = crea_accessorio("D0442-2.000D", "Patrona std corsa 80mm passo 2.00", 1, 380, "Patrona")

        self.elementi["DA4070001"] = crea_accessorio("DA4070001", "Piastra di interfaccia DX28/EX28", 3, 380, "Piastra")

        self.elementi["10410071"] = crea_accessorio("10410071", "EBPE85.60", 4, 710, "Accessorio") 
        self.elementi["10410075"] = crea_accessorio("10410075", "EBPE85.85", 4, 710, "Accessorio") 
        self.elementi["10410041"] = crea_accessorio("10410041", "EBIE85.60", 4, 710, "Accessorio") 
        self.elementi["10410045"] = crea_accessorio("10410045", "EBIE85.85", 4, 710, "Accessorio") 
        self.elementi["10410015"] = crea_accessorio("10410015", "EAE85", 4, 710, "Accessorio") 
        self.elementi["10410215"] = crea_accessorio("10410215", "EGE85", 4, 1000, "Accessorio") 
        self.elementi["10410225"] = crea_accessorio("10410225", "EHE85", 4, 930, "Accessorio") 
        self.elementi["10410140"] = crea_accessorio("10410140", "EDE85/500", 4, 500, "Accessorio") 
        self.elementi["10410145"] = crea_accessorio("10410145", "EDE85/600", 4, 550, "Accessorio") 
        self.elementi["10410144"] = crea_accessorio("10410144", "EDE85/700", 4, 600, "Accessorio") 
        self.elementi["10410146"] = crea_accessorio("10410146", "EDE85/800", 4, 600, "Accessorio") 
        self.elementi["10410147"] = crea_accessorio("10410147", "EDE85/1000", 4, 650, "Accessorio") 
        self.elementi["10410165"] = crea_accessorio("10410165", "EDEH85/400", 4, 600, "Accessorio") 
        self.elementi["10410170"] = crea_accessorio("10410170", "EDEH85/500", 4, 650, "Accessorio") 
        self.elementi["10410175"] = crea_accessorio("10410175", "EDEH85/600", 4, 710, "Accessorio") 
        self.elementi["10410237"] = crea_accessorio("10410237", "EIPE60", 4, 500, "Accessorio") 
        self.elementi["10410238"] = crea_accessorio("10410238", "EIPE85", 4, 550, "Accessorio") 
        self.elementi["10410257"] = crea_accessorio("10410257", "ELIE60", 4, 500, "Accessorio") 
        self.elementi["10410238X"] = crea_accessorio("10410238X", "ELIE85", 4, 550, "Accessorio") 
        self.elementi["10410185"] = crea_accessorio("10410185", "EEE85", 4, 60, "Accessorio") 
        self.elementi["10410265"] = crea_accessorio("10410265", "EME85", 4, 60, "Accessorio")
        self.elementi["10410240"] = crea_accessorio("10410240", "EJE85", 4, 1000, "Accessorio") 
        self.elementi["10410275"] = crea_accessorio("10410275", "EOE85", 4, 450, "Accessorio") 

    def get_accessorio(self, codice):
        return self.elementi.get(codice)

    def elenco(self):
        return self.elementi