from modelli.famiglia import Famiglia

class ArchivioFamiglie:
    def __init__(self):
        self.elementi = {}

    def carica(self, catalogo):

        f = Famiglia()
        f.codice = "DXP"
        f.descrizione_base = "Unità di foratura elettro-pneumatica"
        
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("velocita_speciale"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("motore_maggiorato"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("riduttore"))
        f.aggiungi_opzione (catalogo.opzioni.get_opzione("colore"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("capacita_foratura"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("spinta"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("concentricita"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("finecorsa"))
            
        self.elementi[f.codice] = f

        f = Famiglia()
        f.codice = "DXE"
        f.descrizione_base = "Unità di foratura con avanzamento ad asse controllato"

        f.aggiungi_opzione(catalogo.opzioni.get_opzione("velocita_speciale"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("motore_maggiorato"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("motore_autofrenante"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("motore_autofrenante_magg"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("posizione_motore_brushless"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("brushless"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("senza_motore"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("montaggio_motore"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("riduttore"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("colore"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("cuscinetti"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("posizione_motore_brushless"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("capacita_foratura"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("capacita_maschiatura"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("spinta"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("concentricita"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("vite"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("rapporto_vite"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("motore_slitta"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("finecorsa"))

        self.elementi[f.codice] = f

        f = Famiglia()
        f.codice = "TX"
        f.descrizione_base = "Unità di maschiatura a patrona"

        f.aggiungi_opzione(catalogo.opzioni.get_opzione("velocita_speciale"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("motore_maggiorato"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("motore_autofrenante"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("motore_autofrenante_magg"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("brushless"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("senza_motore"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("montaggio_motore"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("riduttore"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("colore"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("serbatoio"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("capacita_maschiatura"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("finecorsa"))

        self.elementi[f.codice] = f
        
        f = Famiglia()
        f.codice = "DTX"
        f.descrizione_base = "Unità fora-maschia elettro-pneumatica"

        f.aggiungi_opzione(catalogo.opzioni.get_opzione("velocita_speciale"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("motore_autofrenante_doppia_pol"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("cuscinetti"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("colore"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("capacita_maschiatura"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("finecorsa"))

        self.elementi[f.codice] = f
                
        f = Famiglia()
        f.codice = "DX"
        f.descrizione_base = "Mandrino motorizzato"

        f.aggiungi_opzione(catalogo.opzioni.get_opzione("refrigerante"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("refrigerante_no_giunto"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("velocita_speciale"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("motore_maggiorato"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("posizione_motore_mandrino"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("brushless"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("senza_motore"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("montaggio_motore"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("riduttore"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("rottura_cinghia"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("corpo_mandrino"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("colore"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("posizione_motore_mandrino"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("capacita_foratura"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("carico_assiale"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("concentricita"))
        
        self.elementi[f.codice] = f
                        
        f = Famiglia()
        f.codice = "EX"
        f.descrizione_base = "Slitta di movimentazione ad asse controllato"

        f.aggiungi_opzione(catalogo.opzioni.get_opzione("flangia_motore"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("flangia_motore_rinviato"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("guide_rulli"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("vite_maggiorata"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("camma_micro"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("colore"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("scorrimento"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("spinta"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("vite"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("motore_slitta"))

        self.elementi[f.codice] = f
                                
        f = Famiglia()
        f.codice = "HX"
        f.descrizione_base = "Slitta di movimentazione idraulica"

        f.aggiungi_opzione(catalogo.opzioni.get_opzione("camma_micro"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("guide_rulli"))
        f.aggiungi_opzione(catalogo.opzioni.get_opzione("colore"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("scorrimento"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("cilindro_idraulico"))
        f.aggiungi_descrizione(catalogo.descrizioni.get_descrizione("spinta"))

        self.elementi[f.codice] = f
                                        
        
    def get_famiglia(self, famiglia):
        return self.elementi.get(famiglia)
        
    def elenco(self):
        return self.elementi
    