# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PopupPreventivo.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(447, 253)
        self.cb_Cliente = QComboBox(Dialog)
        self.cb_Cliente.setObjectName(u"cb_Cliente")
        self.cb_Cliente.setGeometry(QRect(10, 40, 400, 41))
        self.cb_anno = QComboBox(Dialog)
        self.cb_anno.setObjectName(u"cb_anno")
        self.cb_anno.setGeometry(QRect(10, 120, 131, 41))
        self.cb_preventivo = QComboBox(Dialog)
        self.cb_preventivo.setObjectName(u"cb_preventivo")
        self.cb_preventivo.setGeometry(QRect(10, 200, 131, 41))
        self.lb_preventivo = QLineEdit(Dialog)
        self.lb_preventivo.setObjectName(u"lb_preventivo")
        self.lb_preventivo.setGeometry(QRect(10, 170, 113, 22))
        self.lb_anno = QLineEdit(Dialog)
        self.lb_anno.setObjectName(u"lb_anno")
        self.lb_anno.setGeometry(QRect(10, 90, 113, 22))
        self.lb_cliente = QLineEdit(Dialog)
        self.lb_cliente.setObjectName(u"lb_cliente")
        self.lb_cliente.setGeometry(QRect(10, 10, 113, 22))
        self.btn_ok = QPushButton(Dialog)
        self.btn_ok.setObjectName(u"btn_ok")
        self.btn_ok.setGeometry(QRect(340, 180, 71, 51))
        self.btn_svuota_campi = QPushButton(Dialog)
        self.btn_svuota_campi.setObjectName(u"btn_svuota_campi")
        self.btn_svuota_campi.setGeometry(QRect(230, 200, 101, 31))
        QWidget.setTabOrder(self.cb_Cliente, self.cb_anno)
        QWidget.setTabOrder(self.cb_anno, self.cb_preventivo)
        QWidget.setTabOrder(self.cb_preventivo, self.btn_ok)
        QWidget.setTabOrder(self.btn_ok, self.btn_svuota_campi)
        QWidget.setTabOrder(self.btn_svuota_campi, self.lb_cliente)
        QWidget.setTabOrder(self.lb_cliente, self.lb_anno)
        QWidget.setTabOrder(self.lb_anno, self.lb_preventivo)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.lb_preventivo.setText(QCoreApplication.translate("Dialog", u"Preventivo", None))
        self.lb_anno.setText(QCoreApplication.translate("Dialog", u"Anno", None))
        self.lb_cliente.setText(QCoreApplication.translate("Dialog", u"Cliente", None))
        self.btn_ok.setText(QCoreApplication.translate("Dialog", u"OK", None))
        self.btn_svuota_campi.setText(QCoreApplication.translate("Dialog", u"Svuota campi", None))
    # retranslateUi

