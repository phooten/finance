# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
from PySide6.QtWidgets import (QApplication, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(436, 308)
        self.tickerListWidget = QListWidget(Widget)
        self.tickerListWidget.setObjectName(u"tickerListWidget")
        self.tickerListWidget.setGeometry(QRect(10, 10, 256, 192))
        self.filterButton = QPushButton(Widget)
        self.filterButton.setObjectName(u"filterButton")
        self.filterButton.setGeometry(QRect(20, 240, 100, 32))
        self.selectedTicker = QLabel(Widget)
        self.selectedTicker.setObjectName(u"selectedTicker")
        self.selectedTicker.setGeometry(QRect(180, 250, 58, 16))
        self.exitButton = QPushButton(Widget)
        self.exitButton.setObjectName(u"exitButton")
        self.exitButton.setGeometry(QRect(330, 270, 100, 32))

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.filterButton.setText(QCoreApplication.translate("Widget", u"PushButton", None))
        self.selectedTicker.setText(QCoreApplication.translate("Widget", u"TextLabel", None))
        self.exitButton.setText(QCoreApplication.translate("Widget", u"exit", None))
    # retranslateUi

