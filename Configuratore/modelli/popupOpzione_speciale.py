from PySide6.QtWidgets import QDialog, QMessageBox, QWidget
from modelli.opzione_speciale import OpzioneSpeciale
from gui.popupOpzione import Ui_PopupOpzione
import pyodbc
import configparser
import os
import sys
from config_loader import D_HOST, D_NAME, D_USER, D_PASS, DB_CONFIG, risorsa_percorso

class ufOpzione(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_app = parent
        
        self.ui = Ui_PopupOpzione()
        self.ui.setupUi(self)
        
        self.ui.btn_salva.clicked.connect(self.salva_opzione)
        self.ui.btn_carica.clicked.connect(self.importa_opzione)
        self.ui.cb_opzioni_speciali.currentIndexChanged.connect(self.carica_opzione)
        self.ui.btn_agg_opz.clicked.connect(self.aggiungi_opzione)
        self.ui.btn_elim_opz.clicked.connect(self.elimina_opzione)
        self.modalita_opzione = None
        self.nuova_opzione = None

        try:
            connessione = pyodbc.connect(DB_CONFIG)

            cursore = connessione.cursor()

            cursore.execute("SELECT codice FROM dbo.opzioni ORDER BY codice ASC")
            opzioni = [riga[0] for riga in cursore.fetchall()]

            self.ui.cb_opzioni_speciali.clear()
            self.ui.cb_opzioni_speciali.addItems(opzioni)

            self.ui.cb_opzioni_speciali.setCurrentIndex(-1)

            cursore.close()
            connessione.close()

        except Exception as e:
                    QMessageBox.critical(self, "Errore Caricamento Dati", f"Impossibile caricare le opzioni:\n{e}")

        self.ui.cb_opzioni_speciali.setCurrentIndex(-1)
        self.ui.tb_descrizione.clear()
        self.ui.tb_prezzo.clear()
        self.ui.tb_consegna.clear()
        self.ui.tb_note.clear()
        self.ui.tb_creatore.clear()
        self.ui.tb_data.clear()
                
    def aggiungi_opzione(self):
        self.modalita_opzione = "NUOVO"
        self.ui.cb_opzioni_speciali.setCurrentIndex(-1)
        self.ui.tb_descrizione.clear()
        self.ui.tb_prezzo.clear()
        self.ui.tb_consegna.clear()
        self.ui.tb_data.clear()
        self.ui.tb_creatore.clear()
        self.ui.tb_note.clear()
        self.ui.btn_salva.setEnabled(True)
        for widget in self.findChildren(QWidget):
            widget.setEnabled(True)
        self.ui.btn_carica.setEnabled(False)

    def elimina_opzione(self):
        codice_da_eliminare = self.ui.cb_opzioni_speciali.currentText()
        indice_selezionato = self.ui.cb_opzioni_speciali.currentIndex()
        if indice_selezionato >= 0:
            self.ui.cb_opzioni_speciali.removeItem(indice_selezionato)
        try:
            connessione = pyodbc.connect(DB_CONFIG)

            cursore = connessione.cursor()

            if not codice_da_eliminare != "":
                cursore.execute("DELETE FROM dbo.opzioni WHERE codice = ?", (codice_da_eliminare,))
                connessione.commit() 

            cursore.close()
            connessione.close()

            QMessageBox.information(self, "Successo", f"Opzione {codice_da_eliminare} eliminata con successo")
        
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile eliminare l'opzione:\n{e}")

        self.ui.cb_opzioni_speciali.setCurrentIndex(-1)
        self.ui.tb_descrizione.clear()
        self.ui.tb_prezzo.clear()
        self.ui.tb_consegna.clear()
        self.ui.tb_note.clear()
        self.ui.tb_creatore.clear()
        self.ui.tb_data.clear()
        
    def salva_opzione(self):
        self.ui.btn_carica.setEnabled(True)
        self.nuova_opzione = OpzioneSpeciale(
            codice = self.ui.cb_opzioni_speciali.currentText(),
            descrizione = self.ui.tb_descrizione.toPlainText(),
            prezzo = self.ui.tb_prezzo.text(),
            consegna = self.ui.tb_consegna.text(),
            note = self.ui.tb_note.toPlainText(),
            autore = self.ui.tb_creatore.text(),
            data = self.ui.tb_data.text()   
        )
        valido, messaggio_errore = self.nuova_opzione.convalida_dati()
        
        if not valido:
            QMessageBox.warning(self, "Errore di compilazione", messaggio_errore)
            return

        try:
            connessione = pyodbc.connect(DB_CONFIG)

            cursore = connesisone.cursor()

            if self.modalita_opzione == "NUOVO":

                query_opzione = "INSERT INTO dbo.opzioni (codice, descrizione, prezzo," \
                    "consegna, data, autore, note) VALUES (?,?,?,?,?,?,?)"

                valori_opzione = (self.nuova_opzione.codice, self.nuova_opzione.descrizione, self.nuova_opzione.prezzo,
                self.nuova_opzione.consegna, self.nuova_opzione.data, self.nuova_opzione.autore, self.nuova_opzione.note)

                cursore.execute(query_opzione, valori_opzione)
                
            elif self.modalita_opzione == "MODIFICA":

                query_opzione = """
                    UPDATE dbo.opzioni
                    SET descrizione=?, prezzo=?, consegna=?, data=?, autore=?, note=? WHERE codice=?                
                    """    
                valori_opzione = (self.nuova_opzione.descrizione, self.nuova_opzione.prezzo,
                    self.nuova_opzione.consegna, self.nuova_opzione.data, self.nuova_opzione.autore, self.nuova_opzione.note, self.nuova_opzione.codice)

                cursore.execute(query_opzione, valori_opzione)

            connessione.commit()
            cursore.close()
            connessione.close()

            QMessageBox.information(self, "Successo", "Opzione salvata")
            self.modalita_opzione = None

        except Exception as e:
            QMessageBox.critical(
            self,
            "Errore Caricamento Opzione",
            f"Impossibile caricare l'opzione:\n{e}"
        )
            
    def importa_opzione(self):
        self.nuova_opzione = OpzioneSpeciale(
            codice = self.ui.cb_opzioni_speciali.currentText(),
            descrizione = self.ui.tb_descrizione.toPlainText(),
            prezzo = self.ui.tb_prezzo.text(),
            consegna = self.ui.tb_consegna.text(),
            note = self.ui.tb_note.toPlainText(),
            autore = self.ui.tb_creatore.text(),
            data = self.ui.tb_data.text()   
        )

        if self.nuova_opzione.codice in [o.codice for o in self.main_app.opzioni_temporanee]:
            QMessageBox.warning(self, "Attenzione", "Opzione già presente")
            return
        
        valido, messaggio_errore = self.nuova_opzione.convalida_dati()
        
        if not valido:
            QMessageBox.warning(self, "Errore di compilazione", messaggio_errore)
            return
        
        self.accept()

    def reject(self):
        self.nuova_opzione = None
        super().reject()

    def carica_opzione(self):
        self.modalita_opzione = "MODIFICA"
        for widget in self.findChildren(QWidget):
            widget.setEnabled(True)
        codice = self.ui.cb_opzioni_speciali.currentText()

        if codice == "":
            return

        try:
            connessione = pyodbc.connect(DB_CONFIG)

            cursore = connessione.cursor()

            cursore.execute("""
                SELECT
                    descrizione,
                    prezzo,
                    consegna,
                    data,
                    autore,
                    note
                    FROM dbo.opzioni
                WHERE codice = ?
            """, (codice,))
            
            opzione = cursore.fetchone()
            
            if opzione:

                self.ui.tb_descrizione.setPlainText(opzione[0] or "")
                self.ui.tb_prezzo.setText(str(opzione[1]) if opzione[1] is not None else "")
                self.ui.tb_consegna.setText(str(opzione[2]) if opzione[2] is not None else "")
                self.ui.tb_data.setText(opzione[3] or "")
                self.ui.tb_creatore.setText(opzione[4] or "")
                self.ui.tb_note.setPlainText(opzione[5] or "")
                
            cursore.close()
            connessione.close()

        except Exception as e:
            QMessageBox.critical(
            self,
            "Errore Caricamento opzione",
            f"Impossibile caricare l'opzione:\n{e}"
        )
