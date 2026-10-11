# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MotoreSpeciale.ui'
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

class Ui_PopUpMotoreSpeciale(object):
    def setupUi(self, PopUpMotoreSpeciale):
        if not PopUpMotoreSpeciale.objectName():
            PopUpMotoreSpeciale.setObjectName(u"PopUpMotoreSpeciale")
        PopUpMotoreSpeciale.resize(233, 185)
        self.cbTaglia = QComboBox(PopUpMotoreSpeciale)
        self.cbTaglia.setObjectName(u"cbTaglia")
        self.cbTaglia.setGeometry(QRect(80, 21, 120, 30))
        self.cbTaglia.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.cbPoli = QComboBox(PopUpMotoreSpeciale)
        self.cbPoli.setObjectName(u"cbPoli")
        self.cbPoli.setGeometry(QRect(80, 100, 120, 30))
        self.cbPotenza = QComboBox(PopUpMotoreSpeciale)
        self.cbPotenza.setObjectName(u"cbPotenza")
        self.cbPotenza.setGeometry(QRect(80, 60, 120, 30))
        self.lbTaglia = QLabel(PopUpMotoreSpeciale)
        self.lbTaglia.setObjectName(u"lbTaglia")
        self.lbTaglia.setGeometry(QRect(20, 20, 41, 30))
        self.lbPoli = QLabel(PopUpMotoreSpeciale)
        self.lbPoli.setObjectName(u"lbPoli")
        self.lbPoli.setGeometry(QRect(20, 100, 31, 30))
        self.lbPotenza = QLabel(PopUpMotoreSpeciale)
        self.lbPotenza.setObjectName(u"lbPotenza")
        self.lbPotenza.setGeometry(QRect(20, 60, 51, 30))
        self.OkButton = QPushButton(PopUpMotoreSpeciale)
        self.OkButton.setObjectName(u"OkButton")
        self.OkButton.setGeometry(QRect(80, 140, 91, 31))
        QWidget.setTabOrder(self.cbTaglia, self.cbPotenza)
        QWidget.setTabOrder(self.cbPotenza, self.cbPoli)
        QWidget.setTabOrder(self.cbPoli, self.OkButton)

        self.retranslateUi(PopUpMotoreSpeciale)

        QMetaObject.connectSlotsByName(PopUpMotoreSpeciale)
    # setupUi

    def retranslateUi(self, PopUpMotoreSpeciale):
        PopUpMotoreSpeciale.setWindowTitle(QCoreApplication.translate("PopUpMotoreSpeciale", u"Dialog", None))
        self.lbTaglia.setText(QCoreApplication.translate("PopUpMotoreSpeciale", u"Taglia", None))
        self.lbPoli.setText(QCoreApplication.translate("PopUpMotoreSpeciale", u"Poli", None))
        self.lbPotenza.setText(QCoreApplication.translate("PopUpMotoreSpeciale", u"Potenza", None))
        self.OkButton.setText(QCoreApplication.translate("PopUpMotoreSpeciale", u"OK", None))
    # retranslateUi

