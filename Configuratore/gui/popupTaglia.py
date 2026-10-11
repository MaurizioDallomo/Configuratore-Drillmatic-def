# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PopupTaglia.ui'
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

class Ui_PopUpTaglia(object):
    def setupUi(self, PopUpTaglia):
        if not PopUpTaglia.objectName():
            PopUpTaglia.setObjectName(u"PopUpTaglia")
        PopUpTaglia.resize(196, 118)
        self.cbTaglia = QComboBox(PopUpTaglia)
        self.cbTaglia.setObjectName(u"cbTaglia")
        self.cbTaglia.setGeometry(QRect(18, 40, 151, 31))
        self.lbTaglia = QLabel(PopUpTaglia)
        self.lbTaglia.setObjectName(u"lbTaglia")
        self.lbTaglia.setGeometry(QRect(20, 10, 151, 21))
        self.lbTaglia.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.OkButton = QPushButton(PopUpTaglia)
        self.OkButton.setObjectName(u"OkButton")
        self.OkButton.setGeometry(QRect(50, 80, 91, 31))

        self.retranslateUi(PopUpTaglia)

        QMetaObject.connectSlotsByName(PopUpTaglia)
    # setupUi

    def retranslateUi(self, PopUpTaglia):
        PopUpTaglia.setWindowTitle(QCoreApplication.translate("PopUpTaglia", u"Dialog", None))
        self.lbTaglia.setText(QCoreApplication.translate("PopUpTaglia", u"Taglie Disponibili", None))
        self.OkButton.setText(QCoreApplication.translate("PopUpTaglia", u"OK", None))
    # retranslateUi

