# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PopupOpzione.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QLabel,
    QLineEdit, QPlainTextEdit, QPushButton, QSizePolicy,
    QWidget)

class Ui_PopupOpzione(object):
    def setupUi(self, PopupOpzione):
        if not PopupOpzione.objectName():
            PopupOpzione.setObjectName(u"PopupOpzione")
        PopupOpzione.resize(351, 725)
        self.lb_titolo = QLabel(PopupOpzione)
        self.lb_titolo.setObjectName(u"lb_titolo")
        self.lb_titolo.setGeometry(QRect(110, 10, 121, 31))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        self.lb_titolo.setFont(font)
        self.lb_titolo.setTextFormat(Qt.TextFormat.PlainText)
        self.lb_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cb_opzioni_speciali = QComboBox(PopupOpzione)
        self.cb_opzioni_speciali.setObjectName(u"cb_opzioni_speciali")
        self.cb_opzioni_speciali.setEnabled(True)
        self.cb_opzioni_speciali.setGeometry(QRect(10, 50, 211, 41))
        self.cb_opzioni_speciali.setEditable(True)
        self.btn_agg_opz = QPushButton(PopupOpzione)
        self.btn_agg_opz.setObjectName(u"btn_agg_opz")
        self.btn_agg_opz.setGeometry(QRect(240, 50, 41, 41))
        self.btn_elim_opz = QPushButton(PopupOpzione)
        self.btn_elim_opz.setObjectName(u"btn_elim_opz")
        self.btn_elim_opz.setGeometry(QRect(290, 50, 41, 41))
        self.tb_descrizione = QPlainTextEdit(PopupOpzione)
        self.tb_descrizione.setObjectName(u"tb_descrizione")
        self.tb_descrizione.setEnabled(False)
        self.tb_descrizione.setGeometry(QRect(10, 130, 331, 151))
        self.tb_prezzo = QLineEdit(PopupOpzione)
        self.tb_prezzo.setObjectName(u"tb_prezzo")
        self.tb_prezzo.setEnabled(False)
        self.tb_prezzo.setGeometry(QRect(50, 290, 121, 31))
        self.tb_note = QPlainTextEdit(PopupOpzione)
        self.tb_note.setObjectName(u"tb_note")
        self.tb_note.setEnabled(False)
        self.tb_note.setGeometry(QRect(10, 370, 331, 211))
        self.tb_creatore = QLineEdit(PopupOpzione)
        self.tb_creatore.setObjectName(u"tb_creatore")
        self.tb_creatore.setEnabled(False)
        self.tb_creatore.setGeometry(QRect(10, 610, 201, 31))
        self.tb_data = QLineEdit(PopupOpzione)
        self.tb_data.setObjectName(u"tb_data")
        self.tb_data.setEnabled(False)
        self.tb_data.setGeometry(QRect(220, 610, 121, 31))
        self.lb_note = QLabel(PopupOpzione)
        self.lb_note.setObjectName(u"lb_note")
        self.lb_note.setGeometry(QRect(10, 340, 321, 16))
        self.lb_prezzo = QLabel(PopupOpzione)
        self.lb_prezzo.setObjectName(u"lb_prezzo")
        self.lb_prezzo.setGeometry(QRect(10, 300, 41, 16))
        self.lb_creatore = QLabel(PopupOpzione)
        self.lb_creatore.setObjectName(u"lb_creatore")
        self.lb_creatore.setGeometry(QRect(10, 590, 201, 16))
        self.lb_data = QLabel(PopupOpzione)
        self.lb_data.setObjectName(u"lb_data")
        self.lb_data.setGeometry(QRect(220, 590, 111, 16))
        self.btn_salva = QPushButton(PopupOpzione)
        self.btn_salva.setObjectName(u"btn_salva")
        self.btn_salva.setEnabled(False)
        self.btn_salva.setGeometry(QRect(40, 660, 121, 41))
        self.lb_consegna = QLabel(PopupOpzione)
        self.lb_consegna.setObjectName(u"lb_consegna")
        self.lb_consegna.setGeometry(QRect(210, 300, 61, 16))
        self.tb_consegna = QLineEdit(PopupOpzione)
        self.tb_consegna.setObjectName(u"tb_consegna")
        self.tb_consegna.setEnabled(False)
        self.tb_consegna.setGeometry(QRect(280, 290, 61, 31))
        self.lb_descrizione = QLabel(PopupOpzione)
        self.lb_descrizione.setObjectName(u"lb_descrizione")
        self.lb_descrizione.setGeometry(QRect(10, 110, 91, 16))
        self.btn_carica = QPushButton(PopupOpzione)
        self.btn_carica.setObjectName(u"btn_carica")
        self.btn_carica.setEnabled(False)
        self.btn_carica.setGeometry(QRect(190, 660, 121, 41))
        QWidget.setTabOrder(self.cb_opzioni_speciali, self.tb_descrizione)
        QWidget.setTabOrder(self.tb_descrizione, self.tb_prezzo)
        QWidget.setTabOrder(self.tb_prezzo, self.tb_consegna)
        QWidget.setTabOrder(self.tb_consegna, self.tb_note)
        QWidget.setTabOrder(self.tb_note, self.tb_creatore)
        QWidget.setTabOrder(self.tb_creatore, self.tb_data)
        QWidget.setTabOrder(self.tb_data, self.btn_salva)
        QWidget.setTabOrder(self.btn_salva, self.btn_carica)
        QWidget.setTabOrder(self.btn_carica, self.btn_agg_opz)
        QWidget.setTabOrder(self.btn_agg_opz, self.btn_elim_opz)

        self.retranslateUi(PopupOpzione)

        QMetaObject.connectSlotsByName(PopupOpzione)
    # setupUi

    def retranslateUi(self, PopupOpzione):
        PopupOpzione.setWindowTitle(QCoreApplication.translate("PopupOpzione", u"Dialog", None))
        self.lb_titolo.setText(QCoreApplication.translate("PopupOpzione", u"OPZIONI SPECIALI", None))
        self.btn_agg_opz.setText(QCoreApplication.translate("PopupOpzione", u"+", None))
        self.btn_elim_opz.setText(QCoreApplication.translate("PopupOpzione", u"-", None))
        self.lb_note.setText(QCoreApplication.translate("PopupOpzione", u"NOTE LIBERE (calcolo prezzo, dettagli sulla fattibilita)", None))
        self.lb_prezzo.setText(QCoreApplication.translate("PopupOpzione", u"Prezzo", None))
        self.lb_creatore.setText(QCoreApplication.translate("PopupOpzione", u"Inserito da", None))
        self.lb_data.setText(QCoreApplication.translate("PopupOpzione", u"Data", None))
        self.btn_salva.setText(QCoreApplication.translate("PopupOpzione", u"SALVA", None))
        self.lb_consegna.setText(QCoreApplication.translate("PopupOpzione", u"Consegna", None))
        self.lb_descrizione.setText(QCoreApplication.translate("PopupOpzione", u"Descrizione", None))
        self.btn_carica.setText(QCoreApplication.translate("PopupOpzione", u"CARICA", None))
    # retranslateUi

