from gui.popupPosizioneMotore import Ui_Dialog
from PySide6.QtWidgets import QDialog

class UfDefinisciPosizioneMotore(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_app = parent
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.p_confermato = False
        self.posizione_selezionata = None

        self.ui.btn_ok.clicked.connect(self.ok_button_click)
        self.ui.cb_posizione_motore.currentTextChanged.connect(self.cb_posizione_motore_change)

        self.ui.btn_ok.setVisible(False)

        self.ui.cb_posizione_motore.clear()
        self.ui.cb_posizione_motore.addItem("U1")
        self.ui.cb_posizione_motore.addItem("U2")
        self.ui.cb_posizione_motore.addItem("U3")
        self.ui.cb_posizione_motore.addItem("U4")
        self.ui.cb_posizione_motore.addItem("Z1")
        self.ui.cb_posizione_motore.addItem("Z2")
        self.ui.cb_posizione_motore.addItem("Z3")
        self.ui.cb_posizione_motore.addItem("Z4")

    def cb_posizione_motore_change(self):
        if self.ui.cb_posizione_motore.currentText() != "":
            self.ui.btn_ok.setVisible(True)
            self.posizione_selezionata = self.ui.cb_posizione_motore.currentText()
            return self.posizione_selezionata

    def ok_button_click(self):
        self.p_confermato = True
        self.accept()
        
    def reject(self):
        self.posizione_selezionata = None
        self.p_confermato = False
        super().reject()
