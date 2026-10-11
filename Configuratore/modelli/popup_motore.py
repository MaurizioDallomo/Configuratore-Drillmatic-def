from modelli.motore import Motore
from gui.popupMotoreSpeciale import Ui_PopUpMotoreSpeciale
from PySide6.QtWidgets import QDialog, QMessageBox

class UfMotoreSpeciale(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_app = parent 
        
        self.ui = Ui_PopUpMotoreSpeciale()
        self.ui.setupUi(self)

        self.mot_sel = self.main_app.motore_selezionato
        self.vel_sel = self.main_app.velocita_selezionata
        self.taglia_selezionata = self.ui.cbTaglia.currentText()
                
        self.p_potenze_motore = {}
        self.p_poli_motore = {}
        self.motore_creato = None
        self.p_confermato = False
        self.p_prodotto = None

        self.connetti_eventi()

    def connetti_eventi(self):
        self.ui.OkButton.clicked.connect(self.cb_genera_motore_click)
        self.ui.cbTaglia.currentTextChanged.connect(self.cb_taglia_change)
        self.ui.cbPotenza.currentIndexChanged.connect(self.popola_poli)
        
    def cb_taglia_change(self):
        self.ui.cbTaglia.blockSignals(True)
        self.ui.cbPotenza.blockSignals(True)

        self.ui.cbPotenza.setVisible(True)
        self.ui.cbPotenza.clear()
        self.ui.cbPoli.setVisible(True)
        self.popola_potenze()

        self.ui.cbPotenza.blockSignals(False)
        self.ui.cbTaglia.blockSignals(False)

    def cb_genera_motore_click(self):
        self.motore_creato = self.crea_motore_personalizzato()
        self.p_confermato = True
        self.accept() 

    def verifica_motori_disponibili(self) -> bool:
        array_taglie = ["80", "90", "100", "112", "132", "160", "180"]
        elenco_taglie = {taglia: taglia for taglia in self.main_app.passa_taglie.keys()}
        
        if hasattr(self, 'p_prodotto') and self.p_prodotto and self.p_prodotto.max_taglia_motore:
            max_taglia = int(self.p_prodotto.max_taglia_motore)
            for taglia_array in array_taglie:
                if int(taglia_array) <= max_taglia:
                    elenco_taglie[taglia_array] = taglia_array

        for motore in self.main_app.catalogo.motori_maggiorati.elementi.values():
            if motore.grandezza in elenco_taglie:
                if not self.vel_sel.codice == "xxx":
                    if self.mot_sel.poli == motore.poli:
                        return True 
                else:
                    return True 
                    
        return False 
    
    def popola_potenze(self):
        self.taglia_selezionata = self.ui.cbTaglia.currentText()

        if self.taglia_selezionata == "":
            return

        self.p_potenze_motore = {}

        for motore in self.main_app.catalogo.motori_maggiorati.elementi.values():
            if self.taglia_selezionata == motore.grandezza:
                if not self.vel_sel.codice == "xxx":
                    if self.mot_sel.poli == motore.poli:
                        if motore.potenza not in self.p_potenze_motore:
                            self.p_potenze_motore[motore.potenza] = motore.potenza
                else:
                    if motore.potenza not in self.p_potenze_motore:
                        self.p_potenze_motore[motore.potenza] = motore.potenza

        for potenza in self.p_potenze_motore.values():
            self.ui.cbPotenza.addItem(str(potenza))
            self.ui.cbPotenza.setCurrentIndex(-1)

        self.ui.cbTaglia.blockSignals(False)

    def popola_poli(self):

        self.ui.cbPoli.clear()
        self.ui.cbPoli.setCurrentIndex(-1)

        if self.vel_sel.codice == "xxx":
        
            potenza_selezionata = self.ui.cbPotenza.currentText()
            if potenza_selezionata == "":
                return

            self.p_poli_motore = {"": ""}

            for motore in self.main_app.catalogo.motori_maggiorati.elementi.values():
                if potenza_selezionata == motore.potenza:
                    if self.taglia_selezionata == motore.grandezza:
                        if motore.poli not in self.p_poli_motore:
                            self.p_poli_motore[motore.poli] = motore.poli

            for poli in self.p_poli_motore.values():
                self.ui.cbPoli.addItem(str(poli))
        else:
            self.ui.cbPoli.addItem(str(self.mot_sel.poli))
            
    def crea_motore_personalizzato(self) -> Motore:
        motore_personalizzato = Motore()
        
        motore_personalizzato.testo_agg = "maggiorato"
        motore_personalizzato.grandezza = self.ui.cbTaglia.currentText()
        motore_personalizzato.grandezza_descr = self.ui.cbTaglia.currentText()
        motore_personalizzato.potenza = self.ui.cbPotenza.currentText()
        motore_personalizzato.poli = self.ui.cbPoli.currentText()

        opzione = self.main_app.opzione_passata 
        if opzione == "motore_autofrenante_magg":
            motore_personalizzato.freno = " autofrenante"
                 
        return motore_personalizzato

    def genera_taglia(self, p):
        self.ui.cbTaglia.blockSignals(True)

        self.p_prodotto = p
        array_taglie = ["80", "90", "100", "112", "132", "160", "180"]
        opzione = self.main_app.opzione_passata

        elenco_taglie = {}
        
        for taglia_passata in self.main_app.passa_taglie.keys():
            elenco_taglie[taglia_passata] = taglia_passata

        self.ui.cbTaglia.clear()
        for taglia_passata in elenco_taglie.values():
            self.ui.cbTaglia.addItem(str(taglia_passata))

        prima_taglia_lista = self.ui.cbTaglia.itemText(0) if self.ui.cbTaglia.count() > 0 else "0"

        for taglia_array in array_taglie:
            max_taglia = int(p.max_taglia_motore) if p.max_taglia_motore else 0
            
            if int(taglia_array) <= max_taglia:
                if int(taglia_array) >= int(prima_taglia_lista):
                    if taglia_array not in elenco_taglie:
                        elenco_taglie[taglia_array] = taglia_array

        self.ui.cbTaglia.clear()
        for taglia in elenco_taglie.keys():
            self.ui.cbTaglia.addItem(str(taglia))

        self.ui.cbTaglia.blockSignals(False)
        self.cb_taglia_change()

    def reject(self):
        self.motore_creato = None
        self.p_confermato = False
        super().reject()
