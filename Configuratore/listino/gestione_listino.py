import sys
import os
import pyodbc
from sqlalchemy import create_engine
import urllib
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem, QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTreeView, QLineEdit, QPushButton, QLabel, QDialog,
    QMessageBox, QHeaderView
)
import configparser
import hashlib
from archivi.archiviomandrini import ArchivioMandrini
from archivi.archivioopzioni import ArchivioOpzioni
from config_loader import D_HOST, D_NAME, D_USER, D_PASS, DB_CONFIG, risorsa_percorso

try:
    parametri = urllib.parse.quote_plus(DB_CONFIG)

    db_pool = create_engine(
        f"mssql+pyodbc:///?odbc_connect={parametri}",
        pool_size=5,                     # Stessa dimensione di prima
        pool_reset_on_return='rollback'  # Ripristina la sessione alla chiusura
    )
except Exception as err:
    print(f"Impossibile avviare il Connection Pool: {err}")
    db_pool = None

def cambia_password_utente(username, nuova_password_chiaro):
    if not db_pool:
        print("Errore: Connection pool non disponibile.")
        return False

    # 1. Genera un NUOVO salt casuale
    nuovo_salt = os.urandom(16).hex()
    
    # 2. Calcola il nuovo hash
    hash_oggetto = hashlib.sha256((nuova_password_chiaro + nuovo_salt).encode('utf-8'))
    nuovo_hash = hash_oggetto.hexdigest()
    
    conn = None
    cursor = None
    try:
        conn = db_pool.raw_connection()
        cursor = conn.cursor()
        
        # 3. Aggiorna sia l'hash che il salt per lo username specificato
        query = """
            UPDATE configuratore.utenti 
            SET password_hash = ?, salt = ? 
            WHERE username = ?
        """
        cursor.execute(query, (nuovo_hash, nuovo_salt, username))
        conn.commit()
        
        if cursor.rowcount == 0:
            print(f"Errore: L'utente '{username}' non esiste.")
            return False
            
        print(f"Password per l'utente '{username}' aggiornata con successo!")
        return True
        
    except pyodbc.Error as err:
        print(f"Errore durante il cambio password: {err}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        
class LoginDialog(QDialog):
    """Finestra di autenticazione per l'accesso al listino."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Accesso Riservato Listino")
        self.setFixedSize(300, 150)
        
        layout = QVBoxLayout()
        
        self.lbl_info = QLabel("Inserisci la password amministratore:")
        self.lbl_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_info)
        
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.txt_password)
        
        self.btn_login = QPushButton("Accedi")
        self.btn_login.clicked.connect(self.verifica_password)
        layout.addWidget(self.btn_login)
        
        self.setLayout(layout)
        
    def verifica_password(self):
        username_inserito = "admin"
        password_inserita = self.txt_password.text()

        if not db_pool:
            QMessageBox.critical(self, "Errore", "Connessione al database non disponibile!")
            return

        conn = None
        cursor = None

        try:
            conn = db_pool.raw_connection()
            cursor = conn.cursor()
            
            query = "SELECT password_hash, salt FROM configuratore.utenti WHERE username = ?"
            cursor.execute(query, (username_inserito,))
            utente = cursor.fetchone()
            
            if utente:
                db_hash = utente['password_hash']
                db_salt = utente['salt']
                
                hash_oggetto = hashlib.sha256((password_inserita + db_salt).encode('utf-8'))
                hash_calcolato = hash_oggetto.hexdigest()
                
                if hash_calcolato == db_hash:
                    self.accept()
                    return
                
            QMessageBox.warning(self, "Errore", "Username o Password errati!")
            
        except pyodbc.Error as err:
            QMessageBox.critical(self, "Errore DB", f"Errore durante la verifica: {err}")
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

class ListinoEditorWindow(QMainWindow):
    """Finestra principale di gestione dei 4 fogli del listino."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pannello di Controllo Listino Prezzi")
        self.resize(900, 650)

        self.archivio_m = ArchivioMandrini()
        self.archivio_m.carica()
        
        self.archivio_op = ArchivioOpzioni()
        self.archivio_op.carica()
        
        # Widget centrale e Tab
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)

        self.modifiche_in_sospeso = {}
        
        # Creazione dei 4 fogli 
        self.crea_foglio_unita()
        self.crea_foglio_mandrini()
        self.crea_foglio_slitte()
        self.crea_foglio_tavole()
        
        # Bottone di salvataggio globale
        self.btn_salva = QPushButton("Salva Tutte le Modifiche nel Database")
        self.btn_salva.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.btn_salva.setFixedHeight(45)
        self.btn_salva.clicked.connect(self.salva_tutto)
        self.main_layout.addWidget(self.btn_salva)
        
        # Dizionario per tracciare le modifiche da salvare
        # Struttura: {(tabella_db, prodotto, codice_chiave): nuovo_prezzo}
        

    def crea_albero_base(self):
        """Helper per creare la struttura ad albero standard delle schede."""
        tree = QTreeView()
        tree.setAlternatingRowColors(True)
        
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Descrizione / Codice Componente", "Prezzo (€)"])
        tree.setModel(model)
        
        # Autofit delle colonne
        tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        tree.setColumnWidth(1, 150)
        
        # Intercettiamo le modifiche effettuate dall'utente a schermo
        model.itemChanged.connect(self.registra_modifica)
        return tree, model


    def ottieni_descrizione_mandrino(self, codice):
        obj = self.archivio_m.get_mandrino(codice)
        # Se l'oggetto ha la proprietà '.nome' usiamo quella, altrimenti '.descrizione'
        if obj:
            return getattr(obj, 'nome', getattr(obj, 'descrizione', ''))
        return "Mandrino Opzionale"

    def ottieni_descrizione_opzione(self, codice):
        obj = self.archivio_op.get_opzione(codice)
        if obj:
            return getattr(obj, 'nome', getattr(obj, 'descrizione', ''))
        return "Opzione Fuori Catalogo"
    
    def crea_foglio_unita(self):
        tree, model = self.crea_albero_base()
        root = model.invisibleRootItem()

        def fetch_as_dict(cur):
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]
        
        try:
            with pyodbc.connect(DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT DISTINCT prodotto_codice FROM configuratore.prezzi_base_unita")
                    prodotti = fetch_as_dict(cursor)
                    
                    for prod in prodotti:
                        p_cod = prod['prodotto_codice']
                        
                        cursor.execute("SELECT corsa_codice, prezzo FROM configuratore.prezzi_base_unita WHERE prodotto_codice = ?", (p_cod,))
                        for corsa_row in fetch_as_dict(cursor):
                            c_cod = corsa_row['corsa_codice']
                            prezzo_base = float(corsa_row['prezzo'])
                            
                            # Riga principale del prodotto: DXP10/75
                            item_macchina = QStandardItem(f"{p_cod}/{c_cod}")
                            item_macchina.setEditable(False)
                            item_macchina.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                            item_macchina.setData(("configuratore.prezzi_base_unita", p_cod, c_cod), Qt.ItemDataRole.UserRole)
                            
                            item_prezzo = QStandardItem(f"{prezzo_base:.2f}")
                            item_prezzo.setEditable(True)
                            item_prezzo.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                            root.appendRow([item_macchina, item_prezzo])
                            
                            # Sotto-riga: Elenco Mandrini Compatibili
                            cursor.execute("SELECT mandrino_codice, prezzo FROM configuratore.prezzi_mandrini WHERE prodotto_codice = ?", (p_cod,))
                            mandrini = fetch_as_dict(cursor)
                            for m_row in mandrini:
                                m_cod = m_row['mandrino_codice']
                                desc_m = self.ottieni_descrizione_mandrino(m_cod)
                                
                                item_m = QStandardItem(f"  {m_cod} ...... {desc_m}")
                                item_m.setEditable(False)
                                item_m.setData(("configuratore.prezzi_mandrini", p_cod, m_cod), Qt.ItemDataRole.UserRole)
                                
                                item_p_m = QStandardItem(f"{float(m_row['prezzo']):.2f}")
                                item_p_m.setEditable(True)
                                item_macchina.appendRow([item_m, item_p_m])
                                
                            # Separatore di sezione e Sotto-riga: Elenco Opzioni
                            cursor.execute("SELECT opzione_codice, prezzo FROM configuratore.prezzi_opzioni WHERE prodotto_codice = ?", (p_cod,))
                            opzioni = fetch_as_dict(cursor)
                            if opzioni:
                                item_div = QStandardItem("  Opzioni")
                                item_div.setEditable(False)
                                item_div.setFont(QFont("Arial", 9, QFont.Weight.Medium))
                                item_div.setForeground(Qt.GlobalColor.darkGray)
                                item_macchina.appendRow([item_div, QStandardItem("")])
                                
                                for op_row in opzioni:
                                    op_cod = op_row['opzione_codice']
                                    desc_op = self.ottieni_descrizione_opzione(op_cod)
                                    
                                    item_op = QStandardItem(f"  {desc_op}")
                                    item_op.setEditable(False)
                                    item_op.setData(("configuratore.prezzi_opzioni", p_cod, op_cod), Qt.ItemDataRole.UserRole)
                                    
                                    item_p_op = QStandardItem(f"{float(op_row['prezzo']):.2f}")
                                    item_p_op.setEditable(True)
                                    item_macchina.appendRow([item_op, item_p_op])
            tree.expandAll()
        except Exception as e:
            print(f"Errore foglio Unità: {e}")
        self.tabs.addTab(tree, "1) Unità")

    def crea_foglio_mandrini(self):
        tree, model = self.crea_albero_base()
        root = model.invisibleRootItem()

        def fetch_as_dict(cur):
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]
        
        try:
            with pyodbc.connect(DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT DISTINCT prodotto_codice FROM configuratore.prezzi_base_mandrini")
                    prodotti = fetch_as_dict(cursor)

                    for prod in prodotti:
                        p_cod = prod['prodotto_codice']
                        
                        cursor.execute("SELECT cuscinetto_codice, taglia, prezzo FROM configuratore.prezzi_base_mandrini WHERE prodotto_codice = ?", (p_cod,))
                        for base_row in fetch_as_dict(cursor):
                            c_cod = base_row['cuscinetto_codice']
                            taglia = base_row['taglia']
                            prezzo_base = float(base_row['prezzo'])
                            
                            item_macchina = QStandardItem(f"Mandrino {p_cod} (Cuscinetto {c_cod} / Gr.{taglia})")
                            item_macchina.setEditable(False)
                            item_macchina.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                            item_macchina.setData(("configuratore.prezzi_base_mandrini", p_cod, f"{c_cod}|{taglia}"), Qt.ItemDataRole.UserRole)
                            
                            item_prezzo = QStandardItem(f"{prezzo_base:.2f}")
                            item_prezzo.setEditable(True)
                            item_prezzo.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                            root.appendRow([item_macchina, item_prezzo])
                            
                            # Accessori/Componenti interni del mandrino
                            cursor.execute("SELECT mandrino_codice, prezzo FROM configuratore.prezzi_mandrini WHERE prodotto_codice = ?", (p_cod,))
                            for m_row in fetch_as_dict(cursor):
                                m_cod = m_row['mandrino_codice']
                                desc_m = self.ottieni_descrizione_mandrino(m_cod)
                                item_m = QStandardItem(f"  {m_cod} ...... {desc_m}")
                                item_m.setEditable(False)
                                item_m.setData(("configuratore.prezzi_mandrini", p_cod, m_cod), Qt.ItemDataRole.UserRole)
                                
                                item_p_m = QStandardItem(f"{float(m_row['prezzo']):.2f}")
                                item_p_m.setEditable(True)
                                item_macchina.appendRow([item_m, item_p_m])
                            
                            # Opzioni del mandrino
                            cursor.execute("SELECT opzione_codice, prezzo FROM configuratore.prezzi_opzioni WHERE prodotto_codice = ?", (p_cod,))
                            opzioni = fetch_as_dict(cursor)
                            if opzioni:
                                item_div = QStandardItem("  Opzioni")
                                item_div.setEditable(False)
                                item_div.setForeground(Qt.GlobalColor.darkGray)
                                item_macchina.appendRow([item_div, QStandardItem("")])
                                
                                for op_row in opzioni:
                                    op_cod = op_row['opzione_codice']
                                    desc_op = self.ottieni_descrizione_opzione(op_cod)
                                    item_op = QStandardItem(f"  {desc_op}")
                                    item_op.setEditable(False)
                                    item_op.setData(("configuratore.prezzi_opzioni", p_cod, op_cod), Qt.ItemDataRole.UserRole)
                                    
                                    item_p_op = QStandardItem(f"{float(op_row['prezzo']):.2f}")
                                    item_p_op.setEditable(True)
                                    item_macchina.appendRow([item_op, item_p_op])
            tree.expandAll()
        except Exception as e:
            print(f"Errore foglio Mandrini: {e}")
            
        self.tabs.addTab(tree, "2) Mandrini")

    def crea_foglio_slitte(self):
        tree, model = self.crea_albero_base()
        root = model.invisibleRootItem()

        def fetch_as_dict(cur):
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]
        
        try:
            with pyodbc.connect(DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT DISTINCT prodotto_codice FROM configuratore.prezzi_base_slitte")
                    prodotti = fetch_as_dict(cursor)
                    for prod in prodotti:
                        p_cod = prod['prodotto_codice']
                        cursor.execute("SELECT corsa_codice, prezzo FROM configuratore.prezzi_base_slitte WHERE prodotto_codice = ?", (p_cod,))
                        for corsa_row in fetch_as_dict(cursor):
                            c_cod = corsa_row['corsa_codice']
                            prezzo_base = float(corsa_row['prezzo'])
                            
                            item_macchina = QStandardItem(f"{p_cod}/{c_cod}")
                            item_macchina.setEditable(False)
                            item_macchina.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                            item_macchina.setData(("configuratore.prezzi_base_slitte", p_cod, c_cod), Qt.ItemDataRole.UserRole)
                            
                            item_prezzo = QStandardItem(f"{prezzo_base:.2f}")
                            item_prezzo.setEditable(True)
                            item_prezzo.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                            root.appendRow([item_macchina, item_prezzo])
                            
                            # Opzioni specifiche della slitta
                            cursor.execute("SELECT opzione_codice, prezzo FROM configuratore.prezzi_opzioni WHERE prodotto_codice = ?", (p_cod,))
                            opzioni = fetch_as_dict(cursor)
                            if opzioni:
                                item_div = QStandardItem("  Opzioni")
                                item_div.setEditable(False)
                                item_div.setForeground(Qt.GlobalColor.darkGray)
                                item_macchina.appendRow([item_div, QStandardItem("")])
                                
                                for op_row in opzioni:
                                    op_cod = op_row['opzione_codice']
                                    desc_op = self.ottieni_descrizione_opzione(op_cod)
                                    item_op = QStandardItem(f"  {desc_op}")
                                    item_op.setEditable(False)
                                    item_op.setData(("configuratore.prezzi_opzioni", p_cod, op_cod), Qt.ItemDataRole.UserRole)
                                    
                                    item_p_op = QStandardItem(f"{float(op_row['prezzo']):.2f}")
                                    item_p_op.setEditable(True)
                                    item_macchina.appendRow([item_op, item_p_op])
            tree.expandAll()
        except Exception as e:
            print(f"Errore foglio Slitte: {e}")
        self.tabs.addTab(tree, "3) Slitte")

    def crea_foglio_tavole(self):
        tree, model = self.crea_albero_base()
        root = model.invisibleRootItem()
        info = QStandardItem("Nessun prodotto tavola configurato nell'archivio attuale.")
        info.setEditable(False)
        root.appendRow([info, QStandardItem("-")])
        self.tabs.addTab(tree, "4) Tavole")

    def registra_modifica(self, item):
        """Intercetta il cambio del valore numerico del prezzo."""
        model = item.model()
        row = item.row()
        # Recuperiamo l'elemento del codice sulla stessa riga (colonna 0)
        sibling_item = model.item(row, 0) if item.column() == 1 else None
        
        if sibling_item and sibling_item.data(Qt.ItemDataRole.UserRole):
            meta = sibling_item.data(Qt.ItemDataRole.UserRole) # (tabella, prodotto, codice)
            nuovo_prezzo = item.text().replace(',', '.') # Gestisce la virgola decimale
            try:
                # Validazione di sicurezza del dato inserito
                valor_float = float(nuovo_prezzo)
                self.modifiche_in_sospeso[meta] = valor_float
                item.setText(f"{valor_float:.2f}") # Uniforma la formattazione a schermo
            except ValueError:
                QMessageBox.critical(self, "Errore", "Valore inserito non valido! Inserire un numero.")

    def salva_tutto(self):
        """Esegue le query di UPDATE sul database in blocco unico transazionale."""
        if not self.modifiche_in_sospeso:
            QMessageBox.information(self, "Info", "Nessuna modifica da salvare.")
            return
            
        try:
            with pyodbc.connect(DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    for meta, nuovo_prezzo in self.modifiche_in_sospeso.items():
                        tabella, prod_cod, comp_cod = meta
                        
                        if tabella == "configuratore.prezzi_base_unita":
                            cursor.execute("""UPDATE configuratore.prezzi_base_unita SET prezzo = ? 
                                            WHERE prodotto_codice = ? AND corsa_codice = ?""", (nuovo_prezzo, prod_cod, comp_cod))
                        elif tabella == "configuratore.prezzi_base_slitte":
                            cursor.execute("""UPDATE configuratore.prezzi_base_slitte SET prezzo = ? 
                                            WHERE prodotto_codice = ? AND corsa_codice = ?""", (nuovo_prezzo, prod_cod, comp_cod))
                        elif tabella == "configuratore.prezzi_opzioni":
                            cursor.execute("""UPDATE configuratore.prezzi_opzioni SET prezzo = ? 
                                            WHERE prodotto_codice = ? AND opzione_codice = ?""", (nuovo_prezzo, prod_cod, comp_cod))
                        elif tabella == "configuratore.prezzi_mandrini":
                            cursor.execute("""UPDATE configuratore.prezzi_mandrini SET prezzo = ? 
                                            WHERE prodotto_codice = ? AND mandrino_codice = ?""", (nuovo_prezzo, prod_cod, comp_cod))
                        elif tabella == "configuratore.prezzi_base_mandrini":
                            cuscinetto, taglia = comp_cod.split('|')
                            cursor.execute("""UPDATE configuratore.prezzi_base_mandrini SET prezzo = ? 
                                            WHERE prodotto_codice = ? AND cuscinetto_codice = ? AND taglia = ?""", (nuovo_prezzo, prod_cod, cuscinetto, taglia))
                    conn.commit()
            QMessageBox.information(self, "Successo", f"Salvate con successo {len(self.modifiche_in_sospeso)} voci di listino!")
            self.modifiche_in_sospeso.clear()
        except Exception as e:
            QMessageBox.critical(self, "Errore di Rete", f"Impossibile salvare i dati su SQL: {e}")

    if __name__ == "__main__":
        app = QApplication(sys.argv)
        # 1. Mostra la richiesta Password
        login = LoginDialog()
        if login.exec() == QDialog.DialogCode.Accepted:
            # 2. Se corretta, apre il listino prezzi
            editor = ListinoEditorWindow()
            editor.show()
            sys.exit(app.exec()) 

                        