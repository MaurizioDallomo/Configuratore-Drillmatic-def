from PySide6.QtWidgets import QDialog
from gui.popupTaglia import Ui_PopUpTaglia 
from modelli.motore import Motore

class UfDefinisciTaglia(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_app = parent
        
        self.ui = Ui_PopUpTaglia()
        self.ui.setupUi(self)
        
        self.p_confermato = False
        self.motore_creato = None

        self.ui.OkButton.clicked.connect(self.ok_button_click)
        self.ui.cbTaglia.currentTextChanged.connect(self.cb_taglia_change)

        self.ui.OkButton.setVisible(False)

    def genera_taglia(self):
        self.ui.cbTaglia.clear()
        for v in self.main_app.passa_taglie.values():
            self.ui.cbTaglia.addItem(str(v))

    def cb_taglia_change(self):
        if self.ui.cbTaglia.currentText() != "":
            self.ui.OkButton.setVisible(True)

    def ok_button_click(self):
        self.p_confermato = True
        self.motore_creato = self.crea_motore_personalizzato()
        self.accept() 

    def crea_motore_personalizzato(self) -> Motore:
        motore_personalizzato = Motore()
        valore_taglia = self.ui.cbTaglia.currentText()
        
        motore_personalizzato.grandezza = valore_taglia
        motore_personalizzato.grandezza_descr = valore_taglia
        motore_personalizzato.testo_agg = "da definire"
        
        return motore_personalizzato

    def reject(self):
        self.motore_creato = None
        self.p_confermato = False
        super().reject()
