# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'popupPosizioneMotore.ui'
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
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(218, 141)
        self.cb_posizione_motore = QComboBox(Dialog)
        self.cb_posizione_motore.setObjectName(u"cb_posizione_motore")
        self.cb_posizione_motore.setGeometry(QRect(10, 40, 191, 41))
        self.lb_posizione_motore = QLabel(Dialog)
        self.lb_posizione_motore.setObjectName(u"lb_posizione_motore")
        self.lb_posizione_motore.setGeometry(QRect(60, 10, 101, 21))
        self.btn_ok = QPushButton(Dialog)
        self.btn_ok.setObjectName(u"btn_ok")
        self.btn_ok.setGeometry(QRect(60, 90, 91, 31))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.lb_posizione_motore.setText(QCoreApplication.translate("Dialog", u"Posizione motore", None))
        self.btn_ok.setText(QCoreApplication.translate("Dialog", u"OK", None))
    # retranslateUi

