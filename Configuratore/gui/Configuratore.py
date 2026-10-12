import pyodbc
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QMessageBox, QDialog, QInputDialog, QComboBox, QLabel, QTableWidgetItem, QFileDialog, QWidget, QVBoxLayout, QWidget
from gui.popupUserform import Ui_MainWindow
from modelli.enums import TipovariabileObbligatoria, DestinazioneOpzione, ComportamentoOpzione, MacroCategorie
from archivi.catalogo import Catalogo
from modelli.cliente import Cliente
from modelli.referente import Referente
from modelli.preventivo_riga import Preventivo_riga
from modelli.preventivo import Preventivo
from modelli.popup_motore import UfMotoreSpeciale
from modelli.popupOpzione_speciale import ufOpzione
from modelli.popup_accessori import ufAccessori
from modelli.popup_taglia import UfDefinisciTaglia
from modelli.popupReferente import UfReferente
from modelli.popup_preventivo import UfPreventivo
from modelli.popupPosizioneMotore import UfDefinisciPosizioneMotore
import copy
import os
import re
from decimal import Decimal
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime, date
from listino.gestione_listino import LoginDialog, ListinoEditorWindow
import configparser
import sys
from config_loader import D_HOST, D_NAME, D_USER, D_PASS, DB_CONFIG, risorsa_percorso

def disegna_grafica_preventivo(canvas, doc):
    canvas.saveState()

    # --- INTESTAZIONE (In alto) ---
    # x=36 (margine sinistro), y=720 (bordo superiore del foglio), width=540 (larghezza totale utile)
    percorso_logo = risorsa_percorso("Immagini/intestazione.png")
    
    if os.path.exists(percorso_logo):
        img = ImageReader(percorso_logo)
        larghezza_originale, altezza_originale = img.getSize()
    
        larghezza_desiderata = 80
    
        altezza_proporzionale = (altezza_originale / larghezza_originale) * larghezza_desiderata
    
        canvas.drawImage(percorso_logo, 30, 700, width=larghezza_desiderata, height=altezza_proporzionale)

    # --- PIÈ DI PAGINA (In basso) ---
    # x=36, y=20 (bordo inferiore del foglio)
    percorso_footer = risorsa_percorso("Immagini/pie_pagina.png")
    
    if os.path.exists(percorso_footer):
        canvas.drawImage(percorso_footer, 36, 20, width=540, height=40)
        
    canvas.restoreState()

