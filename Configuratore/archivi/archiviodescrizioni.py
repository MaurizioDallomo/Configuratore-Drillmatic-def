from dati.creadati import crea_descrizione

class ArchivioDescrizioni:
    def __init__(self):
        self.elementi = {}

    def carica(self):
        
        self.elementi ["capacita_foratura"] = crea_descrizione("capacita_foratura", "Capacità di foratura su acciaio a 600N/mm2 = ")
        self.elementi ["capacita_maschiatura"] = crea_descrizione("capacita_maschiatura", "Capacità di maschiatura su acciaio a 600N/mm2 = ")
        self.elementi ["spinta"] = crea_descrizione("spinta", "Spinta = ")
        self.elementi ["carico_assiale"] = crea_descrizione("carico_assiale", "Carico assiale = ")
        self.elementi ["concentricita"] = crea_descrizione("concentricita", "Concentricità = ")
        self.elementi ["vite"] = crea_descrizione("vite", "Avanzamento tramite vite a ricircolo di sfere ")
        self.elementi ["rapporto_vite"] = crea_descrizione("rapporto_vite", "Rapporto di trasmissione vite 1:1 o 1:2 in riduzione")
        self.elementi ["posizione_motore_brushless"] = crea_descrizione("posizione_motore_brushless", "Motore brushless montato in posizione U2")
        self.elementi ["posizione_motore_mandrino"] = crea_descrizione("posizione_motore_mandrino", "Motore mandrino montato in posizione Z1")
        self.elementi ["motore_slitta"] = crea_descrizione("motore_slitta", "Flangia e giunto per montaggio Vostro motore (motore non compreso)")
        self.elementi ["finecorsa"] = crea_descrizione("finecorsa", "Finecorsa magnetici")
        self.elementi ["scorrimento"] = crea_descrizione("scorrimento", "Movimentazione tramite n.2 guide + n.4 pattini a ricircolo di sfere")
        self.elementi ["lubrificazione"] = crea_descrizione("lubrificazione", "Lubrificazione pattini a vita")
        self.elementi ["cilindro_idraulico"] = crea_descrizione("cilindro_idraulico", "Cilindro idraulico dia.")
        self.elementi ["cilindro_pneumatico"] = crea_descrizione("cilindro_pneumatico", "Cilindro pneumatico dia.")

    def get_descrizione(self, descrizione):
            return self.elementi.get(descrizione)
    
    def elenco(self):
        return self.elementi