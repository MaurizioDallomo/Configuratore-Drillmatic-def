# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Referente.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_PopupReferente(object):
    def setupUi(self, PopupReferente):
        if not PopupReferente.objectName():
            PopupReferente.setObjectName(u"PopupReferente")
        PopupReferente.resize(675, 184)
        self.tbNome = QLineEdit(PopupReferente)
        self.tbNome.setObjectName(u"tbNome")
        self.tbNome.setGeometry(QRect(10, 30, 211, 31))
        self.tbCognome = QLineEdit(PopupReferente)
        self.tbCognome.setObjectName(u"tbCognome")
        self.tbCognome.setGeometry(QRect(230, 30, 211, 31))
        self.tbEmail = QLineEdit(PopupReferente)
        self.tbEmail.setObjectName(u"tbEmail")
        self.tbEmail.setGeometry(QRect(450, 90, 211, 31))
        self.tbRuolo = QLineEdit(PopupReferente)
        self.tbRuolo.setObjectName(u"tbRuolo")
        self.tbRuolo.setGeometry(QRect(450, 30, 211, 31))
        self.tbTelefono = QLineEdit(PopupReferente)
        self.tbTelefono.setObjectName(u"tbTelefono")
        self.tbTelefono.setGeometry(QRect(10, 90, 211, 31))
        self.tbCellulare = QLineEdit(PopupReferente)
        self.tbCellulare.setObjectName(u"tbCellulare")
        self.tbCellulare.setGeometry(QRect(230, 90, 211, 31))
        self.lbNome = QLabel(PopupReferente)
        self.lbNome.setObjectName(u"lbNome")
        self.lbNome.setGeometry(QRect(10, 10, 49, 16))
        self.lbCognome = QLabel(PopupReferente)
        self.lbCognome.setObjectName(u"lbCognome")
        self.lbCognome.setGeometry(QRect(230, 10, 71, 16))
        self.lbRuolo = QLabel(PopupReferente)
        self.lbRuolo.setObjectName(u"lbRuolo")
        self.lbRuolo.setGeometry(QRect(450, 10, 49, 16))
        self.lb_tel = QLabel(PopupReferente)
        self.lb_tel.setObjectName(u"lb_tel")
        self.lb_tel.setGeometry(QRect(10, 70, 81, 16))
        self.lb_cell = QLabel(PopupReferente)
        self.lb_cell.setObjectName(u"lb_cell")
        self.lb_cell.setGeometry(QRect(230, 70, 101, 16))
        self.lbEmail = QLabel(PopupReferente)
        self.lbEmail.setObjectName(u"lbEmail")
        self.lbEmail.setGeometry(QRect(450, 70, 49, 16))
        self.btnOk = QPushButton(PopupReferente)
        self.btnOk.setObjectName(u"btnOk")
        self.btnOk.setGeometry(QRect(300, 140, 75, 31))
        QWidget.setTabOrder(self.tbNome, self.tbCognome)
        QWidget.setTabOrder(self.tbCognome, self.tbRuolo)
        QWidget.setTabOrder(self.tbRuolo, self.tbTelefono)
        QWidget.setTabOrder(self.tbTelefono, self.tbCellulare)
        QWidget.setTabOrder(self.tbCellulare, self.tbEmail)
        QWidget.setTabOrder(self.tbEmail, self.btnOk)

        self.retranslateUi(PopupReferente)

        QMetaObject.connectSlotsByName(PopupReferente)
    # setupUi

    def retranslateUi(self, PopupReferente):
        PopupReferente.setWindowTitle(QCoreApplication.translate("PopupReferente", u"Dialog", None))
        self.lbNome.setText(QCoreApplication.translate("PopupReferente", u"Nome", None))
        self.lbCognome.setText(QCoreApplication.translate("PopupReferente", u"Cognome", None))
        self.lbRuolo.setText(QCoreApplication.translate("PopupReferente", u"Ruolo", None))
        self.lb_tel.setText(QCoreApplication.translate("PopupReferente", u"Telefono fisso", None))
        self.lb_cell.setText(QCoreApplication.translate("PopupReferente", u"Telefono cellulare", None))
        self.lbEmail.setText(QCoreApplication.translate("PopupReferente", u"Email", None))
        self.btnOk.setText(QCoreApplication.translate("PopupReferente", u"Salva", None))
    # retranslateUi

