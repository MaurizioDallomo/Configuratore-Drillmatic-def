class OpzioneSpeciale:
    def __init__(self, codice, descrizione, consegna, prezzo, note, autore, data):
        self.codice = codice.strip()
        self.descrizione = descrizione.strip()
        self.consegna = consegna
        self.prezzo = prezzo
        self.note = note.strip()
        self.autore = autore.strip()
        self.data = data

    def convalida_dati(self) -> tuple[bool, str]:
        if not self.codice or not self.descrizione or not self.consegna or not self.prezzo or not self.autore or not self.data:
            return False, "Mancano dati obbligatori"
        if not self.consegna.isdigit():
            return False, "La consegna deve essere espressa in giorni (numero intero)"
        prezzo_pulito = self.prezzo.replace(",", ".")
        try:
            float(prezzo_pulito)
        except ValueError:
            return False, "Il prezzo deve essere un numero valido (es. 10 o 10.50)"
        return True, "Dati validi"