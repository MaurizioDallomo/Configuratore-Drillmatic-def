from dati.creadati import crea_opzione
from modelli.enums import DestinazioneOpzione, ComportamentoOpzione
from enum import Flag, auto

class ArchivioOpzioni:
    def __init__(self):
        self.elementi = {}

    def carica(self):
        
        # opzioni motore
        self.elementi["motore_maggiorato"] = crea_opzione(
            "motore_maggiorato",
            "Motore maggiorato",
            "Motore maggiorato ",
            ComportamentoOpzione.DescrizioneEditabile,
            DestinazioneOpzione.Motore
        )

        self.elementi["posizione_motore_mandrino"] = crea_opzione(
            "posizione_motore_mandrino",
            "Posizione motore mandrino",
            "Motore mandrino montato in posizione",
            ComportamentoOpzione.DescrizioneEditabile,
            DestinazioneOpzione.posizione_motore_mandrino
        )

        self.elementi["motore_autofrenante"] = crea_opzione(
            "motore_autofrenante",
            "Motore autofrenante",
            "Motore autofrenante ",
            ComportamentoOpzione.DescrizioneComplessa,
            DestinazioneOpzione.Motore
        )

        self.elementi["motore_autofrenante_magg"] = crea_opzione(
            "motore_autofrenante_magg",
            "Motore autofrenante maggiorato",
            "Motore autofrenante maggiorato ",
            ComportamentoOpzione.DescrizioneEditabile,
            DestinazioneOpzione.Motore
        )

        self.elementi["motore_doppia_pol"] = crea_opzione(
            "motore_doppia_pol",
            "Motore doppia polarità",
            "Motore doppia polarità ",
            ComportamentoOpzione.DescrizioneEditabile,
            DestinazioneOpzione.Motore
        )

        self.elementi["motore_autofrenante_doppia_pol"] = crea_opzione(
            "motore_autofrenante_doppia_pol",
            "Motore autofrenante doppia polarità",
            "Motore autofrenante doppia polarità ",
            ComportamentoOpzione.DescrizioneComplessa,
            DestinazioneOpzione.Motore
        )

        self.elementi["riduttore"] = crea_opzione(
            "riduttore",
            "Riduttore di velocità",
            "Riduttore di velocità ",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.Nuovo
        )

        self.elementi["brushless"] = crea_opzione(
            "brushless",
            "Flangia per motore brushless",
            "Predisposizione per montaggio Vostro motore brushless\nMotore non compreso",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.Motore
        )

        self.elementi["posizione_motore_brushless"] = crea_opzione(
            "posizione_motore_brushless",
            "Posizione motore brushless",
            "Motore brushless montato in posizione",
            ComportamentoOpzione.DescrizioneEditabile,
            DestinazioneOpzione.posizione_motore_brushless
        )

        self.elementi["senza_motore"] = crea_opzione(
            "senza_motore",
            "Motore non fornito",
            "Motore non fornito\nFlangia per motore standard\nPuleggia motore standard",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.Motore
        )

        self.elementi["corpo_mandrino"] = crea_opzione(
            "corpo_mandrino",
            "Senza motore e scatola di trasmissione",
            "Scatola di trasmissione non compresa\nMotore non compreso",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.Sbloccaggio | DestinazioneOpzione.Motore
        )

        self.elementi["velocita_speciale"] = crea_opzione(
            "velocita_speciale",
            "Velocità speciale fuori catalogo",
            "Velocità speciale ",
            ComportamentoOpzione.DescrizioneEditabile,
            DestinazioneOpzione.Velocita
        )

        self.elementi["colore"] = crea_opzione(
            "colore",
            "Colore diverso da RAL 7016",
            "Colore RAL ",
            ComportamentoOpzione.DescrizioneEditabile,
            DestinazioneOpzione.Nuovo
        )

        self.elementi["refrigerante"] = crea_opzione(
            "refrigerante",
            "Refrigerante interno",
            "Passaggio del liquido refrigerante attraverso il mandrino",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.Sbloccaggio
        )

        self.elementi["refrigerante_no_giunto"] = crea_opzione(
            "refrigerante_no_giunto",
            "Refrigerante interno (giunto escluso)",
            "Passaggio del liquido refrigerante attraverso il mandrino\nGiunto non compreso",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.Sbloccaggio
        )

        self.elementi["cuscinetti"] = crea_opzione(
            "cuscinetti",
            "Cuscinetti CO",
            "Cuscinetti a contatto obliquo precaricati",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.Nuovo
        )

        self.elementi["serbatoio"] = crea_opzione(
            "serbatoio",
            "Serbatoio olio patrona",
            "Serbatoio olio patrona per lavorazione dal basso all'alto",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.Nuovo
        )

        self.elementi["equilibratura"] = crea_opzione(
            "equilibratura",
            "Equilibratura",
            "Albero mandrino equilibrato per alte velocità",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.Nuovo
        )

        self.elementi["montaggio_motore"] = crea_opzione(
            "montaggio_motore",
            "Montaggio motore cliente",
            "Montaggio motore di fornitura del cliente",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.Nuovo | DestinazioneOpzione.Motore
        )

        self.elementi["sbloccaggio_pneumatico"] = crea_opzione(
            "sbloccaggio_pneumatico",
            "Cambio utensile pneumatico",
            "Cambio utensile pneumatico\n"
            "Ritenuta meccanica tramite molle a tazza\n"
            "Sbloccaggio tramite cilindro pneumatico a 6 bar\n"
            "N.6 sensori induttivi di controllo posizione:\n"
            "- Pinza aperta (rotazione non ammessa)\n"
            "- Pinza chiusa con portautensile\n"
            "- Pinza chiusa in posizione errata\n"
            "- Pinza chiusa senza portautensile\n"
            "- Cilindro in posizione arretrata (rotazione ammessa)\n"
            "- Controllo fasatura angolare\n"
            "Passaggio liquido refrigerante attraverso il mandrino (max 100 bar)\n"
            "Rotazione a secco ammessa",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.Sbloccaggio
        )

        self.elementi["sbloccaggio_idraulico"] = crea_opzione(
            "sbloccaggio_idraulico",
            "Cambio utensile idraulico",
            "Cambio utensile idraulico\n"
            "Ritenuta meccanica tramite molle a tazza\n"
            "Sbloccaggio tramite cilindro idraulico a 30 bar\n"
            "N.6 sensori induttivi di controllo posizione:\n"
            "- Pinza aperta (rotazione non ammessa)\n"
            "- Pinza chiusa con portautensile\n"
            "- Pinza chiusa in posizione errata\n"
            "- Pinza chiusa senza portautensile\n"
            "- Cilindro in posizione arretrata (rotazione ammessa)\n"
            "Controllo fasatura angolare\n"
            "Passaggio liquido refrigerante attraverso il mandrino (max 100 bar)\n"
            "Rotazione a secco ammessa",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.Sbloccaggio
        )

        self.elementi["predisposizione_teste"] = crea_opzione(
            "predisposizione_teste",
            "Flangia per teste multiple",
            "Predisposizione montaggio teste multiple",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.Nuovo
        )

        self.elementi["rottura_cinghia"] = crea_opzione(
            "rottura_cinghia",
            "Controllo rottura cinghia",
            "Camma per il controllo rottura cinghia (sensore non compreso)",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.Nuovo
        )

        self.elementi["flangia_motore"] = crea_opzione(
            "flangia_motore",
            "Flangia per motore brushless diretto",
            "Flangia e giunto elastico per Vostro motore brushless\nMotore non compreso",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.MotorizzazioneSlitta
        )

        self.elementi["flangia_motore_rinviato"] = crea_opzione(
            "flangia_motore_rinviato",
            "Flangia per motore brushless rinviato 180°",
            "Scatola di trasmissione con pulegge e cinghia per motore brushless rinviato a 180°\n"
            "Posizione motore ",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.MotorizzazioneSlitta
        )

        self.elementi["soffietto_100"] = crea_opzione(
            "soffietto_100",
            "Soffietto corsa 100mm",
            "Soffietto di protezione interno a lamelle corsa 100mm",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.Nuovo
        )

        self.elementi["soffietto_200"] = crea_opzione(
            "soffietto_200",
            "Soffietto corsa 200mm",
            "Soffietto di protezione interno a lamelle corsa 200mm",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.Nuovo
        )

        self.elementi["soffietto_300"] = crea_opzione(
            "soffietto_300",
            "Soffietto corsa 300mm",
            "Soffietto di protezione interno a lamelle corsa 300mm",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.Nuovo
        )

        self.elementi["soffietto_250"] = crea_opzione(
            "soffietto_250",
            "Soffietto corsa 250mm",
            "Soffietto di protezione interno a lamelle corsa 250mm",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.Nuovo
        )

        self.elementi["soffietto_400"] = crea_opzione(
            "soffietto_400",
            "Soffietto corsa 400mm",
            "Soffietto di protezione interno a lamelle corsa 400mm",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.Nuovo
        )

        self.elementi["soffietto_600"] = crea_opzione(
            "soffietto_600",
            "Soffietto corsa 600mm",
            "Soffietto di protezione interno a lamelle corsa 600mm",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.Nuovo
        )

        self.elementi["guide_rulli"] = crea_opzione(
            "guide_rulli",
            "Guide a rulli",
            "Movimentazione tramite n.2 guide + n.4 pattini a ricircolo di rulli",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.scorrimento
        )

        self.elementi["vite_maggiorata"] = crea_opzione(
            "vite_maggiorata",
            "Vite maggiorata",
            "Avanzamento tramite vite a ricircolo di sfere maggiorata",
            ComportamentoOpzione.DescrizioneEditabile,
            DestinazioneOpzione.vite
        )

        self.elementi["camma_micro"] = crea_opzione(
            "camma_micro",
            "Camma micro laterale",
            "Camma 3 micro laterale\nPosizione DX/SX da definire",
            ComportamentoOpzione.DescrizioneFissa,
            DestinazioneOpzione.Nuovo
        )

    def get_opzione(self, opzione):
        return self.elementi.get(opzione)
            
    def elenco(self):
        return self.elementi

    def numero_opzioni(self):
        return len(self.elementi)