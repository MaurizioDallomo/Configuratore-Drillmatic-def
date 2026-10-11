from gui.popupPreventivo import Ui_Dialog
from PySide6.QtWidgets import QMessageBox, QDialog
import pyodbc
import configparser
import sys
import os

def risorsa_percorso(relative_path):
    """ Ottiene il percorso assoluto della risorsa, funziona sia in sviluppo che dopo PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

config = configparser.ConfigParser()
percorso_config = risorsa_percorso("config.ini")
if os.path.exists(percorso_config):
    config.read(percorso_config)
    D_HOST = config["DATABASE"].get("host", "localhost")
else:
    D_HOST = "localhost"
    
class UfPreventivo(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_app = parent 
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.id_preventivo_scelto = None
                
        self.ui.btn_ok.clicked.connect(self.carica_preventivo)
        self.ui.btn_svuota_campi.clicked.connect(self.svuota_campi)
        self.ui.cb_anno.currentIndexChanged.connect(self.seleziona_anno)
        self.ui.cb_Cliente.currentIndexChanged.connect(self.seleziona_cliente)
        self.ui.cb_preventivo.currentIndexChanged.connect(self.seleziona_preventivo)

        self.ui.cb_Cliente.blockSignals(True)
        self.ui.cb_anno.blockSignals(True)
        self.ui.cb_preventivo.blockSignals(True)

        self.ui.cb_preventivo.clear()
        self.ui.cb_Cliente.clear()
        self.ui.cb_anno.clear()

        try:
            connessione = pyodbc.connect(
                "Driver={ODBC Driver 18 for SQL Server};"
                f"Server={D_HOST};"  # Manterrà 'localhost' o l'IP che hai inserito nella variabile
                "Database=configuratore;"
                "Trusted_Connection=yes;"
                "TrustServerCertificate=yes;"  # Fondamentale per evitare l'errore SSL visto in precedenza
            )

            cursore = connessione.cursor()

            cursore.execute("SELECT id, ragione_sociale FROM configuratore.clienti ORDER BY ragione_sociale ASC")
            clienti_db = cursore.fetchall()

            for riga in clienti_db:
                id_cliente = riga[0]
                ragione_sociale = riga[1]
                self.ui.cb_Cliente.addItem(ragione_sociale, id_cliente)    

            self.ui.cb_Cliente.blockSignals(False)
            self.ui.cb_Cliente.setCurrentIndex(-1)

            cursore.close()
            connessione.close()

        except Exception as e:
            QMessageBox.critical(self, "Errore Caricamento Dati", f"Impossibile caricare i clienti:\n{e}")
                 
    def seleziona_cliente(self):
        id_cliente_selezionato = self.ui.cb_Cliente.currentData()

        try:
            connessione = pyodbc.connect(
                "Driver={ODBC Driver 18 for SQL Server};"
                f"Server={D_HOST};"
                "Database=configuratore;"
                "Trusted_Connection=yes;"
                "TrustServerCertificate=yes;"
            )

            cursore = connessione.cursor()

            cursore.execute("""
                SELECT DISTINCT anno_preventivo 
                FROM configuratore.preventivi 
                WHERE cliente_id = ? 
                ORDER BY anno_preventivo DESC
            """, (id_cliente_selezionato,))
            
            anni = [str(riga[0]) for riga in cursore.fetchall()]
            
            self.ui.cb_anno.blockSignals(True)
            self.ui.cb_preventivo.blockSignals(True)
            self.ui.cb_anno.clear()
            self.ui.cb_preventivo.clear()
            
            self.ui.cb_anno.addItems(anni)
            
            self.ui.cb_anno.blockSignals(False)
            self.ui.cb_anno.setCurrentIndex(-1)

            cursore.close()
            connessione.close()

        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile caricare gli anni:\n{e}")

    def seleziona_anno(self):
        id_cliente_selezionato = self.ui.cb_Cliente.currentData()
        anno_selezionato = self.ui.cb_anno.currentText()

        if id_cliente_selezionato is None or anno_selezionato == "":
            return

        try:
            connessione = pyodbc.connect(
                "Driver={ODBC Driver 18 for SQL Server};"
                f"Server={D_HOST};"
                "Database=configuratore;"
                "Trusted_Connection=yes;"
                "TrustServerCertificate=yes;"
            )

            cursore = connessione.cursor()

            cursore.execute("""
                SELECT id_preventivo, numero_preventivo 
                FROM configuratore.preventivi 
                WHERE cliente_id = ? AND anno_preventivo = ? 
                ORDER BY id_preventivo DESC
            """, (id_cliente_selezionato, int(anno_selezionato)))
            
            preventivi_db = cursore.fetchall()

            self.ui.cb_preventivo.blockSignals(True)
            self.ui.cb_preventivo.clear()
            
            for riga in preventivi_db:
                self.ui.cb_preventivo.addItem(riga[1], riga[0])

            self.ui.cb_preventivo.blockSignals(False)
            self.ui.cb_preventivo.setCurrentIndex(-1)

            cursore.close()
            connessione.close()

        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile caricare i preventivi:\n{e}")

    def seleziona_preventivo(self):
        id_preventivo = self.ui.cb_preventivo.currentData()
        
        if id_preventivo is not None:
            self.id_preventivo_scelto = id_preventivo
        else:
            self.id_preventivo_scelto = None

    def carica_preventivo(self):
        if not hasattr(self, 'id_preventivo_scelto') or self.id_preventivo_scelto is None:
            QMessageBox.warning(self, "Selezione incompleta", "Seleziona un preventivo dall'elenco prima di procedere")
            return

        self.accept()

    def svuota_campi(self):
        self.id_preventivo_scelto = None
        
        self.ui.cb_Cliente.blockSignals(True)
        self.ui.cb_anno.blockSignals(True)
        self.ui.cb_preventivo.blockSignals(True)
        
        self.ui.cb_Cliente.setCurrentIndex(-1)
        self.ui.cb_anno.clear()
        self.ui.cb_preventivo.clear()
        
        self.ui.cb_Cliente.blockSignals(False)

    def reject(self):
            self.id_preventivo_scelto = None
            super().reject()
