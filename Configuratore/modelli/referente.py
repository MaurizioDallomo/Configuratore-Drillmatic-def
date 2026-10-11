import re

class Referente:
     def __init__(self, nome, cognome, ruolo, telefono, cellulare, email):
         self.nome = nome.strip()
         self.cognome = cognome.strip()
         self.ruolo = ruolo.strip()
         self.telefono = telefono.strip()
         self.cellulare = cellulare.strip()
         self.email = email.strip()

     def convalida_dati(self) -> tuple[bool, str]:
        if not self.nome or not self.cognome:
            return False, "Nome e cognome sono obbligatori"
        if self.email:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
                return False, "Indirizzo email non valido"
        if len(self.cellulare) < 6:
            return False, "Il numero di cellulare deve contenere almeno 6 cifre"
        if self.telefono and not self.telefono.isdigit():
            return False, "Il numero di telefono deve contenere solo cifre"
        if self.cellulare and not self.cellulare.isdigit():
            return False, "Il numero di cellulare deve contenere solo cifre"
        return True, "Dati validi"