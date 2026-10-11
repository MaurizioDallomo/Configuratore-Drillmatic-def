from dati.creadati import crea_mandrino

class ArchivioMandrini:
    def __init__(self):
        self.elementi = {}

    def carica(self):
        
        self.elementi["L"] = crea_mandrino("L", "Mandrino portautensili a pinza ER20")
        self.elementi["N"] = crea_mandrino("N", "Mandrino portautensili a pinza ER32")
        self.elementi["A"] = crea_mandrino("A", "Mandrino portautensili B.12")
        self.elementi["B"] = crea_mandrino("B", "Mandrino portautensili B.18")
        self.elementi["F"] = crea_mandrino("F", "Mandrino portautensili cilindrico Ø16 DIN55058")
        self.elementi["F1"] = crea_mandrino("F1", "Mandrino portautensili cilindrico Ø16 DIN55058 integrale")
        self.elementi["H"] = crea_mandrino("H", "Mandrino portautensili cilindrico Ø28 DIN55058")
        self.elementi["H1"] = crea_mandrino("H1", "Mandrino portautensili cilindrico Ø28 DIN55058")
        self.elementi["H2"] = crea_mandrino("H2", "Mandrino portautensili cilindrico Ø28 DIN55058")
        self.elementi["I"] = crea_mandrino("I", "Mandrino portautensili cilindrico Ø36 DIN55058")
        self.elementi["D"] = crea_mandrino("D", "Mandrino portautensili CM2")
        self.elementi["D1"] = crea_mandrino("D1", "Mandrino portautensili CM2")
        self.elementi["LC"] = crea_mandrino("LC", "Mandrino portautensili a pinza ER20 con compensazione in trazione 15mm")
        self.elementi["LX"] = crea_mandrino("LX", "Mandrino portautensili a pinza ER32 con compensazione in trazione 15mm")
        self.elementi["S"] = crea_mandrino("S", "Mandrino portautensili ISO30 DIN 2080")
        self.elementi["T"] = crea_mandrino("T", "Mandrino portautensili ISO40 DIN 2080")
        self.elementi["TL"] = crea_mandrino("TL", "Mandrino portautensili ISO40 DIN 69871 allungato")
        self.elementi["U"] = crea_mandrino("U", "Mandrino portautensili ISO50 DIN 2080")
        self.elementi["O"] = crea_mandrino("O", "Mandrino portautensili HSK50")
        self.elementi["P"] = crea_mandrino("P", "Mandrino portautensili HSK63 A")
        self.elementi["Q"] = crea_mandrino("Q", "Mandrino portautensili HSK63 C")

    def get_mandrino(self, mandrino):
        return self.elementi.get(mandrino)
            
    def elenco(self):
        return self.elementi