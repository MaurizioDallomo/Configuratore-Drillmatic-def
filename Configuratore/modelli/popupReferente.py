from PySide6.QtWidgets import QDialog, QMessageBox
import pyodbc
from gui.popupReferente import Ui_PopupReferente
from modelli.referente import Referente

class UfReferente(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_app = parent
        
        self.ui = Ui_PopupReferente()
        self.ui.setupUi(self)
        
        self.ui.btnOk.clicked.connect(self.interfaccia_aggiungi_referente)
        self.nuovo_ref = None
          
    def interfaccia_aggiungi_referente(self):
        nome = self.ui.tbNome.text().strip()
        cognome = self.ui.tbCognome.text().strip()
        ruolo = self.ui.tbRuolo.text().strip()
        telefono = self.ui.tbTelefono.text().strip()
        cellulare = self.ui.tbCellulare.text().strip()
        email = self.ui.tbEmail.text().strip()

        ref_da_testare = Referente(
        nome=nome,
        cognome=cognome,
        telefono=telefono,
        cellulare=cellulare,
        email=email,
        ruolo=ruolo
    )

        valido, messaggio_errore = ref_da_testare.convalida_dati()
        
        if not valido:
            QMessageBox.warning(self, "Errore di compilazione", messaggio_errore)
            return

        self.nuovo_ref = ref_da_testare
        
        self.ui.tbNome.clear()
        self.ui.tbCognome.clear()
        self.ui.tbRuolo.clear()
        self.ui.tbTelefono.clear()
        self.ui.tbCellulare.clear()
        self.ui.tbEmail.clear()

        self.accept()

    def reject(self):
        self.nuovo_ref = None
        super().reject()
