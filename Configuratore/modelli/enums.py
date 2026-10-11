from enum import Flag, auto

class MacroCategorie(Flag):
    Unita = auto()
    Mandrino = auto()
    Slitta = auto()
    Tavola = auto()

class ComportamentoOpzione(Flag):
    DescrizioneFissa = auto()
    DescrizioneEditabile = auto()
    DescrizioneComplessa = auto()

class DestinazioneOpzione(Flag):
    Motore = auto()
    Velocita = auto()
    Sbloccaggio = auto()
    MotorizzazioneSlitta = auto()
    Nuovo = auto()
    scorrimento = auto()
    vite = auto()
    posizione_motore_brushless = auto()
    posizione_motore_mandrino = auto()
    flangia_motore_rinviato = auto()

class TipovariabileObbligatoria(Flag):
    Corse = auto()
    Mandrini = auto()
    Motori = auto()
    Velocita = auto()
    Cuscinetti = auto()

class TipologiaAccessorio(Flag):
    Base = auto()
    Freno = auto()
    Patrona = auto()
    Accessorio = auto()
    Piastra = auto()
    Tavola = auto()
    Portautensile = auto()

