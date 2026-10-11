from gui.popupAccessori import Ui_Dialog
from PySide6.QtWidgets import QDialog, QTreeView
from PySide6.QtGui import QStandardItemModel, QStandardItem

class ufAccessori(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_app = parent
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.accessorio_selezionato = None
        self.ui.btn_ok.clicked.connect(self.btn_ok_click)

        model = QStandardItemModel(0, 2)
        model.setHorizontalHeaderLabels(['Codice', 'Descrizione'])

        for accessorio in self.main_app.catalogo.accessori.elenco().values():
            item_codice = QStandardItem(str(accessorio.codice))
            item_desc = QStandardItem(str(accessorio.descrizione)) 

            model.appendRow([item_codice, item_desc])

            self.ui.cb_accessori.setModel(model)

            view = QTreeView()
            view.header().setVisible(True)
            self.ui.cb_accessori.setView(view)

        self.ui.cb_accessori.setCurrentIndex(-1)

    def btn_ok_click(self):
        self.accessorio_selezionato = self.ui.cb_accessori.currentText()
        if not self.accessorio_selezionato == "":
            self.accept()

    def reject(self):
        self.accessorio_selezionato = None
        super().reject()
