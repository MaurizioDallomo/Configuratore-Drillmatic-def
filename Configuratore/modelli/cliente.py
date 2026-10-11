import re
from modelli.referente import Referente

class Cliente:
     def __init__(self, codice="", ragione_sociale="", indirizzo="", cap="", citta="", provincia="", 
                  partita_iva="", codice_fiscale="", telefono="", email="", pagamento="", 
                  sconto=0, corriere="", resa_merce="", categoria=None):
         self.codice = codice
         self.ragione_sociale = ragione_sociale.strip()
         self.indirizzo = indirizzo.strip()
         self.cap = cap.strip()
         self.citta = citta.strip()
         self.provincia = provincia.strip().upper()
         self.partita_iva = partita_iva.strip()
         self.codice_fiscale = codice_fiscale.strip()
         self.telefono = telefono.strip()
         self.email = email.strip()
         self.categoria = categoria
         self.pagamento = pagamento
         self.sconto = sconto
         self.corriere = corriere
         self.resa_merce = resa_merce
         self.referenti = {}

     def aggiungi_referente(self, ref):
        chiave = f'{ref.nome} {ref.cognome} {ref.ruolo}'
        self.referenti[chiave] = ref

     def convalida_dati(self) -> tuple[bool, str]:
        if not self.ragione_sociale:
            return False, "La ragione sociale è obbligatoria"
        if not self.indirizzo:
            return False, "L'indirizzo è obbligatorio"
        if not self.cap or len(self.cap) != 5 or not self.cap.isdigit():
            return False, "Il CAP deve contenere 5 cifre"
        if not self.citta:
            return False, "La città è obbligatoria"
        if not self.provincia or len(self.provincia) != 2:
            return False, "La provincia deve contenere 2 lettere"
        if self.email:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
                return False, "Indirizzo email non valido"
        if self.telefono and not self.telefono.isdigit():
            return False, "Il numero di telefono deve contenere solo cifre"
        return True, "Dati validi"