class Configuratore(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ###############################
        # per ridimensionare lo schermo
        ###############################
        self.setWindowState(Qt.WindowState.WindowMaximized)
        self.layout().setSizeConstraint(QVBoxLayout.SetMinAndMaxSize) if self.layout() else None
                
        self.catalogo = Catalogo()
        self.catalogo.carica()
        
        self.descrizione_da_sostituire = None
        self.descrizione_base_originale_vite = None
        self.descrizione_base_originale_scorrimento = None
        self.descrizione_base_originale_posizione_motore_brushless = None
        self.descrizione_base_originale_posizione_motore_mandrino = None
        self.descrizione_base_originale_flangia_motore_rinviato = None
        self.posizione_motore_selezionata = None
        self.motore_selezionato = None
        self.velocita_selezionata = None
        self.prodotto_selezionato = None
        self.famiglia_selezionata = None
        self.corsa_selezionata = None
        self.mandrino_selezionato = None
        self.trasmissione_selezionata = None
        self.cuscinetto_selezionato = None
        self.aggiornamento_in_corso = False
        self.salta_trasmissione = False
        self.salta_sbloccaggio = False
        self.salta_evita_selezioni_multiple = False
        self.descrizione = ""
        self.descrizioni_aggiuntive = {}
        self.valore_attuale = ""
        self.motore_speciale = None
        self.motore_da_definire = None
        self.passa_taglie = {}
        self.opzione_passata = ""
        self.referenti_temporanei = [] 
        self.opzioni_temporanee = []
        self.modalita_cliente = None
        self.id_preventivo_corrente = None
        self.codice_preventivo_corrente = None
        self.carica_opzioni_combobox()

        self.categorie = ["Costruttore", "Utilizzatore", "Studio tecnico", "Rivenditore", "Partner", "Altro"]
        self.resa_merce = ["EXW", "FCA", "FAS", "FOB", "CFR", "CIF", "CPT", "CIP", "DAP", "DPU", "DDP"]
        self.imballo = ["1,2%", "al costo"]
        self.ui.cbCategoria.clear()
        self.ui.cbResa.clear()
        self.ui.cbImballo.clear()
        self.ui.cbCategoria.addItems(self.categorie)
        self.ui.cbResa.addItems(self.resa_merce)
        self.ui.cbImballo.addItems(self.imballo)
        self.ui.cbCategoria.setCurrentIndex(-1)
        self.ui.cbResa.setCurrentIndex(-1)
        self.ui.cbCliente.setCurrentIndex(-1)
        self.ui.cbImballo.setCurrentIndex(-1)

        self.inizializza_form()
        self.reset_condizioni()
        self.connetti_eventi()

        self.ui.frmCliente.setEnabled(False)
        self.ui.btn_modifica.setEnabled(False)
        self.ui.btn_salva.setEnabled(False)

    def carica_opzioni_combobox(self):
        try:
            connessione = pyodbc.connect(
                "Driver={ODBC Driver 18 for SQL Server};"
                f"Server={D_HOST};"
                f"Database={D_NAME};"  # Usiamo la variabile dinamica invece del nome fisso
                f"UID={D_USER};"       # Inserisce l'utente del file config.ini
                f"PWD={D_PASS};"       # Inserisce la password del file config.ini
                "TrustServerCertificate=yes;"
            )

            cursore = connessione.cursor()

            cursore.execute("SELECT descrizione FROM configuratore.opzioni_pagamento ORDER BY descrizione ASC")
            pagamenti = [riga[0] for riga in cursore.fetchall()]
            
            self.ui.cbPagamento.clear()
            self.ui.cbPagamento.addItems(pagamenti)
            self.ui.cbPagamento.setCurrentIndex(-1) 

            cursore.execute("SELECT nome_corriere FROM configuratore.opzioni_trasporto ORDER BY nome_corriere ASC")
            trasporti = [riga[0] for riga in cursore.fetchall()]
            
            self.ui.cbTrasporto.clear()
            self.ui.cbTrasporto.addItems(trasporti)
            self.ui.cbTrasporto.setCurrentIndex(-1)

            cliente_corrente = self.ui.cbCliente.currentText()

            cursore.execute("SELECT ragione_sociale FROM configuratore.clienti ORDER BY ragione_sociale ASC")
            clienti = [riga[0] for riga in cursore.fetchall()]

            self.ui.cbCliente.clear()
            self.ui.cbCliente.addItems(clienti)

            if cliente_corrente and cliente_corrente in clienti:
                self.ui.cbCliente.setCurrentText(cliente_corrente)
            else:
                self.ui.cbCliente.setCurrentIndex(-1)

            cursore.close()
            connessione.close()

        except Exception as e:
            QMessageBox.critical(self, "Errore Caricamento Dati", f"Impossibile caricare le opzioni di pagamento o trasporto:\n{e}")
             

    def inizializza_form(self):
        for p in self.catalogo.prodotti.elementi.values():
            self.ui.cbProdotto.addItem(p.codice)   
            self.ui.cbProdotto.setCurrentIndex (-1)
        
    def connetti_eventi(self):
        for i in range(1, self.catalogo.opzioni.numero_opzioni() + 1):
            widget = getattr(self.ui, f"ck{i}", None)
            if widget:
                widget.clicked.connect(lambda checked, w=widget: self.evento_checkbox_generico(w))

        self.ui.btn_opzione_speciale1.clicked.connect(lambda: self.evento_checkbox_generico(self.ui.btn_opzione_speciale1))
        self.ui.btn_opzione_speciale2.clicked.connect(lambda: self.evento_checkbox_generico(self.ui.btn_opzione_speciale2))
        self.ui.btn_opzione_speciale3.clicked.connect(lambda: self.evento_checkbox_generico(self.ui.btn_opzione_speciale3))
        self.ui.cbProdotto.currentIndexChanged.connect(self.cbProdotto_click)
        self.ui.cbOpzione1.currentIndexChanged.connect(self.cbOpzione1_click)
        self.ui.cbOpzione2.currentIndexChanged.connect(self.cbOpzione2_click)
        self.ui.cbOpzione3.currentIndexChanged.connect(self.cbOpzione3_click)
        self.ui.cbOpzione4.currentIndexChanged.connect(self.cbOpzione4_click)
        self.ui.btn_agg_referente.clicked.connect(self.aggiungi_referente)
        self.ui.btn_elim_referente.clicked.connect(self.elimina_referente)
        self.ui.btn_salva.clicked.connect(self.salva_cliente)
        self.ui.btn_nuovo.clicked.connect(self.inserisci_nuovo_cliente)
        self.ui.btn_modifica.clicked.connect(self.modifica_cliente)
        self.ui.cbCliente.currentIndexChanged.connect(self.cbCliente_click)
        self.ui.btn_sposta_giu.clicked.connect(self.btn_sposta_giu_click)
        self.ui.btn_sposta_su.clicked.connect(self.btn_sposta_su_click)
        self.ui.btn_elimina_riga.clicked.connect(self.btn_elimina_riga_click)
        self.ui.btn_aggiungi_prodotto.clicked.connect(self.btn_aggiungi_prodotto_click)
        self.ui.btn_aggiungi_accessorio.clicked.connect(self.btn_aggiungi_accessorio_click)
        self.ui.btn_aggiungi_testo.clicked.connect(self.btn_aggiungi_testo_click)
        self.ui.btn_genera_preventivo.clicked.connect(self.genera_preventivo)
        self.ui.btn_carica_preventivo.clicked.connect(self.carica_preventivo)
        self.ui.btn_elimina_preventivo.clicked.connect(self.elimina_preventivo)
        self.ui.btn_listino.clicked.connect(self.apri_listino)
                
    def gestisci_apertura_o_reset_bottone(self, btn):
        if not btn.property("is_red"):
            uf = ufOpzione(self)
            if uf.exec() == QDialog.Accepted:
                self.opzioni_temporanee.append(uf.nuova_opzione)
                btn.setText(uf.nuova_opzione.codice)
                btn.setProperty("is_red", True)
                btn.setStyleSheet("background-color: red; color: white;")
        else:
            btn.setProperty("is_red", False)
            
    def evento_checkbox_generico(self, mittente = None):
        if mittente is None:
            mittente = self.sender()

        ckb_passata = None
        btn_passato = None

        if mittente.objectName().startswith("ck"):
            ckb_passata = mittente
        elif mittente.objectName().startswith("btn_opzione_speciale"):
            btn_passato = mittente
            self.gestisci_apertura_o_reset_bottone(btn_passato)

        self.aggiorna_opzione(ckb=ckb_passata, btn=btn_passato)
        self.casi_speciali()
        self.aggiorna_prezzo_prodotto(self.ui.cbOpzione1, self.ui.cbOpzione2, self.ui.cbOpzione4)

    def cbOpzione1_click(self):
        if self.aggiornamento_in_corso: return
        layout = self.famiglia_selezionata.macro_categoria.layout_variabili
        self.filtra_motorizzazioni(self.ui.cbOpzione1, self.ui.cbOpzione2, layout.opzione1, self.prodotto_selezionato)
        self.descrizione_opzione(layout.opzione1, self.ui.cbOpzione1.currentText())
        self.aggiorna_prodotto()
        self.consenso_offerta()
        self.aggiorna_prezzo_prodotto(self.ui.cbOpzione1, self.ui.cbOpzione2, self.ui.cbOpzione4)

    def cbOpzione2_click(self):
        if self.aggiornamento_in_corso: return
        layout = self.famiglia_selezionata.macro_categoria.layout_variabili
        self.filtra_motorizzazioni(self.ui.cbOpzione2, self.ui.cbOpzione1, layout.opzione2, self.prodotto_selezionato)
        self.descrizione_opzione(layout.opzione2, self.ui.cbOpzione2.currentText())
        self.aggiorna_prodotto()
        self.consenso_offerta()
        self.aggiorna_prezzo_prodotto(self.ui.cbOpzione1, self.ui.cbOpzione2, self.ui.cbOpzione4)

    def cbOpzione3_click(self):
        if self.aggiornamento_in_corso: return
        layout = self.famiglia_selezionata.macro_categoria.layout_variabili
        self.filtra_motorizzazioni(self.ui.cbOpzione3, self.ui.cbOpzione4, layout.opzione3, self.prodotto_selezionato)
        self.descrizione_opzione(layout.opzione3, self.ui.cbOpzione3.currentText())
        self.aggiorna_prodotto()
        self.consenso_offerta()
        self.aggiorna_prezzo_prodotto(self.ui.cbOpzione1, self.ui.cbOpzione2, self.ui.cbOpzione4)

    def cbOpzione4_click(self):
        if self.aggiornamento_in_corso: return
        layout = self.famiglia_selezionata.macro_categoria.layout_variabili
        self.filtra_motorizzazioni(self.ui.cbOpzione4, self.ui.cbOpzione3, layout.opzione4, self.prodotto_selezionato)
        self.descrizione_opzione(layout.opzione4, self.ui.cbOpzione4.currentText())
        self.aggiorna_prodotto()
        self.consenso_offerta()
        self.aggiorna_prezzo_prodotto(self.ui.cbOpzione1, self.ui.cbOpzione2, self.ui.cbOpzione4)

    def cbProdotto_click(self):
        if not self.ui.cbProdotto.currentText(): return
        self.reset_condizioni()

        self.prodotto_selezionato = self.catalogo.prodotti.get_prodotto(self.ui.cbProdotto.currentText())
        self.famiglia_selezionata = self.prodotto_selezionato.famiglia
        self.descrizioni_aggiuntive = {}

        layout = self.famiglia_selezionata.macro_categoria.layout_variabili
        self.popola_combo(self.ui.cbOpzione1, self.ui.lbOpzione1, layout.opzione1, self.prodotto_selezionato)
        self.popola_combo(self.ui.cbOpzione2, self.ui.lbOpzione2, layout.opzione2, self.prodotto_selezionato)
        self.popola_combo(self.ui.cbOpzione3, self.ui.lbOpzione3, layout.opzione3, self.prodotto_selezionato)
        self.popola_combo(self.ui.cbOpzione4, self.ui.lbOpzione4, layout.opzione4, self.prodotto_selezionato)

    def reset_condizioni(self):
        self.motore_selezionato = None
        self.velocita_selezionata = None

        # ufDefinisciTaglia.reset_taglie() 
        self.passa_taglie.clear()

        for i in range(1, 5):
            combo = getattr(self.ui, f"cbOpzione{i}", None)
            if combo: 
                combo.setVisible(False)

        if hasattr(self.ui, "frmConfiguratore"):
            for widget in self.ui.frmConfiguratore.findChildren(QWidget):
                class_name = widget.metaObject().className()
                
                if class_name == "QCheckBox":
                    widget.setVisible(False)
                    widget.setChecked(False)
                    widget.setEnabled(True)
                    
                elif class_name == "QLineEdit":
                    widget.clear()
                    
                elif class_name == "QPlainTextEdit":
                    widget.clear()
                    
                elif class_name == "QPushButton":
                    widget.setEnabled(False)
                    widget.setVisible(False)
                    
                elif class_name == "QLabel":
                    widget.setText("")
                    widget.setEnabled(True)

        if hasattr(self.ui, "lbProdotto"):
            self.ui.lbProdotto.setText("Prodotto")

        self.ui.btn_opzione_speciale1.setProperty("is_red", False)
        self.ui.btn_opzione_speciale2.setProperty("is_red", False)
        self.ui.btn_opzione_speciale3.setProperty("is_red", False)
        self.ui.btn_opzione_speciale1.setStyleSheet("")
        self.ui.btn_opzione_speciale2.setStyleSheet("")
        self.ui.btn_opzione_speciale3.setStyleSheet("")
        self.ui.btn_opzione_speciale1.setText("Aggiungi opzione speciale")
        self.ui.btn_opzione_speciale2.setText("Aggiungi opzione speciale")
        self.ui.btn_opzione_speciale3.setText("Aggiungi opzione speciale")
        self.opzioni_temporanee.clear()
                                        
    def popola_combo(self, cb: QComboBox, lb: QLabel, tipo: TipovariabileObbligatoria, p):

        index_pieno = self.aggiornamento_in_corso
        self.aggiornamento_in_corso = True

        cb.clear()

        if tipo == TipovariabileObbligatoria.Corse:
            lb.setText("Corse")
            for k in p.corse.values():
                cb.setVisible(True)
                cb.setEnabled(True)
                cb.addItem(k.codice)
                cb.setProperty("tag", "cbCorsa")
                
        elif tipo == TipovariabileObbligatoria.Motori:
            lb.setText("Motori")
            for k in p.motori(self.catalogo).values():
                cb.setVisible(True)
                cb.setEnabled(True)
                cb.addItem(k.codice)
                cb.setProperty("tag", "cbMotore")

        elif tipo == TipovariabileObbligatoria.Velocita:
            lb.setText("Velocità")
            for k in p.velocita(self.catalogo).values():
                cb.setVisible(True)
                cb.setEnabled(True)
                cb.addItem(k.codice)
                cb.setProperty("tag", "cbVelocita")

        elif tipo == TipovariabileObbligatoria.Mandrini:
            lb.setText("Mandrini")
            for k in p.mandrini.values():
                cb.setVisible(True)
                cb.setEnabled(True)
                cb.addItem(k.codice)
                cb.setProperty("tag", "cbMandrino")

        elif tipo == TipovariabileObbligatoria.Cuscinetti:
            lb.setText("Cuscinetti")
            for k in p.cuscinetti.values():
                cb.setVisible(True)
                cb.setEnabled(True)
                cb.addItem(k.codice)
                cb.setProperty("tag", "cbCuscinetto")

        cb.setCurrentIndex (-1)
        self.aggiornamento_in_corso = index_pieno


    def filtra_motorizzazioni(self, cb, cb2, tipo, p):

        if self.aggiornamento_in_corso:
            return

        self.aggiornamento_in_corso = True
        
        # ------------------------------------------------------------------------------------------
        # SALVO IL VALORE PRECEDENTEMENTE SELEZIONATO NELLA COMBOBOX DI RIFERIMENTO (MOTORE O VELOCITA')
        # ------------------------------------------------------------------------------------------
        self.valore_attuale = cb2.currentText()

        # -------------------------------
        # MODIFICO LA COMBOBOX VELOCITA'
        # -------------------------------
        if tipo == TipovariabileObbligatoria.Velocita:
            opz = DestinazioneOpzione.Velocita 

            self.passa_taglie.clear()

            cb2.clear()

            # ----------------------------------------------------------------------------------------
            # SELEZIONO UNA VELOCITA' STANDARD E IN FUNZIONE DI QUESTA CARICO I MOTORI SELEZIONABILI
            # ----------------------------------------------------------------------------------------
            if cb.currentText() != "xxx":
                self.abilita_cb(opz)
                
                for m in p.motori_selezionabili(self.catalogo, cb.currentText()).values():
                    cb2.addItem(m.codice)
                    
                    # ------------------------------------------------------
                    # PASSO LA TAGLIA DI TUTTI I MOTORI SELEZIONABILI
                    # ------------------------------------------------------
                    if m.grandezza not in self.passa_taglie:
                        if m.grandezza != "":
                            self.passa_taglie[m.grandezza] = m.grandezza
                
                # ---------------------------------------------------------------------
                # SE MOTORE ERA PIENA, LA RIMETTO. SE NO IMPOSTO L'INDEX VUOTO
                # ---------------------------------------------------------------------
                if self.valore_attuale == "":
                    cb2.setCurrentIndex(-1)
                else:
                    cb2.setCurrentText(self.valore_attuale)
                
            # ----------------------------------------------------------------------------------------
            # SE INVECE SELEZIONO VELOCITA' DA DEFINIRE, CARICO TUTTI I MOTORI RELATIVI AL PRODOTTO
            # ----------------------------------------------------------------------------------------
            else:
                for m in p.motori(self.catalogo).values():
                    cb2.addItem(m.codice)
                    
                    # ------------------------------------------------------
                    # PASSO LA TAGLIA DI TUTTI I MOTORI RELATIVI AL PRODOTTO
                    # ------------------------------------------------------
                    if m.grandezza not in self.passa_taglie:
                        if m.grandezza != "":
                            self.passa_taglie[m.grandezza] = m.grandezza
                            
                # ---------------------------------------------------------------------
                # SE MOTORE ERA PIENA, LA RIMETTO. SE NO IMPOSTO L'INDEX VUOTO
                # ---------------------------------------------------------------------
                if self.valore_attuale == "":
                    cb2.setCurrentIndex(-1)
                else:
                    cb2.setCurrentText(self.valore_attuale)

        # ----------------------------
        # MODIFICO LA COMBOBOX MOTORI
        # ----------------------------
        elif tipo == TipovariabileObbligatoria.Motori:
            opz = DestinazioneOpzione.Motore

            # cb2.Clear
            cb2.clear()
            
            # --------------------------------------------------------------
            # SELEZIONO UN MOTORE STANDARD E DEFINISCO IL MOTORE SELEZIONATO
            # --------------------------------------------------------------
            if cb.currentText() != "xxx":
                self.motore_selezionato = copy.deepcopy(self.catalogo.motori.get_motore(cb.currentText()))
                self.motore_selezionato.descrizione = self.motore_selezionato.dati_motore()

                # ------------------------------------------------------------------------
                # ABILITO TUTTE LE OPZIONI LEGATE AL FATTO CHE IL MOTORE SCELTO E' STANDARD
                # ------------------------------------------------------------------------
                self.abilita_cb(opz)
                
                # ---------------------------------------------------------------------
                # IN BASE AL MOTORE STANDARD SCELTO, CARICO LE VELOCITA' SELEZIONABILI
                # ---------------------------------------------------------------------
                for v in p.velocita_selezionabili(self.catalogo, cb.currentText()).values():
                    cb2.addItem(v.codice)

                # ---------------------------------------------------------------------
                # SE LA VELOCITA' ERA PIENA, LA RIMETTO. SE NO IMPOSTO L'INDEX VUOTO
                # ---------------------------------------------------------------------
                if self.valore_attuale == "":
                    cb2.setCurrentIndex(-1)
                else:
                    cb2.setCurrentText(self.valore_attuale)
                                
            else:
                # ------------------------------------------------------
                # SE LA VELOCITA' NON E' ANCORA STATA SELEZIONATA, PASSO LA TAGLIA DI TUTTI I MOTORI RELATIVI AL PRODOTTO
                # ALTRIMENTI PASSO LA TAGLIA DEI MOTORI RELATIVI ALLA VELOCITA' SELEZIONATA
                # ------------------------------------------------------
                if self.valore_attuale == "":
                    for m in p.motorizzazioni.values():
                        if m.motore.grandezza not in self.passa_taglie:
                            self.passa_taglie[m.motore.grandezza] = m.motore.grandezza
                else:
                    for m in p.motorizzazioni.values():
                        if m.velocita.codice == self.valore_attuale:
                            if m.motore.grandezza not in self.passa_taglie:
                                self.passa_taglie[m.motore.grandezza] = m.motore.grandezza

                # ------------------------------------
                # DEFINISCO IL MOTORE SELEZIONATO XXX
                # ------------------------------------
                self.motore_selezionato = copy.deepcopy(self.catalogo.motori.get_motore(cb.currentText()))
                self.motore_selezionato.descrizione = self.motore_selezionato.dati_motore()
                
                # ----------------------------------------------------------------------
                # CARICO IL MOTORE DA DEFINIRE E GLI ASSEGNO TUTTE LE DESCRIZIONI CREATE
                # ----------------------------------------------------------------------
                self.crea_motore_da_definire()
                
                if self.motore_da_definire is not None:
                    self.motore_selezionato.grandezza = self.motore_da_definire.grandezza
                    self.motore_selezionato.grandezza_descr = self.motore_da_definire.grandezza_descr
                    self.motore_selezionato.testo_agg = self.motore_da_definire.testo_agg
                    self.motore_selezionato.descrizione = self.motore_selezionato.dati_motore()

                # -----------------------------------------------------------------------------------------------------------------------
                # ORA CHE HO IL MOTORE SELEZIONATO XXX CON LA TAGLIA ASSOCIATA, SELEZIONO LE VELOCITA' IN FUNZIONE DELLA GRANDEZZA MOTORE
                # -----------------------------------------------------------------------------------------------------------------------
                for v in p.velocita_selezionabili_da_taglia(self.catalogo, self.motore_selezionato.grandezza).values():
                    cb2.addItem(v.codice)

                # ---------------------------------------------------------------------
                # SE LA VELOCITA' ERA PIENA, LA RIMETTO. SE NO IMPOSTO L'INDEX VUOTO
                # ---------------------------------------------------------------------
                                    
                if self.valore_attuale == "":
                    cb2.setCurrentIndex(-1)
                else:
                    cb2.setCurrentText(self.valore_attuale)

        self.aggiornamento_in_corso = False        

    def consenso_offerta(self):
        for i in range(1, 5):
            combo = getattr(self.ui, f"cbOpzione{i}", None)
            if combo and combo.isVisible() and combo.currentText() == "":
                return

            if combo and combo.property("tag") == "cbVelocita" and combo.currentText() != "":
                vel_in_combo = combo.currentText()
                vel = self.catalogo.velocita.get_velocita(vel_in_combo).descrizione
                vel_estratta = re.search(r'\d+', vel)
                if vel_estratta:
                    numero = int(vel_estratta.group())

                    if numero > 3000:
                        for i in range(1, 5):
                            combo_cusc = getattr(self.ui, f"cbOpzione{i}", None)
                            if combo_cusc and combo_cusc.currentText() == "RC":
                                QMessageBox.warning(self, "Configurazione a rischio", "Velocità non idonea per cuscinetti RC")
                                return

        self.ui.btn_opzione_speciale1.setVisible(True)
        self.ui.btn_opzione_speciale2.setVisible(True)
        self.ui.btn_opzione_speciale3.setVisible(True)
        self.ui.btn_opzione_speciale1.setEnabled(True)
        self.ui.btn_opzione_speciale2.setEnabled(True)
        self.ui.btn_opzione_speciale3.setEnabled(True)
        self.ui.btn_aggiungi_prodotto.setEnabled(True)
        self.ui.btn_aggiungi_accessorio.setEnabled(True)
        self.ui.btn_aggiungi_testo.setEnabled(True)
        self.ui.tb_righe.setEnabled(True)
                
        self.popola_opzioni()
        self.soffietti()
        self.dx38l()
        self.applica_riduttore()

    def dx38l(self):
        if self.prodotto_selezionato.codice == "DX38L":
            for i in range(1, self.catalogo.opzioni.numero_opzioni() + 1):
                ck = getattr(self.ui, f"ck{i}", None)
                if ck and ck.property("tag") == "sbloccaggio_pneumatico":
                    ck.setChecked(True)
                    self.evento_checkbox_generico(ck)
                    break

    def applica_riduttore(self):
        for i in range(1, self.catalogo.opzioni.numero_opzioni() + 1):
            ck = getattr(self.ui, f"ck{i}", None)
            lb = getattr(self.ui, f"opzione{i}", None)
            if ck and lb and lb.text() == "Riduttore di velocità":
                if self.trasmissione_selezionata.codice == "catena_riduttore":
                    ck.setChecked(True)
                    ck.setEnabled(False)
                    self.evento_checkbox_generico(ck)
                    break
                else:
                    ck.setChecked(False)
                    ck.setEnabled(True)
                    self.evento_checkbox_generico(ck)
                    break
                                            
    def popola_opzioni(self):
        opz_tot = self.prodotto_selezionato.opzioni_totali()
        i = 1

        for op in opz_tot.values():
            if not self.catalogo.listino.salta_opzione(self.prodotto_selezionato, op):
                
                ck = getattr(self.ui, f"ck{i}", None)
                lbl = getattr(self.ui, f"opzione{i}", None)
                
                if ck:
                    ck.setVisible(True)
                    ck.setProperty("tag", op.codice)
                if lbl:
                    lbl.setVisible(True)
                    lbl.setText(op.voce_ck)

                i += 1

        self.motore_autofrenante()
        self.disabilita_cb()

    
#########################################################################################
# ----------------- GESTIONE DESCRIZIONE E CODICE ARTICOLO ------------------------------
#########################################################################################

    def genera_codice(self):
        elenco_codici = [] 
        codice_articolo = f"{self.prodotto_selezionato.codice}/"

        for i in range(1, 5):
            combo = getattr(self.ui, f"cbOpzione{i}", None)
            if combo and combo.isVisible():
                if combo.isEnabled():
                    cod = f"{combo.currentText()}/"
                    elenco_codici.append(cod)
                else:
                    if self.prodotto_selezionato.famiglia.codice == "TX":
                        cod = f"{combo.currentText()}/"
                        elenco_codici.append(cod)
                    else:
                        cod = "xxx/"
                        elenco_codici.append(cod)

        for c in elenco_codici:
            codice_articolo += c

        if codice_articolo.endswith("/"):
            codice_articolo = codice_articolo[:-1]

        if hasattr(self.ui, "tbCodice"):
            self.ui.tbCodice.setText(codice_articolo)

    def genera_descrizione(self):
        testo_con_spazi = f"{self.famiglia_selezionata.descrizione_base}\n{self.posizione_descrizioni(self.famiglia_selezionata.macro_categoria.nome)}"

        for desc in self.prodotto_selezionato.descrizioni(self.descrizione_base_originale_vite):
            if desc:
                testo_con_spazi += f"{desc}\n"

        for desc_agg in self.descrizioni_aggiuntive.values():
            testo_con_spazi += f"{desc_agg}\n"

        self.descrizione = "\n".join(r.strip() for r in testo_con_spazi.split("\n") if r.strip() and r.strip() != "None")

        if hasattr(self.ui, "tbDescrizione"):
            self.ui.tbDescrizione.setPlainText(self.descrizione)

    def descrizione_opzione(self, tipo, v):
        if tipo == TipovariabileObbligatoria.Corse:
            self.corsa_selezionata = self.catalogo.corse.get_corsa(v)

        elif tipo == TipovariabileObbligatoria.Mandrini:
            self.mandrino_selezionato = self.catalogo.mandrini.get_mandrino(v)

        elif tipo == TipovariabileObbligatoria.Velocita:
            self.velocita_selezionata = copy.deepcopy(self.catalogo.velocita.get_velocita(v))
            self.trasmissione()

        elif tipo == TipovariabileObbligatoria.Cuscinetti:
            self.cuscinetto_selezionato = self.catalogo.cuscinetti.get_cuscinetto(v)

    def trasmissione(self):
            if self.salta_trasmissione == True:
                return

            velocita_originale = getattr(self, "velocita_selezionata_originale", "")
            
            if velocita_originale == "":
                if self.famiglia_selezionata.macro_categoria.tipo != MacroCategorie.Slitta:
                    
                    if self.velocita_selezionata.codice == "xxx":
                        t = self.catalogo.trasmissioni.get_trasmissione("xxx")
                    else:
                        t = None
                        for m in self.prodotto_selezionato.motorizzazioni.values():
                            if m.velocita.codice == self.velocita_selezionata.codice:
                                t = m.trasmissione
                                break
                else:
                    t = None
            else:
                t = self.catalogo.trasmissioni.get_trasmissione("xxx")
    
            self.trasmissione_selezionata = t
            
    def posizione_descrizioni(self, tipo: str) -> str:
        d = ""
        if tipo == "unita":
            d = (f"{self.corsa_selezionata.descrizione}\n"
                 f"{self.mandrino_selezionato.descrizione}\n"
                 f"{self.motore_selezionato.descrizione}\n"
                 f"{self.velocita_selezionata.descrizione}\n"
                 f"{self.trasmissione_selezionata.descrizione}\n")

        elif tipo == "mandrino":
            d = (f"{self.mandrino_selezionato.descrizione}\n"
                 f"{self.cuscinetto_selezionato.descrizione}\n"
                 f"{self.motore_selezionato.descrizione}\n"
                 f"{self.velocita_selezionata.descrizione}\n"
                 f"{self.trasmissione_selezionata.descrizione}\n")

        elif tipo == "slitta":
            d = f"{self.corsa_selezionata.descrizione}\n"

        return d

    def aggiorna_prodotto(self):
        for i in range(1, 5):
            combo = getattr(self.ui, f"cbOpzione{i}", None)
            if combo and combo.isVisible(): 
                if combo.currentText() == "" or combo.currentIndex() == -1:
                    return
                
        self.genera_codice()
        self.genera_descrizione()

#########################################################################################
# ----------------- AGGIORNAMENTO CHECKBOX ----------------------------------------------
#########################################################################################

    def aggiorna_opzione(self, ckb=None, btn=None):
        if ckb is not None:
            tag_codice = ckb.property("tag")
            op = self.prodotto_selezionato.opzioni_totali().get(tag_codice)

            if op:
                if ckb.isChecked(): 
                    self.applica_opzione(op, ckb)
                else:
                    self.rimuovi_opzione(op)

        if btn is not None:
            if btn.property("is_red"):
                self.applica_opzione_speciale(btn)
            else:
                self.rimuovi_opzione_speciale(btn)

    def applica_opzione(self, op, ckb):
        v_idx, m_idx = None, None
        self.motore_speciale = None

        # --------------------------------------------------
        # CERCO IL NUMERO DELLA COMBOBOX MOTORE E VELOCITA'
        # --------------------------------------------------
        for i in range(1, 5):
            combo = getattr(self.ui, f"cbOpzione{i}", None)
            if combo:
                tag = combo.property("tag")
                if tag == "cbVelocita":
                    v_idx = i
                elif tag == "cbMotore":
                    m_idx = i

        # ------------------------------------------------------------------------------------------
        # SE L'OPZIONE SELEZIONATA E' RELATIVA ALLA VELOCITA'
        # ------------------------------------------------------------------------------------------
        if DestinazioneOpzione.Velocita in op.destinazione:
            if v_idx:
                combo_v = getattr(self.ui, f"cbOpzione{v_idx}", None)
                if combo_v: combo_v.setEnabled(False)
            
            if op.comportamento == ComportamentoOpzione.DescrizioneFissa:
                self.velocita_selezionata.descrizione = op.descrizione
            else:
                testo, ok = QInputDialog.getText(
                    self, "Velocità speciale", op.voce_ck, text=op.descrizione
                )
                if ok:
                    self.velocita_selezionata.descrizione = testo

        # ------------------------------------------------------------------------------------------
        # SE L'OPZIONE SELEZIONATA E' RELATIVA AL MOTORE
        # ------------------------------------------------------------------------------------------
        elif DestinazioneOpzione.Motore in op.destinazione:
            if m_idx:
                combo_m = getattr(self.ui, f"cbOpzione{m_idx}", None)
                if combo_m: combo_m.setEnabled(False)
            
            if op.comportamento == ComportamentoOpzione.DescrizioneFissa:
                self.motore_selezionato.descrizione = op.descrizione
                # --------------------------------------------------------------------------------------------------------
                # SE E' CORPO MANDRINO, CAMBIO LA DESCRIZIONE, DISABILITO LA VELOCITA' E DISABILITO LE OPZIONI SBLOCCAGGIO
                # --------------------------------------------------------------------------------------------------------
                if op.codice == "corpo_mandrino":
                    self.salta_trasmissione = True
                    self.salta_evita_selezioni_multiple = True
                    combo_v = getattr(self.ui, f"cbOpzione{v_idx}", None)
                    combo_v.setEnabled(False)
                    self.velocita_selezionata = copy.deepcopy(self.catalogo.velocita.get_velocita(combo_v.currentText()))

                    # elimino la descrizione della posizione motore mandrino, in quanto non è più selezionabile
                    self.posizione_mandrino_selezionata_originale = self.prodotto_selezionato.famiglia.get_descrizione("posizione_motore_mandrino").descrizione_base
                    self.descrizione_da_sostituire = self.prodotto_selezionato.famiglia.get_descrizione("posizione_motore_mandrino")
                    self.descrizione_da_sostituire.descrizione_base = ""

                    if not combo_v.currentText() == "xxx":
                        for m in self.prodotto_selezionato.motorizzazioni.values():
                            if m.velocita.codice == self.velocita_selezionata.codice:
                                t = m.trasmissione
                                self.trasmissione_selezionata = copy.deepcopy(t)
                                break
                    else:
                        self.trasmissione_selezionata = copy.deepcopy(self.catalogo.velocita.get_velocita("xxx"))

                    self.velocita_selezionata.descrizione = "Velocità di collaudo da definire"
                    self.trasmissione_selezionata.descrizione = "Trasmissione non compresa"

                    for i in range(1, self.catalogo.opzioni.numero_opzioni() + 1):
                        ck = getattr(self.ui, f"ck{i}", None)
                        lb = getattr(self.ui, f"opzione{i}", None)
                        if ck and ck.isVisible():
                            tag_codice = ck.property("tag")
                            op = self.prodotto_selezionato.opzioni_totali().get(tag_codice)
                            if op and (DestinazioneOpzione.Sbloccaggio in op.destinazione or DestinazioneOpzione.Velocita in op.destinazione or DestinazioneOpzione.posizione_motore_mandrino in op.destinazione or DestinazioneOpzione.Motore in op.destinazione):
                                self.salta_sbloccaggio = True

                                if not ck.isChecked():
                                    if not ckb:
                                        ck.setEnabled(False)
                                        lb.setEnabled(False)
                                    else:
                                        ck.setChecked(False)
                                        ck.setEnabled(False)
                                        lb.setEnabled(False)

            elif op.comportamento == ComportamentoOpzione.DescrizioneEditabile:
                self.opzione_passata = op.codice
                
                uf = UfMotoreSpeciale(self) 

                if not uf.verifica_motori_disponibili():
                    QMessageBox.warning(self, "Attenzione", "Nessun motore maggiorato disponibile con questa velocità")
                    ckb.setChecked(False)
                    self.rimuovi_opzione(op)
                else:
                    uf.genera_taglia(self.prodotto_selezionato)
                    
                    if uf.exec() == QDialog.Accepted or getattr(uf, "confermato", False):
                        self.motore_speciale = uf.motore_creato
                    else:
                        ckb.setChecked(False)
                        self.rimuovi_opzione(op)
                    
                if self.motore_speciale is not None:
                    self.motore_selezionato.grandezza_descr = self.motore_speciale.grandezza_descr
                    self.motore_selezionato.potenza = self.motore_speciale.potenza
                    self.motore_selezionato.poli = self.motore_speciale.poli
                    self.motore_selezionato.freno = self.motore_speciale.freno
                    self.motore_selezionato.testo_agg = self.motore_speciale.testo_agg
                    self.motore_selezionato.descrizione = self.motore_selezionato.dati_motore()
            
            elif op.comportamento == ComportamentoOpzione.DescrizioneComplessa:
                if self.famiglia_selezionata.codice != "TX":
                    self.motore_selezionato = copy.deepcopy(self.catalogo.motori.get_motore(combo_m.currentText()))
                    self.motore_selezionato.freno = " autofrenante"
                    self.motore_selezionato.descrizione = self.motore_selezionato.dati_motore()

                                
        # -----------------------------------------------------
        # SE INVECE L'OPZIONE SELEZIONATA E' SCORRIMENTO
        # -----------------------------------------------------
        elif DestinazioneOpzione.scorrimento in op.destinazione:
            
            self.descrizione_base_originale_scorrimento = self.prodotto_selezionato.famiglia.get_descrizione(op.destinazione.name).descrizione_base
            self.descrizione_da_sostituire = self.prodotto_selezionato.famiglia.get_descrizione(op.destinazione.name)
            self.descrizione_da_sostituire.descrizione_base = copy.deepcopy(op.descrizione)

        # -----------------------------------------------------
        # SE INVECE L'OPZIONE SELEZIONATA E' VITE
        # -----------------------------------------------------
        elif DestinazioneOpzione.vite in op.destinazione:
                        
            self.descrizione_base_originale_vite = self.prodotto_selezionato.famiglia.get_descrizione(op.destinazione.name).descrizione_base
            self.descrizione_da_sostituire = self.prodotto_selezionato.famiglia.get_descrizione(op.destinazione.name)
            self.descrizione_da_sostituire.descrizione_base = copy.deepcopy(op.descrizione)

        # -----------------------------------------------------
        # SE INVECE L'OPZIONE SELEZIONATA E' POSIZIONE MOTORE BRUSHLESS
        # -----------------------------------------------------
        elif DestinazioneOpzione.posizione_motore_brushless in op.destinazione:
                        
            self.descrizione_base_originale_posizione_motore_brushless = self.prodotto_selezionato.famiglia.get_descrizione(op.destinazione.name).descrizione_base
            self.descrizione_da_sostituire = self.prodotto_selezionato.famiglia.get_descrizione(op.destinazione.name)
            
            uf = UfDefinisciPosizioneMotore(self)

            if uf.exec() == QDialog.Accepted or getattr(uf, "confermato", False):
                posizione_motore_scelta = uf.cb_posizione_motore_change()
                self.descrizione_da_sostituire.descrizione_base = f"{copy.deepcopy(op.descrizione)} {posizione_motore_scelta}"
            else:
                ckb.setChecked(False)
                self.rimuovi_opzione(op)

        # -----------------------------------------------------
        # SE INVECE L'OPZIONE SELEZIONATA E' POSIZIONE MOTORE MANDRINO
        # -----------------------------------------------------
        elif DestinazioneOpzione.posizione_motore_mandrino in op.destinazione:
                        
            self.descrizione_base_originale_posizione_motore_mandrino = self.prodotto_selezionato.famiglia.get_descrizione(op.destinazione.name).descrizione_base
            self.descrizione_da_sostituire = self.prodotto_selezionato.famiglia.get_descrizione(op.destinazione.name)

            uf = UfDefinisciPosizioneMotore(self)
            
            if uf.exec() == QDialog.Accepted or getattr(uf, "confermato", False):
                posizione_motore_scelta = uf.cb_posizione_motore_change()
                self.descrizione_da_sostituire.descrizione_base = f"{copy.deepcopy(op.descrizione)} {posizione_motore_scelta}"
            else:
                ckb.setChecked(False)
                self.rimuovi_opzione(op)

        # -----------------------------------------------------
        # SE INVECE L'OPZIONE SELEZIONATA E' MOTORE SLITTA RINVIATO 180°
        # -----------------------------------------------------
        elif DestinazioneOpzione.MotorizzazioneSlitta in op.destinazione and op.codice == "flangia_motore_rinviato":
            
            uf = UfDefinisciPosizioneMotore(self)

            if uf.exec() == QDialog.Accepted or getattr(uf, "confermato", False):
                posizione_motore_scelta = uf.cb_posizione_motore_change()
                self.descrizioni_aggiuntive[op.codice] = f"{copy.deepcopy(op.descrizione)} {posizione_motore_scelta}"
            else:
                ckb.setChecked(False)
                self.rimuovi_opzione(op)

        # ------------------------------------------------------------
        # SE INVECE L'OPZIONE SELEZIONATA E' DI ALTRO TIPO (Case Else)
        # ------------------------------------------------------------
        else:
            if op.comportamento == ComportamentoOpzione.DescrizioneFissa:
                self.descrizioni_aggiuntive[op.codice] = op.descrizione
            else:
                testo, ok = QInputDialog.getText(
                    self, "Opzione aggiuntiva", op.voce_ck, text=op.descrizione
                )
                if ok:
                    op.descrizione = testo
                    self.descrizioni_aggiuntive[op.codice] = testo

                else:
                    ckb.setChecked(False)

        # ------------------------------------------------------------------------------------------
        # RICHIAMO I METODI DI AGGIORNAMENTO FINALI
        # ------------------------------------------------------------------------------------------
        self.genera_codice()
        self.trasmissione()
        self.genera_descrizione()

        self.salta_trasmissione = False
        
    def rimuovi_opzione(self, op):
        v_idx, m_idx = None, None
        self.aggiornamento_in_corso = True

        self.disabilita_motore_autofrenante_tx()

        # --------------------------------------------------
        # CERCO IL NUMERO DELLA COMBOBOX MOTORE E VELOCITA'
        # --------------------------------------------------
        for i in range(1, 5):
            combo = getattr(self.ui, f"cbOpzione{i}", None)
            if combo:
                tag = combo.property("tag")
                if tag == "cbVelocita":
                    v_idx = i
                elif tag == "cbMotore":
                    m_idx = i

        # ------------------------------------------------------------------------------------------
        # SE L'OPZIONE SELEZIONATA E' RELATIVA ALLA VELOCITA'
        # ------------------------------------------------------------------------------------------
        if DestinazioneOpzione.Velocita in op.destinazione:
            if v_idx:
                combo_v = getattr(self.ui, f"cbOpzione{v_idx}", None)
                if combo_v:
                    combo_v.setEnabled(True)
                    testo_combo = combo_v.currentText()
                    vel_base = self.catalogo.velocita.get_velocita(testo_combo)
                    if vel_base:
                        self.velocita_selezionata.descrizione = vel_base.descrizione

        # ------------------------------------------------------------------------------------------
        # SE L'OPZIONE SELEZIONATA E' RELATIVA AL MOTORE
        # ------------------------------------------------------------------------------------------
        elif DestinazioneOpzione.Motore in op.destinazione:
            self.motore_speciale = None
            
            if m_idx:
                combo_m = getattr(self.ui, f"cbOpzione{m_idx}", None)
                if combo_m:
                    combo_m.setEnabled(True)
                    valore_combo = combo_m.currentText()
                    # ------------------------------------------------------------------------------------------
                    # SE E' CORPO MANDRINO, RIABILITO LA COMBOBOX VELOCITA'
                    # ------------------------------------------------------------------------------------------
                    if op.codice == "corpo_mandrino":
                        combo_v = getattr(self.ui, f"cbOpzione{v_idx}", None)
                        combo_v.setEnabled(True)
                        testo_combo = combo_v.currentText()
                        vel_base = self.catalogo.velocita.get_velocita(testo_combo)
                        if vel_base:
                            self.velocita_selezionata.descrizione = vel_base.descrizione

                            #ripristino la descrizione della posizione motore mandrino
                            self.descrizione_da_sostituire = self.prodotto_selezionato.famiglia.get_descrizione("posizione_motore_mandrino")
                            self.descrizione_da_sostituire.descrizione_base = self.posizione_mandrino_selezionata_originale
                            self.posizione_mandrino_selezionata_originale = None
                            
                        for i in range(1, self.catalogo.opzioni.numero_opzioni() + 1):
                            ck = getattr(self.ui, f"ck{i}", None)
                            lb = getattr(self.ui, f"opzione{i}", None)
                            if ck and ck.isVisible():
                                tag_codice = ck.property("tag")
                                op = self.prodotto_selezionato.opzioni_totali().get(tag_codice)
                                if op and (DestinazioneOpzione.Sbloccaggio in op.destinazione or DestinazioneOpzione.Velocita in op.destinazione or DestinazioneOpzione.posizione_motore_mandrino in op.destinazione):
                                    ck.setChecked(False)
                                    ck.setEnabled(True)
                                    lb.setEnabled(True)
                            
                    # ---------------------------------------------------------------------------------------------------------------------------
                    # SE L'OPZIONE E' IL MOTORE AUTOFRENANTE DELLA TX, DEVO SOTTRARRE 100 AL CODICE (Es: "250" diventa "150")
                    # ---------------------------------------------------------------------------------------------------------------------------
                    if op.codice == "motore_autofrenante" and self.prodotto_selezionato.famiglia.codice == "TX":
                        try:
                            nuovo_codice = str(int(valore_combo) - 100)
                            combo_m.setCurrentText(nuovo_codice)
                            valore_combo = nuovo_codice
                        except ValueError:
                            pass
                        
                        self.motore_selezionato = copy.deepcopy(self.catalogo.motori.get_motore(valore_combo))
                        if self.motore_selezionato:
                            self.motore_selezionato.descrizione = self.motore_selezionato.dati_motore()
                    else:
                        self.motore_selezionato = copy.deepcopy(self.catalogo.motori.get_motore(valore_combo))
                        if self.motore_selezionato:
                            self.motore_selezionato.descrizione = self.motore_selezionato.dati_motore()

            self.salta_evita_selezioni_multiple = False 

        # -----------------------------------------------------
        # SE INVECE L'OPZIONE SELEZIONATA E' SCORRIMENTO
        # -----------------------------------------------------
        elif DestinazioneOpzione.scorrimento in op.destinazione:
            self.descrizione_da_sostituire = self.prodotto_selezionato.famiglia.get_descrizione(op.destinazione.name)
            self.descrizione_da_sostituire.descrizione_base = self.descrizione_base_originale_scorrimento
            self.descrizione_base_originale_scorrimento = None
            self.descrizione_da_sostituire = None

        # -----------------------------------------------------
        # SE INVECE L'OPZIONE SELEZIONATA E' VITE
        # -----------------------------------------------------
        elif DestinazioneOpzione.vite in op.destinazione:
            self.descrizione_da_sostituire = self.prodotto_selezionato.famiglia.get_descrizione(op.destinazione.name)
            self.descrizione_da_sostituire.descrizione_base = self.descrizione_base_originale_vite
            self.descrizione_base_originale_vite = None
            self.descrizione_da_sostituire = None

        # -----------------------------------------------------
        # SE INVECE L'OPZIONE SELEZIONATA E' POSIZIONE MOTORE BRUSHLESS
        # -----------------------------------------------------
        elif DestinazioneOpzione.posizione_motore_brushless in op.destinazione:
            self.descrizione_da_sostituire = self.prodotto_selezionato.famiglia.get_descrizione(op.destinazione.name)
            self.descrizione_da_sostituire.descrizione_base = self.descrizione_base_originale_posizione_motore_brushless
            self.descrizione_base_originale_posizione_motore_brushless = None
            self.descrizione_da_sostituire = None

        # -----------------------------------------------------
        # SE INVECE L'OPZIONE SELEZIONATA E' POSIZIONE MOTORE MANDRINO
        # -----------------------------------------------------
        elif DestinazioneOpzione.posizione_motore_mandrino in op.destinazione:
            self.descrizione_da_sostituire = self.prodotto_selezionato.famiglia.get_descrizione(op.destinazione.name)
            self.descrizione_da_sostituire.descrizione_base = self.descrizione_base_originale_posizione_motore_mandrino
            self.descrizione_base_originale_posizione_motore_mandrino = None
            self.descrizione_da_sostituire = None

        # -----------------------------------------------------
        # SE INVECE L'OPZIONE SELEZIONATA E' MOTORE SLITTA RINVIATO 180°
        # -----------------------------------------------------
        elif DestinazioneOpzione.MotorizzazioneSlitta in op.destinazione and op.codice == "flangia_motore_rinviato":
            #self.descrizioni_aggiuntive[op.codice] = op.descrizione
            if op.codice in self.descrizioni_aggiuntive:
                del self.descrizioni_aggiuntive[op.codice]
            

        # ------------------------------------------------------------------------------------------
        # CASE ELSE: RIMUOVO LA DESCRIZIONE DAL DIZIONARIO DELLE DESCRIZIONI AGGIUNTIVE
        # ------------------------------------------------------------------------------------------
        else:
            if op.codice in self.descrizioni_aggiuntive:
                del self.descrizioni_aggiuntive[op.codice]

        # ------------------------------------------------------------------------------------------
        # RICHIAMO I METODI DI AGGIORNAMENTO FINALI
        # ------------------------------------------------------------------------------------------
        self.genera_codice()
        self.trasmissione()
        self.genera_descrizione()

        self.aggiornamento_in_corso = False

##################################################
# ------- GESTIONE BOTTONI OPZIONI SPECIALI -----
##################################################

    def applica_opzione_speciale(self, btn):
        codice_cercato = btn.text()
        opzione_trovata = next((opz for opz in self.opzioni_temporanee if opz.codice == codice_cercato), None)

        if opzione_trovata is not None:
            self.descrizioni_aggiuntive[opzione_trovata] = opzione_trovata.descrizione

        btn.style().unpolish(btn)
        btn.style().polish(btn)

        self.genera_descrizione()

    def rimuovi_opzione_speciale(self, btn):
        codice_cercato = btn.text()
        opzione_trovata = next((opz for opz in self.opzioni_temporanee if opz.codice == codice_cercato), None)

        if opzione_trovata is not None:
            del self.descrizioni_aggiuntive[opzione_trovata]
        if opzione_trovata in self.opzioni_temporanee:
            self.opzioni_temporanee.remove(opzione_trovata)

        btn.style().unpolish(btn)
        btn.style().polish(btn)

        btn.setStyleSheet("")
        btn.setText("Aggiungi opzione speciale")
        
        self.genera_descrizione()
        
#########################################################################################
# ----------------- GESTIONE SPUNTE CHECKBOX --------------------------------------------
#########################################################################################

    def evita_selezione_multipla(self, variabile):

        if self.salta_evita_selezioni_multiple == True:
            return

        opzione_selezionata = False

        for i in range(1, self.catalogo.opzioni.numero_opzioni() + 1):
            ck = getattr(self.ui, f"ck{i}", None)
            if ck and ck.isVisible():
                if ck.isChecked():
                    tag_codice = ck.property("tag")

                    if tag_codice == "motore_autofrenante":
                        continue

                    op = self.prodotto_selezionato.opzioni_totali().get(tag_codice)
                    
                    if op and (variabile in op.destinazione):
                        opzione_selezionata = True
                        break
                    

        for i in range(1, self.catalogo.opzioni.numero_opzioni() + 1):
            ck = getattr(self.ui, f"ck{i}", None)
            lbl = getattr(self.ui, f"opzione{i}", None)
            
            if ck and ck.isVisible():
                tag_codice = ck.property("tag")

                if tag_codice == "motore_autofrenante":
                    continue

                op = self.prodotto_selezionato.opzioni_totali().get(tag_codice)
                
                if op and (variabile in op.destinazione):
                    if opzione_selezionata:
                        if not ck.isChecked():
                            ck.setEnabled(False)
                            if lbl: lbl.setEnabled(False)
                    else:
                        ck.setEnabled(True)
                        if lbl: lbl.setEnabled(True)

    def sbloccaggio(self):
        if self.salta_sbloccaggio == True:
            return
        self.evita_selezione_multipla(DestinazioneOpzione.Sbloccaggio)

    def motore(self):
        self.evita_selezione_multipla(DestinazioneOpzione.Motore)

    def motorizzazione_slitte(self):
        self.evita_selezione_multipla(DestinazioneOpzione.MotorizzazioneSlitta)

    def soffietti(self):
        if self.famiglia_selezionata.macro_categoria.nome == "slitta":
            valore_combo = self.ui.cbOpzione1.currentText()
            corsa_soffietto = valore_combo[-3:] if valore_combo else ""

            for i in range(1, self.catalogo.opzioni.numero_opzioni() + 1):
                ck = getattr(self.ui, f"ck{i}", None)
                lbl = getattr(self.ui, f"opzione{i}", None)

                if ck and ck.isVisible():
                    tag_stringa = str(ck.property("tag") or "")
                    nome_opzione = tag_stringa[:9] 

                    if nome_opzione == "soffietto":
                        if corsa_soffietto != tag_stringa[-3:]:
                            ck.setEnabled(False)
                            if lbl: lbl.setEnabled(False)
                        else:
                            ck.setEnabled(True)
                            if lbl: lbl.setEnabled(True)

    def casi_speciali(self):
        self.motore()
        self.sbloccaggio()
        self.salta_sbloccaggio = False
        self.motorizzazione_slitte()
        self.disabilita_cb()
        self.salta_evita_selezioni_multiple = False

#########################################################################################
# ----------------- GESTIONE LISTINO ----------------------------------------------------
#########################################################################################

    def prezzo_base(self, tipo, prezzo_base1: str, prezzo_base2: str, prezzo_base4: str) -> float:
        pr_b = 0.0

        if tipo == MacroCategorie.Unita:
            pr_b = self.prezzo_base_unita(prezzo_base1)

        elif tipo == MacroCategorie.Slitta:
            pr_b = self.prezzo_base_slitta(prezzo_base1)

        elif tipo == MacroCategorie.Mandrino:
            if prezzo_base2 != "" and prezzo_base4 != "":
                pr_b = self.prezzo_base_mandrino(prezzo_base4)

        return pr_b

    def prezzo_base_unita(self, corsa: str) -> float:
        chiave = f"{self.prodotto_selezionato.codice} | {corsa}"
        conf = self.catalogo.listino.get_prezzo_base_unita(chiave)
        return conf.prezzo if conf else 0.0

    def prezzo_base_slitta(self, corsa: str) -> float:
        chiave = f"{self.prodotto_selezionato.codice} | {corsa}"
        conf = self.catalogo.listino.get_prezzo_base_slitta(chiave)
        return conf.prezzo if conf else 0.0

    def prezzo_base_mandrino(self, cuscinetto: str) -> float:
        gr_motore = self.motore_selezionato.grandezza
        chiave = f"{self.prodotto_selezionato.codice} | {cuscinetto} | {gr_motore}"
        conf = self.catalogo.listino.get_prezzo_base_mandrino(chiave)
        return conf.prezzo if conf else 0.0

    def prezzo_mandrino(self) -> float:
        pr_m = 0.0
        cb_mandrino = self.trova_cb()

        if cb_mandrino is not None:
            valore_combo = cb_mandrino.currentText()
            if valore_combo != "":
                mand = self.prodotto_selezionato.mandrini.get(valore_combo)
                
                if mand:
                    prezzi_prodotto = self.catalogo.listino.prezzi_mandrini.get(self.prodotto_selezionato.codice)
                    if prezzi_prodotto:
                        pr_m = prezzi_prodotto.get(mand.codice, 0.0)

        return pr_m

    def trova_cb(self) -> QComboBox:
        for i in range(1, 5):
            combo = getattr(self.ui, f"cbOpzione{i}", None)
            if combo:
                if combo.property("tag") == "cbMandrino":
                    return combo
        return None

    def prezzi_opzioni(self) -> float:
        pr_o = 0.0

        for i in range(1, self.catalogo.opzioni.numero_opzioni() + 1):
            ck = getattr(self.ui, f"ck{i}", None)
            
            if ck and ck.isVisible():
                if ck.isChecked():
                    tag_codice = ck.property("tag")
                    op = self.prodotto_selezionato.opzioni_totali().get(tag_codice)
                    
                    if op:
                        prezzi_prodotto = self.catalogo.listino.prezzi_opzioni.get(self.prodotto_selezionato.codice)
                        if prezzi_prodotto:
                            pr_o += prezzi_prodotto.get(op.codice, 0.0)

        # ----------------------------------------------------------------------
        # ------------- AGGIUNGO I PREZZI DELLE OPZIONI SPECIALI ---------------
        # ----------------------------------------------------------------------
        for i in range(1,4):
            bottone = getattr(self.ui, f"btn_opzione_speciale{i}", None)
            if bottone and bottone.property("is_red"):
                codice_cercato = bottone.text()
                opzione_trovata = next((opz for opz in self.opzioni_temporanee if opz.codice == codice_cercato), None)
                if opzione_trovata is not None:
                    pr_o += float(opzione_trovata.prezzo)
                                           
        return pr_o

    def aggiorna_prezzo_prodotto(self, cb1, cb2, cb4):
        tipo_prodotto = self.famiglia_selezionata.macro_categoria.tipo

        prezzo_base_p = self.prezzo_base(tipo_prodotto, cb1.currentText(), cb2.currentText(), cb4.currentText())
        prezzo_mandrino_p = self.prezzo_mandrino()
        prezzo_opzioni_p = self.prezzi_opzioni()

        prezzo_prodotto = prezzo_base_p + prezzo_mandrino_p + prezzo_opzioni_p

        if hasattr(self.ui, "tbPrezzo"):
            self.ui.tbPrezzo.setText(f"{prezzo_prodotto:.2f}")

#########################################################################################
# ------------ GESTIONE MOTORE AUTOFRENANTE E MOTORE DA DEFINIRE ------------------------
#########################################################################################

    def abilita_motore_autofrenante(self):
        for i in range(1, self.catalogo.opzioni.numero_opzioni() + 1):
            ck = getattr(self.ui, f"ck{i}", None)
            lbl = getattr(self.ui, f"opzione{i}", None)
            
            if ck and ck.property("tag") == "motore_autofrenante":
                if ck and not ck.isChecked():
                    ck.setChecked(True)
                    ck.setEnabled(True)
                    lbl.setEnabled(True)
                    self.evita_selezione_multipla(DestinazioneOpzione.Motore)

        for i in range(1, 5):
            combo = getattr(self.ui, f"cbOpzione{i}", None)
            if combo and combo.property("tag") == "cbMotore":
                combo.setEnabled(False)
                break
                
    def disabilita_motore_autofrenante_tx(self):
        for i in range(1, self.catalogo.opzioni.numero_opzioni() + 1):
            ck = getattr(self.ui, f"ck{i}", None)
            lbl = getattr(self.ui, f"opzione{i}", None)
            
            if ck and not ck.isChecked():
                if ck.property("tag") == "motore_autofrenante" and self.prodotto_selezionato.famiglia.codice == "TX":
                    ck.setChecked(False)
                    ck.setEnabled(False)
                    lbl.setEnabled(False)
                    
                    for i in range(1, 5):
                        combo = getattr(self.ui, f"cbOpzione{i}", None)
                        if combo and combo.property("tag") == "cbMotore":
                            combo.setEnabled(True)
                            break

    def motore_autofrenante(self):
        if self.motore_selezionato and self.motore_selezionato.freno != "" and self.prodotto_selezionato.famiglia.codice == "TX":
            self.abilita_motore_autofrenante()
        else:
            self.disabilita_motore_autofrenante_tx()    

    def crea_motore_da_definire(self):
        uf = UfDefinisciTaglia(self)
        uf.genera_taglia()

        if uf.exec() == QDialog.Accepted or uf.confermato:
            self.motore_da_definire = uf.motore_creato

    def disabilita_cb(self):
        for i in range(1, 5):
            combo = getattr(self.ui, f"cbOpzione{i}", None)
            if not combo: 
                continue
                
            valore = combo.currentText()
            tag = combo.property("tag")
            
            if valore == "xxx" and tag == "cbMotore":
                for n in range(1, self.catalogo.opzioni.numero_opzioni() + 1):
                    ck = getattr(self.ui, f"ck{n}", None)
                    lbl = getattr(self.ui, f"opzione{n}", None)
                    
                    if ck and ck.isVisible() and not ck.isChecked():
                        tag_codice = ck.property("tag")
                        op = self.prodotto_selezionato.opzioni_totali().get(tag_codice)
                        
                        if op and DestinazioneOpzione.Motore in op.destinazione:
                            ck.setEnabled(False)
                            if lbl: lbl.setEnabled(False)
                            
            elif valore == "xxx" and tag == "cbVelocita":
                for n in range(1, self.catalogo.opzioni.numero_opzioni() + 1):
                    ck = getattr(self.ui, f"ck{n}", None)
                    lbl = getattr(self.ui, f"opzione{n}", None)
                    
                    if ck and ck.isVisible() and not ck.isChecked():
                        tag_codice = ck.property("tag")
                        op = self.prodotto_selezionato.opzioni_totali().get(tag_codice)
                        
                        if op and DestinazioneOpzione.Velocita in op.destinazione:
                            ck.setEnabled(False)
                            if lbl: lbl.setEnabled(False)

    def abilita_cb(self, variabile):
        for i in range(1, self.catalogo.opzioni.numero_opzioni() + 1):
            ck = getattr(self.ui, f"ck{i}", None)
            lbl = getattr(self.ui, f"opzione{i}", None)
            
            if ck and ck.isVisible() and not ck.isChecked():
                tag_codice = ck.property("tag")
                op = self.prodotto_selezionato.opzioni_totali().get(tag_codice)
                
                if op and variabile in op.destinazione:
                    ck.setEnabled(True)
                    if lbl: lbl.setEnabled(True)

#########################################################################################
# ----------------- GESTIONE DATABASE CLIENTE -------------------------------------------
#########################################################################################

    def salva_cliente(self):
        nuovo_cliente = Cliente(
            ragione_sociale=self.ui.cbCliente.currentText(),
            indirizzo=self.ui.tbIndirizzo.text(),
            cap=self.ui.tbCap.text(),
            citta=self.ui.tbCitta.text(),
            provincia=self.ui.tbPV.text(),
            partita_iva=self.ui.tbPiva.text(),
            codice_fiscale=self.ui.tbCF.text(),
            telefono=self.ui.tbTelefono.text(),
            email=self.ui.tbEmail.text(),
            categoria=self.ui.cbCategoria.currentText(),
            pagamento=self.ui.cbPagamento.currentText(),
            sconto=self.ui.tbSconto.text(),
            corriere=self.ui.cbTrasporto.currentText(),
            resa_merce=self.ui.cbResa.currentText()
        )

        for ref in self.referenti_temporanei:
            nuovo_cliente.aggiungi_referente(ref)

        valido, messaggio_errore = nuovo_cliente.convalida_dati()
        if not valido:
            QMessageBox.warning(self, "Attenzione", messaggio_errore)
            return

        try:
            connessione = pyodbc.connect(
                "Driver={ODBC Driver 18 for SQL Server};"
                f"Server={D_HOST};"
                f"Database={D_NAME};"  # Usiamo la variabile dinamica invece del nome fisso
                f"UID={D_USER};"       # Inserisce l'utente del file config.ini
                f"PWD={D_PASS};"       # Inserisce la password del file config.ini
                "TrustServerCertificate=yes;"
            )

            cursore = connessione.cursor()

            if self.modalita_cliente == "NUOVO":

                query_cliente = """
                    INSERT INTO configuratore.clienti (
                        ragione_sociale, indirizzo, cap, citta, provincia, partita_iva, codice_fiscale,
                        telefono, email, categoria, pagamento, sconto, corriere, resa_merce
                    ) 
                    OUTPUT INSERTED.id
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """

                valori_cliente = (
                    nuovo_cliente.ragione_sociale, nuovo_cliente.indirizzo, nuovo_cliente.cap, nuovo_cliente.citta,
                    nuovo_cliente.provincia, nuovo_cliente.partita_iva, nuovo_cliente.codice_fiscale, nuovo_cliente.telefono,
                    nuovo_cliente.email, nuovo_cliente.categoria, nuovo_cliente.pagamento, nuovo_cliente.sconto,
                    nuovo_cliente.corriere, nuovo_cliente.resa_merce
                )
                
                cursore.execute(query_cliente, valori_cliente)
                
                risultato_id = cursore.fetchone()
                if risultato_id:
                    cliente_id_generato = int(risultato_id[0])
                    self.cliente_id_corrente = cliente_id_generato
                else:
                    raise Exception("Impossibile recuperare l'ID del nuovo cliente.")
                messaggio = "Nuovo cliente inserito"

            elif self.modalita_cliente == "MODIFICA":

                query_cliente = """
                    UPDATE configuratore.clienti
                    SET indirizzo=?, cap=?, citta=?, provincia=?, partita_iva=?, codice_fiscale=?,telefono=?, email=?,
                    categoria=?, pagamento=?, sconto=?, corriere=?, resa_merce=? WHERE ragione_sociale=?
                    """

                valori_cliente = (nuovo_cliente.indirizzo, nuovo_cliente.cap, nuovo_cliente.citta,
                    nuovo_cliente.provincia, nuovo_cliente.partita_iva, nuovo_cliente.codice_fiscale, nuovo_cliente.telefono,
                    nuovo_cliente.email, nuovo_cliente.categoria, nuovo_cliente.pagamento, nuovo_cliente.sconto,
                    nuovo_cliente.corriere, nuovo_cliente.resa_merce, nuovo_cliente.ragione_sociale)

                cursore.execute(
                    "SELECT id FROM configuratore.clienti WHERE ragione_sociale=?",
                    (nuovo_cliente.ragione_sociale,)
                )

                risultato = cursore.fetchone()

                if risultato is None:
                    raise Exception("Cliente non trovato nel database")

                cliente_id_generato = risultato[0]

                cursore.execute(
                    "DELETE FROM configuratore.referenti WHERE cliente_id=?",
                    (cliente_id_generato,)
                )

                cursore.execute(query_cliente, valori_cliente)

                messaggio = "Cliente modificato"

            query_referente = ("INSERT INTO configuratore.referenti (cliente_id, nome, cognome, telefono, cellulare, email, ruolo) VALUES (?, ?, ?, ?, ?, ?, ?)")

            for ref in self.referenti_temporanei:
                valori_ref = (cliente_id_generato, ref.nome, ref.cognome, ref.telefono, ref.cellulare, ref.email, ref.ruolo)
                cursore.execute(query_referente, valori_ref)

            connessione.commit()
            cursore.close()
            connessione.close()

            self.modalita_cliente = None

            self.referenti_temporanei.clear()
            self.ui.frmCliente.setEnabled(False)
            self.ui.btn_salva.setEnabled(False)
            self.ui.btn_nuovo.setEnabled(True)
            self.ui.btn_modifica.setEnabled(True)
            self.ui.cbCliente.setEnabled(True)
            
            QMessageBox.information(self, "Successo", "Cliente salvato")

            self.ui.btn_agg_referente.setEnabled(False)
            self.ui.btn_elim_referente.setEnabled(False)
            self.ui.cbReferente.setEnabled(False)

        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Problema con il database:\n{e}")

    def inserisci_nuovo_cliente(self):
        self.modalita_cliente = "NUOVO"
        self.ui.cbReferente.setEnabled(True)
        self.ui.cbReferente.clear()
        self.ui.btn_agg_referente.setEnabled(True)
        self.ui.btn_elim_referente.setEnabled(True)
        self.ui.frmCliente.setEnabled(True)
        self.ui.btn_salva.setEnabled(True)
        self.ui.btn_modifica.setEnabled(False)
        self.ui.cbCliente.setCurrentIndex(-1)
        self.ui.tbIndirizzo.setText("Indirizzo")
        self.ui.tbCap.setText("CAP")
        self.ui.tbCitta.setText("Città")
        self.ui.tbPV.setText("PV")
        self.ui.tbPiva.setText("Partita IVA")
        self.ui.tbCF.setText("Codice Fiscale")
        self.ui.tbTelefono.setText("Telefono")
        self.ui.tbEmail.setText("E-mail")
        self.ui.cbCategoria.setCurrentIndex(-1)
        self.ui.cbPagamento.setCurrentIndex(-1)
        self.ui.tbSconto.clear()
        self.ui.cbTrasporto.setCurrentIndex(-1)
        self.ui.cbResa.setCurrentIndex(-1)
        self.ui.cbReferente.setCurrentIndex(-1)
            
    
    def modifica_cliente(self):
        if not self.ui.cbCliente.currentText() == "":
            self.modalita_cliente = "MODIFICA"
            self.ui.cbReferente.setEnabled(True)
            self.ui.btn_agg_referente.setEnabled(True)
            self.ui.btn_elim_referente.setEnabled(True)
            self.ui.frmCliente.setEnabled(True)
            self.ui.btn_nuovo.setEnabled(False)
            self.ui.btn_salva.setEnabled(True) 
            self.ui.btn_modifica.setEnabled(False)
            self.ui.cbCliente.setEnabled(False)
            
    def aggiungi_referente(self):
        uf = UfReferente(self)
        if uf.exec() == QDialog.Accepted:
            self.referenti_temporanei.append(uf.nuovo_ref)
            testo_combo = f"{uf.nuovo_ref.nome} {uf.nuovo_ref.cognome} ({uf.nuovo_ref.ruolo})"
            self.ui.cbReferente.addItem(testo_combo)
            self.ui.btn_salva.setEnabled(True)

    def elimina_referente(self):
        indice_selezionato = self.ui.cbReferente.currentIndex()
        if indice_selezionato >= 0:
            self.ui.cbReferente.removeItem(indice_selezionato)  
            self.referenti_temporanei.pop(indice_selezionato)

    def cbCliente_click(self):
        self.ui.btn_modifica.setEnabled(True)
        ragione_sociale = self.ui.cbCliente.currentText()

        if ragione_sociale == "":
            return

        try:
            connessione = pyodbc.connect(
                "Driver={ODBC Driver 18 for SQL Server};"
                f"Server={D_HOST};"
                f"Database={D_NAME};"  # Usiamo la variabile dinamica invece del nome fisso
                f"UID={D_USER};"       # Inserisce l'utente del file config.ini
                f"PWD={D_PASS};"       # Inserisce la password del file config.ini
                "TrustServerCertificate=yes;"
            )

            cursore = connessione.cursor()

            cursore.execute("""
                SELECT
                    id,
                    indirizzo,
                    cap,
                    citta,
                    provincia,
                    partita_iva,
                    codice_fiscale,
                    telefono,
                    email,
                    categoria,
                    pagamento,
                    sconto,
                    corriere,
                    resa_merce
                FROM configuratore.clienti
                WHERE ragione_sociale = ?
            """, (ragione_sociale,))

            cliente = cursore.fetchone()

            if cliente:

                cliente_id = cliente[0]
                self.cliente_id_corrente = cliente_id

                self.ui.tbIndirizzo.setText(cliente[1] or "")
                self.ui.tbCap.setText(cliente[2] or "")
                self.ui.tbCitta.setText(cliente[3] or "")
                self.ui.tbPV.setText(cliente[4] or "")
                self.ui.tbPiva.setText(cliente[5] or "")
                self.ui.tbCF.setText(cliente[6] or "")
                self.ui.tbTelefono.setText(cliente[7] or "")
                self.ui.tbEmail.setText(cliente[8] or "")
                self.ui.cbCategoria.setCurrentText(cliente[9] or "")
                self.ui.cbPagamento.setCurrentText(cliente[10] or "")
                self.ui.tbSconto.setText(str(cliente[11] or ""))
                self.ui.cbTrasporto.setCurrentText(cliente[12] or "")
                self.ui.cbResa.setCurrentText(cliente[13] or "")
                
                cursore.execute("""
                    SELECT nome, cognome, telefono, cellulare, email, ruolo 
                    FROM configuratore.referenti 
                    WHERE cliente_id = ?
                """, (cliente_id,))
                
                referenti_db = cursore.fetchall()
                
                self.referenti_temporanei.clear()
                self.ui.cbReferente.clear()
                
                for r in referenti_db:
                    nuovo_ref = Referente(
                        nome=r[0] or "",
                        cognome=r[1] or "",
                        telefono=r[2] or "",
                        cellulare=r[3] or "",
                        email=r[4] or "",
                        ruolo=r[5] or ""
                    )
                    self.referenti_temporanei.append(nuovo_ref)
                    
                    testo_combo = f"{nuovo_ref.nome} {nuovo_ref.cognome} ({nuovo_ref.ruolo})"
                    self.ui.cbReferente.addItem(testo_combo)
                    
                self.ui.cbReferente.setCurrentIndex(0)

            cursore.close()
            connessione.close()

        except Exception as e:
            QMessageBox.critical(
            self,
            "Errore Caricamento Cliente",
            f"Impossibile caricare il cliente:\n{e}"
        )


#########################################################################################
# ----------------- GESTIONE PULSANTI PREVENTIVO ----------------------------------------
#########################################################################################

    def btn_aggiungi_prodotto_click(self):
        riga_successiva = self.ui.tb_righe.rowCount()
        self.ui.tb_righe.insertRow(riga_successiva)

        self.descrizione_da_salvare = self.ui.tbDescrizione.toPlainText()

        testo_libero_item = QTableWidgetItem("")
        riga_item = QTableWidgetItem("")
        codice_item = QTableWidgetItem(str(self.ui.tbCodice.text()))
        prezzo_item = QTableWidgetItem(str(self.ui.tbPrezzo.text()))
        sconto_item = QTableWidgetItem("")
        descrizione_item = QTableWidgetItem(str(self.ui.tbDescrizione.toPlainText()))

        colonne_item = [
        (0, testo_libero_item),
        (1, riga_item),
        (2, codice_item),
        (3, prezzo_item),
        (4, sconto_item),
        (5, descrizione_item)
        ]

        colonne_abilitate = [1, 4]

        for colonna, item in colonne_item:

            if colonna not in colonne_abilitate:
                item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
            else:
                pass

        self.ui.tb_righe.setItem(riga_successiva, 0, testo_libero_item)
        self.ui.tb_righe.setItem(riga_successiva, 1, riga_item)
        self.ui.tb_righe.setItem(riga_successiva, 2, codice_item)
        self.ui.tb_righe.setItem(riga_successiva, 3, prezzo_item)
        self.ui.tb_righe.setItem(riga_successiva, 4, sconto_item)
        self.ui.tb_righe.setItem(riga_successiva, 5, descrizione_item)

        self.ui.tb_righe.setColumnHidden(5, True)

        self.ui.btn_sposta_giu.setEnabled(True)
        self.ui.btn_sposta_su.setEnabled(True)
        self.ui.btn_elimina_riga.setEnabled(True)
        self.ui.tbConsegna.setEnabled(True)
        self.ui.cbImballo.setEnabled(True)
        self.ui.tbValidita.setEnabled(True)

        self.ui.btn_genera_preventivo.setEnabled(True)
        self.ui.btn_elimina_preventivo.setEnabled(True)
        self.reset_condizioni()
        self.ui.cbProdotto.setCurrentIndex(-1)

    def btn_aggiungi_accessorio_click(self):
        uf = ufAccessori(self)
        if uf.exec() == QDialog.Accepted:
            riga_successiva = self.ui.tb_righe.rowCount()
            self.ui.tb_righe.insertRow(riga_successiva)

            cod_accessorio = uf.accessorio_selezionato
            
            accessorio_oggetto = self.catalogo.accessori.get_accessorio(cod_accessorio)
            self.descrizione_da_salvare = accessorio_oggetto.descrizione if accessorio_oggetto else ""
            prezzo_valore = accessorio_oggetto.prezzo if accessorio_oggetto else 0

            testo_libero_item = QTableWidgetItem("")
            riga_item = QTableWidgetItem("")
            codice_item = QTableWidgetItem(str(cod_accessorio))
            prezzo_item = QTableWidgetItem(str(prezzo_valore))
            sconto_item = QTableWidgetItem("")
            descrizione_item = QTableWidgetItem(str(self.descrizione_da_salvare))

            colonne_item = [
            (0, testo_libero_item),
            (1, riga_item),
            (2, codice_item),
            (3, prezzo_item),
            (4, sconto_item),
            (5, descrizione_item)
            ]
    
            colonne_abilitate = [1, 4]
    
            for colonna, item in colonne_item:
    
                if colonna not in colonne_abilitate:
                    item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                else:
                    pass

            self.ui.tb_righe.setItem(riga_successiva, 0, testo_libero_item)
            self.ui.tb_righe.setItem(riga_successiva, 1, riga_item)
            self.ui.tb_righe.setItem(riga_successiva, 2, codice_item)
            self.ui.tb_righe.setItem(riga_successiva, 3, prezzo_item)
            self.ui.tb_righe.setItem(riga_successiva, 4, sconto_item)
            self.ui.tb_righe.setItem(riga_successiva, 5, descrizione_item)

            self.ui.btn_genera_preventivo.setEnabled(True)
            self.ui.btn_elimina_preventivo.setEnabled(True)
            
    def btn_aggiungi_testo_click(self):
        
        testo_libero, ok = QInputDialog.getText(self, "Testo libero", "Inserisci testo")

        if ok:
            
            riga_successiva = self.ui.tb_righe.rowCount()
            self.ui.tb_righe.insertRow(riga_successiva)

            colonne_item = [
            (0, QTableWidgetItem(str(testo_libero))),
            (1, QTableWidgetItem("")),
            (2, QTableWidgetItem("")),
            (3, QTableWidgetItem("")),
            (4, QTableWidgetItem("")),
            (5, QTableWidgetItem(""))
            ]

            colonne_abilitate = [0]
            
            for colonna, item in colonne_item:

                if colonna not in colonne_abilitate:
                    item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                else:
                    pass
            
                self.ui.tb_righe.setItem(riga_successiva, colonna, item)
            
    def btn_sposta_giu_click(self):
        riga_corrente = self.ui.tb_righe.currentRow()
        totale_righe = self.ui.tb_righe.rowCount()
    
        if riga_corrente < 0 or riga_corrente >= totale_righe - 1:
            return
        
        riga_destinazione = riga_corrente + 1
        self._scambia_righe(riga_corrente, riga_destinazione)
    
    def btn_sposta_su_click(self):
        riga_corrente = self.ui.tb_righe.currentRow()
    
        if riga_corrente <= 0:
            return
            
        riga_destinazione = riga_corrente - 1
        self._scambia_righe(riga_corrente, riga_destinazione)
    
    def btn_elimina_riga_click(self):
        riga_corrente = self.ui.tb_righe.currentRow()
    
        if riga_corrente < 0:
            QMessageBox.warning(self, "Attenzione", "Seleziona una riga da eliminare")
            return
            
        self.ui.tb_righe.removeRow(riga_corrente)

        if riga_corrente < 1:
            self.ui.btn_genera_preventivo.setEnabled(False)
            
    def _scambia_righe(self, riga_a, riga_b):
        tabella = self.ui.tb_righe
        totale_colonne = tabella.columnCount()
        
        for colonna in range(totale_colonne):
            item_a = tabella.takeItem(riga_a, colonna)
            item_b = tabella.takeItem(riga_b, colonna)
            
            tabella.setItem(riga_a, colonna, item_b)
            tabella.setItem(riga_b, colonna, item_a)
            
        tabella.setCurrentCell(riga_b, tabella.currentColumn())

    def genera_preventivo(self):

        # Controllo che tutti i campi obbligatori siano compilati
        if self.ui.cbCliente.currentText() == "" or self.ui.tbConsegna.text() == "" or self.ui.cbImballo.currentText() == "" or self.ui.tbValidita.text() == "":
            QMessageBox.warning(self, "Dati incompleti", "Dati mancanti per poter generare il preventivo")
            return

        # Controllo che tutte le righe con prezzo abbiano una quantità valida
        totale_righe = self.ui.tb_righe.rowCount()
        for riga in range(totale_righe):
            prezzo_str = self.ui.tb_righe.item(riga, 3).text() if self.ui.tb_righe.item(riga, 3) else ""
            if prezzo_str != "":
                qta_str = self.ui.tb_righe.item(riga, 1).text().strip() if self.ui.tb_righe.item(riga, 1) else ""
                if qta_str == "" or not qta_str.isdigit() or int(qta_str) <= 0:
                    QMessageBox.warning(
                        self, 
                        "Quantità Mancante", 
                        f"Impossibile generare il PDF: inserire una quantità valida nella riga {riga + 1}."
                    )
                    return

        percorso_salvataggio, _ = QFileDialog.getSaveFileName(
            self, "Salva Preventivo", "Preventivo.pdf", "File PDF (*.pdf)"
        )
        
        if not percorso_salvataggio:
            return

        self.nuovo_preventivo = Preventivo()
        
        anno_corrente = date.today().year
        oggi = datetime.now()

        self.nuovo_preventivo.cliente = self.ui.cbCliente.currentText()
        self.nuovo_preventivo.anno = anno_corrente
        self.nuovo_preventivo.data_creazione = oggi
        self.nuovo_preventivo.consegna = self.ui.tbConsegna.text()
        self.nuovo_preventivo.imballo = self.ui.cbImballo.currentText()
        self.nuovo_preventivo.validita = self.ui.tbValidita.text()

        if not hasattr(self, 'cliente_id_corrente') or self.cliente_id_corrente is None:
            QMessageBox.warning(self, "Attenzione", "Seleziona un cliente valido dall'elenco")
            return

        connessione = None
        try:
            connessione = pyodbc.connect(
                "Driver={ODBC Driver 18 for SQL Server};"
                f"Server={D_HOST};"
                f"Database={D_NAME};"  # Usiamo la variabile dinamica invece del nome fisso
                f"UID={D_USER};"       # Inserisce l'utente del file config.ini
                f"PWD={D_PASS};"       # Inserisce la password del file config.ini
                "TrustServerCertificate=yes;"  # Fondamentale per evitare il blocco SSL locale
            )

            cursore = connessione.cursor()
            connessione.autocommit = False

            # Recupero il codice base del preventivo esistente, se presente
            if self.codice_preventivo_corrente:
                codice_base = self.codice_preventivo_corrente.split('-REV')[0]

                # Recupero il massimo numero di revisione per il codice base del preventivo
                cursore.execute("""
                SELECT COALESCE(MAX(CAST(SUBSTRING(numero_preventivo, CHARINDEX('-REV', numero_preventivo) + 4, LEN(numero_preventivo)) AS INT)), 0) 
                FROM configuratore.preventivi 
                WHERE numero_preventivo LIKE ?
                """, (f"{codice_base}-REV%",))

                # Recupero il massimo numero progressivo per l'anno corrente
                risultato_rev_row = cursore.fetchone()
                
                # Estraiamo l'indice 0 in modo sicuro dalla riga/tupla di pyodbc
                valore_numerico = 0
                if risultato_rev_row and risultato_rev_row[0] is not None:
                    valore_numerico = int(risultato_rev_row[0])
                
                nuova_revisione = valore_numerico + 1
                codice_finale = f"{codice_base}-REV{nuova_revisione}"

            else:

                cursore.execute("""
                    SELECT COALESCE(MAX(CAST(SUBSTRING(numero_preventivo, CHARINDEX('-', numero_preventivo) + 1, LEN(numero_preventivo)) AS INT)), 0) 
                    FROM configuratore.preventivi 
                    WHERE anno_preventivo = ? AND numero_preventivo NOT LIKE '%-REV%'
                """, (anno_corrente,))

                risultato_row = cursore.fetchone()

                # Estraiamo l'indice 0 in modo sicuro dalla riga/tupla di pyodbc
                valore_numerico = 0
                if risultato_row and risultato_row[0] is not None:
                    valore_numerico = int(risultato_row[0])
                    
                nuovo_progressivo = valore_numerico + 1
                codice_finale = f"{anno_corrente}-{nuovo_progressivo:04d}"

            self.nuovo_preventivo.numero = codice_finale

            cursore.close()
            cursore = connessione.cursor()

            query_testata = """
                INSERT INTO configuratore.preventivi (
                    numero_preventivo, anno_preventivo, cliente_id, data_creazione, consegna, imballo, validita
                ) 
                OUTPUT INSERTED.id_preventivo
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            valori_testata = (self.nuovo_preventivo.numero, self.nuovo_preventivo.anno, self.cliente_id_corrente, self.nuovo_preventivo.data_creazione,
                self.nuovo_preventivo.consegna, self.nuovo_preventivo.imballo, self.nuovo_preventivo.validita)
                    
            cursore.execute(query_testata, valori_testata)

            risultato_id_prev = cursore.fetchone()
            if risultato_id_prev:
                self.id_preventivo_generato = int(risultato_id_prev[0])
            else:
                raise Exception("Impossibile recuperare l'ID del nuovo preventivo.")

            numero_righe = self.ui.tb_righe.rowCount()

            for i in range(numero_righe):
                qta_txt = self.ui.tb_righe.item(i, 1).text() if self.ui.tb_righe.item(i, 1) else "1"
                codice_txt = self.ui.tb_righe.item(i, 2).text() if self.ui.tb_righe.item(i, 2) else ""
                prezzo_txt = self.ui.tb_righe.item(i, 3).text() if self.ui.tb_righe.item(i, 3) else ""
                sconto_txt = self.ui.tb_righe.item(i, 4).text() if self.ui.tb_righe.item(i, 4) else "0"
                desc_txt = self.ui.tb_righe.item(i, 5).text() if self.ui.tb_righe.item(i, 5) else ""

                if prezzo_txt == "":
                    desc_txt = self.ui.tb_righe.item(i, 0).text() if self.ui.tb_righe.item(i, 0) else ""

                riga_oggetto = Preventivo_riga()
                riga_oggetto.numero_riga = i
                riga_oggetto.qta = int(qta_txt) if qta_txt.isdigit() else 1
                riga_oggetto.codice = codice_txt
                riga_oggetto.prezzo = float(prezzo_txt.replace(",", ".")) if prezzo_txt else 0.0
                riga_oggetto.sconto = float(sconto_txt.replace(",", ".")) if sconto_txt else 0.0
                riga_oggetto.descrizione = desc_txt

                self.nuovo_preventivo.aggiungi_riga_preventivo(riga_oggetto)

                query_dettagli = "INSERT INTO configuratore.preventivi_dettaglio (preventivo_id, numero_riga, quantita, codice, prezzo, sconto, descrizione_personalizzata) VALUES (?, ?, ?, ?, ?, ?, ?)"
                valori_dettagli = (self.id_preventivo_generato, riga_oggetto.numero_riga, riga_oggetto.qta, riga_oggetto.codice, riga_oggetto.prezzo, riga_oggetto.sconto, riga_oggetto.descrizione)

                cursore.execute(query_dettagli, valori_dettagli)

            connessione.commit()
            cursore.close()
            connessione.close()  # La connessione al DB è chiusa con successo, i dati sono al sicuro!
            connessione = None

        except Exception as e:

            if connessione:
                connessione.rollback()
                connessione.close()
            QMessageBox.critical(self, "Errore Database", f"Problema con il salvataggio dei dati:\n{e}")
            return # Interrompiamo l'esecuzione per non generare un PDF con dati non salvati
        
        try:

            doc = SimpleDocTemplate(
                percorso_salvataggio, 
                pagesize=letter,
                rightMargin=36, leftMargin=36, topMargin=90, bottomMargin=80
            )
            story = []
            
            styles = getSampleStyleSheet()
            
            stile_titolo = ParagraphStyle(
                'TitoloPreventivo', parent=styles['Heading1'],
                fontSize=18, leading=26, textColor=colors.HexColor("#1A365D"), spaceAfter=15
            )
            stile_sottotitolo = ParagraphStyle(
                'SezioneTitolo', parent=styles['Heading2'],
                fontSize=12, leading=16, textColor=colors.HexColor("#1A365D"), spaceBefore=15, spaceAfter=5
            )
            stile_normale = ParagraphStyle(
                'TestoNormale', parent=styles['Normal'],
                fontSize=9, leading=13, textColor=colors.HexColor("#2D3748")
            )
            stile_testo_libero = ParagraphStyle(
                'TestoLiberoTabella', parent=styles['Normal'],
                fontSize=9, leading=13, fontName="Helvetica-BoldOblique", textColor=colors.HexColor("#4A5568")
            )
            stile_inv_tabella = ParagraphStyle(
                'IntestazioneTabella', parent=styles['Normal'],
                fontSize=9.5, leading=12, fontName="Helvetica-Bold", textColor=colors.white
            )

            # --- INTESTAZIONE GRAFICA ---
            story.append(Paragraph(f"<b>PREVENTIVO COMMERCIALE {codice_finale}</b>", stile_titolo))
            story.append(Spacer(1, 5))
            
            # --- BLOCCO ANAGRAFICA (Mittente e Destinatario) ---
            ragione_sociale = self.ui.cbCliente.currentText()
            
            corpo_mittente = """
            <b>Mittente:</b><br/>
            Euroma Group srl<br/>
            Via Cavour 5, 40012 Calderara di Reno (BO)<br/>
            P.IVA: 00547741207<br/>
            Email: info@euromagroup.com
            """
            
            corpo_destinatario = f"""
            <b>Destinatario:</b><br/>
            {ragione_sociale}<br/>
            {self.ui.tbIndirizzo.text()}<br/>
            {self.ui.tbCap.text()} {self.ui.tbCitta.text()} ({self.ui.tbPV.text()})<br/>
            P.IVA: {self.ui.tbPiva.text()} | C.F.: {self.ui.tbCF.text()}<br/>
            Tel: {self.ui.tbTelefono.text()} | Email: {self.ui.tbEmail.text()}
            All'Attenzione del sig. {self.ui.cbReferente.currentText()}
            """
            
            dati_anagrafica = [
                [Paragraph(corpo_mittente, stile_normale), Paragraph(corpo_destinatario, stile_normale)]
            ]
            
            tabella_anagrafica = Table(dati_anagrafica, colWidths=[270, 270])
            tabella_anagrafica.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 15),
            ]))
            story.append(tabella_anagrafica)
            story.append(Spacer(1, 10))

            # --- TABELLA ARTICOLI E TESTI LIBERI ---
            story.append(Paragraph("<b>Dettaglio Fornitura</b>", stile_sottotitolo))

            testo_introduzione = "A seguito della Vostra gentile richiesta, siamo a sottoporre la nostra proposta commerciale:"
            story.append(Paragraph(testo_introduzione, stile_normale))
            story.append(Spacer(1, 5)) 
            
            dati_prodotti = [[
                Paragraph("Articolo", stile_inv_tabella),
                Paragraph("Prezzo lordo", stile_inv_tabella),
                Paragraph("Q.tà", stile_inv_tabella),
                Paragraph("Sconto", stile_inv_tabella),
                Paragraph("Prezzo netto", stile_inv_tabella)
            ]]
            
            totale_preventivo = Decimal('0.00')
            totale_righe = self.ui.tb_righe.rowCount()
            
            # Ci serve tenere traccia di quali righe sono "Testo Libero" per applicare lo stile grafico di unione celle dopo
            indici_righe_testo = []
            
            for riga in range(totale_righe):
                qta_str = self.ui.tb_righe.item(riga, 1).text() if self.ui.tb_righe.item(riga, 1) else "1"
                codice = self.ui.tb_righe.item(riga, 2).text() if self.ui.tb_righe.item(riga, 2) else ""
                prezzo_str = self.ui.tb_righe.item(riga, 3).text() if self.ui.tb_righe.item(riga, 3) else ""
                sconto_str = self.ui.tb_righe.item(riga, 4).text() if self.ui.tb_righe.item(riga, 4) else ""
                descrizione_prodotto = self.ui.tb_righe.item(riga, 5).text() if self.ui.tb_righe.item(riga, 5) else ""

                # --- IDENTIFICAZIONE RIGA DI TESTO LIBERO ---
                # Se la cella del prezzo è vuota, significa che è una riga di testo inserita da btn_aggiungi_testo_click
                if prezzo_str == "":
                    indici_righe_testo.append(riga + 1) # +1 perché c'è l'intestazione della tabella alla riga 0
                    
                    # Prendiamo il testo libero dalla colonna 1 (dove lo avevi salvato nel setItem di testo_libero)
                    testo_libero_str = self.ui.tb_righe.item(riga, 0).text() if self.ui.tb_righe.item(riga, 0) else ""
                    
                    dati_prodotti.append([
                        Paragraph(testo_libero_str, stile_testo_libero),
                        "", "", "" # Lasciamo vuoti gli spazi del prezzo per questa riga
                    ])
                    continue # Salta al ciclo successivo senza fare calcoli commerciali

                # --- GESTIONE RIGHE ARTICOLO / ACCESSORIO STANDARD ---
                cella_articolo = f"<b>{codice}</b>"
                if descrizione_prodotto:
                    desc_formattata = descrizione_prodotto.replace("\n", "<br/>")
                    cella_articolo += f"<br/><font color='#4A5568'>{desc_formattata}</font>"

                prezzo_listino = Decimal(prezzo_str.replace(",", ".")) if prezzo_str else Decimal('0.00')
                quantita = Decimal(qta_str) if qta_str else Decimal('1')
                sconto = Decimal(sconto_str.replace(",", ".")) if sconto_str else Decimal('0.00')
                prezzo_scontato_unitario = prezzo_listino * (Decimal('1.00') - (sconto / Decimal('100.00')))
                totale_riga = prezzo_scontato_unitario * quantita

                totale_preventivo += totale_riga
            
                cella_articolo = f"<b>{codice}</b>"
                if descrizione_prodotto:
                    desc_formattata = descrizione_prodotto.replace("\n", "<br/>")
                    cella_articolo += f"<br/><font color='#4A5568'>{desc_formattata}</font>"

                dati_prodotti.append([
                    Paragraph(cella_articolo, stile_normale),
                    Paragraph(f"&euro; {prezzo_listino:.2f}", stile_normale),
                    Paragraph(str(quantita), stile_normale),
                    Paragraph(f"{sconto:.0f}%" if sconto > 0 else "-", stile_normale),
                    Paragraph(f"<b>&euro; {totale_riga:.2f}</b>", stile_normale)
                ])
                
            # Riga del Totale Fornitura
            dati_prodotti.append([
            "", "", "",
            Paragraph("<b>TOTALE FORNITURA:</b>", stile_normale),
            Paragraph(f"<b>&euro; {totale_preventivo:.2f}</b>", stile_normale)
            ])
            
            # Costruzione degli stili della tabella articoli
            stili_tabella = [
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('TOPPADDING', (0,0), (-1,-1), 6),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#F7FAFC")]),
                ('LINEBELOW', (0,-1), (-1,-1), 1.5, colors.HexColor("#1A365D")),
                ('GRID', (0,0), (-1,-2), 0.5, colors.HexColor("#E2E8F0")),
            ]
            
            # Applichiamo l'unione delle celle (SPAN) per le righe che contengono solo il testo libero
            for idx in indici_righe_testo:
                stili_tabella.append(('SPAN', (0, idx), (4, idx))) 
                stili_tabella.append(('BACKGROUND', (0, idx), (4, idx), colors.HexColor("#EDF2F7")))

            tabella_articoli = Table(dati_prodotti, colWidths=[280, 70, 40, 70, 80])
            tabella_articoli.setStyle(TableStyle(stili_tabella))
            story.append(tabella_articoli)
            
            # --- CONDIZIONI DI VENDITA IN CALCE ---
            story.append(Spacer(1, 20))
            story.append(Paragraph("<b>Condizioni generali di vendita</b>", stile_sottotitolo))
            
            pagamento_cli = self.ui.cbPagamento.currentText()
            corriere_cli = self.ui.cbTrasporto.currentText()
            resa_cli = self.ui.cbResa.currentText()
            
            # Recuperiamo i nuovi valori inseriti a schermo (Assicurati che questi widget esistano con questi nomi o adatta i nomi se diversi)
            consegna_val = self.ui.tbConsegna.text() if hasattr(self.ui, "tbConsegna") else "Da definire"
            imballo_val = self.ui.cbImballo.currentText() if hasattr(self.ui, "cbImballo") else "Al costo"
            validita_val = self.ui.tbValidita.text() if hasattr(self.ui, "tbValidita") else "30 giorni"

            corpo_condizioni = f"""
            • <b>Condizioni di Pagamento:</b> {pagamento_cli or "Da definire"}<br/>
            • <b>Resa Merce (Incoterms):</b> {resa_cli or "EXW - Franco Fabbrica"}<br/>
            • <b>Porto / Trasporto:</b> Tramite corriere {corriere_cli or "Nostro incaricato"}<br/>
            • <b>Tempi di Consegna:</b> {consegna_val}<br/>
            • <b>Imballo:</b> {imballo_val}<br/>
            • <b>Validità Offerta:</b> {validita_val}
            """
            story.append(Paragraph(corpo_condizioni, stile_normale))
            story.append(Spacer(1, 20))

            firma_finale = "Cordiali saluti,<br/>Euroma Group srl"
            story.append(Paragraph(firma_finale, stile_normale))
            story.append(Spacer(1, 20)) 
            
            # --- FOOTER / DISCLAIMER OBBLIGATORIO ---
            stile_nota = ParagraphStyle(
                'NotaCalce', parent=styles['Italic'],
                fontSize=7.5, leading=10, textColor=colors.HexColor("#A0AEC0")
            )
            story.append(Paragraph("This is for informational purposes only. For medical advice or diagnosis, consult a professional. AI responses may include mistakes.", stile_nota))

            doc.build(story, onFirstPage=disegna_grafica_preventivo, onLaterPages=disegna_grafica_preventivo)

            QMessageBox.information(self, "Successo", "Preventivo PDF generato correttamente secondo le specifiche!")
            self.ui.lb_preventivo.setText(f"PREVENTIVO {self.codice_preventivo_corrente}")

            self.reset_condizioni()
            self.ui.cbProdotto.setCurrentIndex(-1)
            self.ui.cbReferente.setEnabled(True)
            self.ui.cbReferente.clear()
            self.ui.btn_agg_referente.setEnabled(True)
            self.ui.btn_elim_referente.setEnabled(True)
            self.ui.frmCliente.setEnabled(True)
            self.ui.btn_salva.setEnabled(True)
            self.ui.btn_modifica.setEnabled(False)
            self.ui.cbCliente.setCurrentIndex(-1)
            self.ui.tbIndirizzo.setText("Indirizzo")
            self.ui.tbCap.setText("CAP")
            self.ui.tbCitta.setText("Città")
            self.ui.tbPV.setText("PV")
            self.ui.tbPiva.setText("Partita IVA")
            self.ui.tbCF.setText("Codice Fiscale")
            self.ui.tbTelefono.setText("Telefono")
            self.ui.tbEmail.setText("E-mail")
            self.ui.cbCategoria.setCurrentIndex(-1)
            self.ui.cbPagamento.setCurrentIndex(-1)
            self.ui.tbSconto.clear()
            self.ui.cbTrasporto.setCurrentIndex(-1)
            self.ui.cbResa.setCurrentIndex(-1)
            self.ui.cbReferente.setCurrentIndex(-1)
            self.ui.tbConsegna.clear()
            self.ui.cbImballo.setCurrentIndex(-1)
            self.ui.tbValidita.clear()
            self.ui.tbConsegna.setEnabled(False)
            self.ui.cbImballo.setEnabled(False)
            self.ui.tbValidita.setEnabled(False)
            self.ui.frmCliente.setEnabled(False)
            self.ui.btn_salva.setEnabled(False)
            self.ui.btn_modifica.setEnabled(False)
            self.ui.btn_agg_referente.setEnabled(False)
            self.ui.btn_elim_referente.setEnabled(False)
            
            for riga in range(self.ui.tb_righe.rowCount()):
                self.ui.tb_righe.removeRow(0)
     
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile creare il file PDF.\n"
            f"Verifica che il documento non sia già aperto in Adobe o in un altro lettore:\n{e}")

    def carica_preventivo(self):
        popup = UfPreventivo(self)
        if popup.exec() == QDialog.Accepted:
            id_da_caricare = popup.id_preventivo_scelto
            self.ricostruisci_interfaccia_preventivo(id_da_caricare)
            self.ui.btn_elimina_preventivo.setEnabled(True)
            self.ui.tb_righe.setEnabled(True)
            self.ui.btn_aggiungi_testo.setEnabled(True)
            self.ui.btn_aggiungi_accessorio.setEnabled(True)
            self.ui.btn_sposta_giu.setEnabled(True)
            self.ui.btn_sposta_su.setEnabled(True)
            self.ui.btn_elimina_riga.setEnabled(True)
            self.ui.cbCliente.setEnabled(False)
            self.ui.lb_preventivo.setText(f"PREVENTIVO {self.codice_preventivo_corrente}")

    def ricostruisci_interfaccia_preventivo(self, id_preventivo):
        try:
            connessione = pyodbc.connect(
                "Driver={ODBC Driver 18 for SQL Server};"
                f"Server={D_HOST};"
                f"Database={D_NAME};"  # Usiamo la variabile dinamica invece del nome fisso
                f"UID={D_USER};"       # Inserisce l'utente del file config.ini
                f"PWD={D_PASS};"       # Inserisce la password del file config.ini
                "TrustServerCertificate=yes;"
            )

            cursore = connessione.cursor()

            # Funzione locale per trasformare le righe di pyodbc in dizionari reali
            def fetch_as_dict(cur):
                columns = [column[0] for column in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]
            
            query_testata = """
                SELECT p.*, c.ragione_sociale 
                FROM configuratore.preventivi p
                JOIN configuratore.clienti c ON p.cliente_id = c.id
                WHERE p.id_preventivo = ?
            """
            cursore.execute(query_testata, (id_preventivo,))

            testate_diz = fetch_as_dict(cursore)
            if not testate_diz:
                QMessageBox.warning(self, "Errore", "Preventivo non trovato nel database.")
                cursore.close()
                connessione.close()
                return

            testata = testate_diz[0]

            self.id_preventivo_corrente = id_preventivo 
            self.codice_preventivo_corrente = testata['numero_preventivo']

            self.ui.cbCliente.blockSignals(True)
            
            self.ui.cbCliente.setCurrentText(testata['ragione_sociale'])
            self.cliente_id_corrente = testata['cliente_id']
            
            self.cbCliente_click() # Questo ricarica i dati anagrafici standard dell'azienda
            
            self.ui.cbCliente.blockSignals(False)

            self.ui.tbConsegna.setText(testata['consegna'] or "")
            self.ui.cbImballo.setCurrentText(testata['imballo'] or "")
            self.ui.tbValidita.setText(testata['validita'] or "")

            query_dettagli = """
                SELECT * FROM configuratore.preventivi_dettaglio 
                WHERE preventivo_id = ? 
                ORDER BY numero_riga ASC
            """
            cursore.execute(query_dettagli, (id_preventivo,))
            righe_db = fetch_as_dict(cursore)

            self.ui.tb_righe.setRowCount(0)

            for riga in righe_db:
                riga_successiva = self.ui.tb_righe.rowCount()
                self.ui.tb_righe.insertRow(riga_successiva)

                qta_str = str(riga['quantita'])
                codice_str = str(riga['codice']) if riga['codice'] else ""
                p_val = float(riga['prezzo']) if riga['prezzo'] is not None else 0.0
                s_val = float(riga['sconto']) if riga['sconto'] is not None else 0.0
                prezzo_str = f"{p_val:.2f}" if p_val > 0 else ""
                sconto_str = f"{s_val:.0f}" if s_val > 0 else ""
                desc_str = str(riga['descrizione_personalizzata']) if riga['descrizione_personalizzata'] else ""

                qta_item = QTableWidgetItem(qta_str)
                codice_item = QTableWidgetItem(codice_str)
                prezzo_item = QTableWidgetItem(prezzo_str)
                sconto_item = QTableWidgetItem(sconto_str)
                desc_nascosta_item = QTableWidgetItem(desc_str)

                if prezzo_str == "" and codice_str == "":
                    testo_libero_item = QTableWidgetItem(desc_str)
                    self.ui.tb_righe.setItem(riga_successiva, 0, testo_libero_item)
                else:
                    codice_item.setFlags(codice_item.flags() & ~Qt.ItemIsEditable)
                    prezzo_item.setFlags(prezzo_item.flags() & ~Qt.ItemIsEditable)

                self.ui.tb_righe.setItem(riga_successiva, 1, qta_item)
                self.ui.tb_righe.setItem(riga_successiva, 2, codice_item)
                self.ui.tb_righe.setItem(riga_successiva, 3, prezzo_item)
                self.ui.tb_righe.setItem(riga_successiva, 4, sconto_item)
                self.ui.tb_righe.setItem(riga_successiva, 5, desc_nascosta_item)

            self.ui.tb_righe.setColumnHidden(5, True)

            cursore.close()
            connessione.close()
            
            QMessageBox.information(self, "Successo", f"Preventivo {testata['numero_preventivo']} ricaricato a schermo!")

            self.reset_condizioni()
            self.ui.cbProdotto.setCurrentIndex(-1)
                        
        except Exception as e:
            QMessageBox.critical(self, "Errore Caricamento", f"Impossibile ricostruire il preventivo:\n{e}")

    def elimina_preventivo(self):
        if not hasattr(self, 'id_preventivo_corrente') or self.id_preventivo_corrente is None:
            QMessageBox.warning(
                self, 
                "Operazione annullata", 
                "Impossibile eliminare: nessun preventivo caricato a schermo.\n"
                "Apri prima un preventivo dall'archivio."
            )
            return
        
        risposta = QMessageBox.question(
            self,
            "Conferma Eliminazione",
            f"Sei sicuro di voler eliminare definitivamente il preventivo {self.codice_preventivo_corrente}?\n"
            "L'operazione cancellerà anche tutti i dettagli associati e non sarà reversibile.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if risposta == QMessageBox.Yes:
            self.esegui_eliminazione_preventivo_db(self.id_preventivo_corrente, self.codice_preventivo_corrente)
            
            self.id_preventivo_corrente = None
            self.codice_preventivo_corrente = None

            self.ui.cbCliente.setEnabled(True)
            self.ui.lb_preventivo.setText("")
            self.ui.cbProdotto.setCurrentIndex(-1)
            self.ui.cbReferente.setEnabled(True)
            self.ui.cbReferente.clear()
            self.ui.btn_agg_referente.setEnabled(True)
            self.ui.btn_elim_referente.setEnabled(True)
            self.ui.frmCliente.setEnabled(True)
            self.ui.btn_salva.setEnabled(True)
            self.ui.btn_modifica.setEnabled(False)
            self.ui.cbCliente.setCurrentIndex(-1)
            self.ui.tbIndirizzo.setText("Indirizzo")
            self.ui.tbCap.setText("CAP")
            self.ui.tbCitta.setText("Città")
            self.ui.tbPV.setText("PV")
            self.ui.tbPiva.setText("Partita IVA")
            self.ui.tbCF.setText("Codice Fiscale")
            self.ui.tbTelefono.setText("Telefono")
            self.ui.tbEmail.setText("E-mail")
            self.ui.cbCategoria.setCurrentIndex(-1)
            self.ui.cbPagamento.setCurrentIndex(-1)
            self.ui.tbSconto.clear()
            self.ui.cbTrasporto.setCurrentIndex(-1)
            self.ui.cbResa.setCurrentIndex(-1)
            self.ui.cbReferente.setCurrentIndex(-1)
            self.ui.tbConsegna.clear()
            self.ui.cbImballo.setCurrentIndex(-1)
            self.ui.tbValidita.clear()
            self.ui.tbConsegna.setEnabled(False)
            self.ui.cbImballo.setEnabled(False)
            self.ui.tbValidita.setEnabled(False)
            self.ui.frmCliente.setEnabled(False)
            self.ui.btn_salva.setEnabled(False)
            self.ui.btn_modifica.setEnabled(False)
            self.ui.btn_agg_referente.setEnabled(False)
            self.ui.btn_elim_referente.setEnabled(False)
            selfui.btn_elimina_preventivo.setEnabled(False)

    def esegui_eliminazione_preventivo_db(self, id_preventivo, codice_preventivo):
        connessione = None
        try:
            connessione = pyodbc.connect(
                "Driver={ODBC Driver 18 for SQL Server};"
                f"Server={D_HOST};"
                f"Database={D_NAME};"  # Usiamo la variabile dinamica invece del nome fisso
                f"UID={D_USER};"       # Inserisce l'utente del file config.ini
                f"PWD={D_PASS};"       # Inserisce la password del file config.ini
                "TrustServerCertificate=yes;"
            )
            cursore = connessione.cursor()
            connessione.autocommit = False

            #  1. CANCELLIAMO PRIMA I DETTAGLI (Evita errori di vincolo Foreign Key)
            query_dettagli = "DELETE FROM configuratore.preventivi_dettaglio WHERE preventivo_id = ?"
            cursore.execute(query_dettagli, (id_preventivo,))

            #  2. CANCELLIAMO LA TESTATA DEL PREVENTIVO
            query_eliminazione = "DELETE FROM configuratore.preventivi WHERE id_preventivo = ?"
            cursore.execute(query_eliminazione, (id_preventivo,))
            
            connessione.commit()
            cursore.close()
            
            # Svuotiamo la tabella grafica a schermo
            self.ui.tb_righe.setRowCount(0)
            
            QMessageBox.information(
                self, 
                "Eliminazione Completata", 
                f"Il preventivo {codice_preventivo} e tutti i suoi dettagli sono stati rimossi dal database."
            )

        except Exception as e:
            if connessione:
                connessione.rollback()
            QMessageBox.critical(
                self, 
                "Errore Eliminazione", 
                f"Impossibile eliminare il preventivo:\n{e}"
            )
        finally:
            if connessione:
                connessione.close()

    def apri_listino(self):
        login = LoginDialog(self)
        
        if login.exec() == login.DialogCode.Accepted:
            self.finestra_listino = ListinoEditorWindow()
            self.finestra_listino.show()



                