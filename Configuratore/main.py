import sys
import traceback
from PySide6.QtWidgets import QApplication 
import qdarktheme
from gui.Configuratore import Configuratore
import os
from PySide6.QtGui import QIcon
from gui.Configuratore import risorsa_percorso

#######################################################################
#if __name__ == "__main__":
#    gestione_listino.cambia_password_utente("admin", "nuova_password")
#######################################################################

def cattura_e_stampa_errori(tipo_errore, valore_errore, traccia_errore):
    print("\n" + "="*60)
    print(" ❌ ERRORE CRITICO INTERCETTATO A RUNTIME:")
    print("="*60)
    # Stampa l'errore completo con file, riga e motivo nel terminale
    traceback.print_exception(tipo_errore, valore_errore, traccia_errore)
    print("="*60)
    print("PREMI INVIO NEL TERMINALE PER CHIUDERE QUESTA FINESTRA...")
    print("="*60)
    # Questo blocca il terminale e gli impedisce di scappare!
    sys.exit(1)
# Diciamo a Python di usare il nostro cacciatore personalizzato
sys.excepthook = cattura_e_stampa_errori





if __name__ == "__main__":
    # Avvia l'applicazione grafica globale
    app = QApplication(sys.argv)

    percorso_icona = risorsa_percorso("logo.ico")
    if os.path.exists(percorso_icona):
        app.setWindowIcon(QIcon(percorso_icona))

    app.setStyleSheet(qdarktheme.load_stylesheet("dark"))
    # Crea e mostra la finestra principale
    finestra = Configuratore()
    finestra.show()
    # Mantiene il programma attivo
    sys.exit(app.exec())