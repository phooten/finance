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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QDateEdit, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QRadioButton, QSizePolicy, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(436, 407)
        self.tickerListWidget = QListWidget(Widget)
        self.tickerListWidget.setObjectName(u"tickerListWidget")
        self.tickerListWidget.setGeometry(QRect(10, 10, 256, 192))
        self.filterButton = QPushButton(Widget)
        self.filterButton.setObjectName(u"filterButton")
        self.filterButton.setGeometry(QRect(10, 370, 100, 32))
        self.labelStartDate = QLabel(Widget)
        self.labelStartDate.setObjectName(u"labelStartDate")
        self.labelStartDate.setGeometry(QRect(5, 210, 70, 15))
        self.exitButton = QPushButton(Widget)
        self.exitButton.setObjectName(u"exitButton")
        self.exitButton.setGeometry(QRect(330, 370, 100, 32))
        self.dateEditStart = QDateEdit(Widget)
        self.dateEditStart.setObjectName(u"dateEditStart")
        self.dateEditStart.setGeometry(QRect(80, 210, 110, 22))
        self.dateEditStart.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.dateEditStart.setCalendarPopup(True)
        self.dateEditStart.setDate(QDate(2024, 1, 1))
        self.labelEndDate = QLabel(Widget)
        self.labelEndDate.setObjectName(u"labelEndDate")
        self.labelEndDate.setGeometry(QRect(5, 240, 70, 15))
        self.dateEditEnd = QDateEdit(Widget)
        self.dateEditEnd.setObjectName(u"dateEditEnd")
        self.dateEditEnd.setGeometry(QRect(80, 240, 110, 22))
        self.dateEditEnd.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.dateEditEnd.setCalendarPopup(True)
        self.dateEditEnd.setDate(QDate(2024, 12, 31))
        self.radioButtonOptions = QRadioButton(Widget)
        self.radioButtonOptions.setObjectName(u"radioButtonOptions")
        self.radioButtonOptions.setGeometry(QRect(300, 50, 99, 20))
        self.radioButtonPuts = QRadioButton(Widget)
        self.radioButtonPuts.setObjectName(u"radioButtonPuts")
        self.radioButtonPuts.setGeometry(QRect(300, 70, 99, 20))
        self.radioButtonCalls = QRadioButton(Widget)
        self.radioButtonCalls.setObjectName(u"radioButtonCalls")
        self.radioButtonCalls.setGeometry(QRect(300, 90, 99, 20))
        self.radioButtonStocks = QRadioButton(Widget)
        self.radioButtonStocks.setObjectName(u"radioButtonStocks")
        self.radioButtonStocks.setGeometry(QRect(300, 110, 99, 20))
        self.radioButtonAll = QRadioButton(Widget)
        self.radioButtonAll.setObjectName(u"radioButtonAll")
        self.radioButtonAll.setGeometry(QRect(300, 30, 99, 20))
        self.radioButtonAll.setChecked(True)
        self.labelType = QLabel(Widget)
        self.labelType.setObjectName(u"labelType")
        self.labelType.setGeometry(QRect(300, 10, 70, 15))
        self.lineEditTicker = QLineEdit(Widget)
        self.lineEditTicker.setObjectName(u"lineEditTicker")
        self.lineEditTicker.setGeometry(QRect(90, 270, 113, 21))
        self.labelTicker = QLabel(Widget)
        self.labelTicker.setObjectName(u"labelTicker")
        self.labelTicker.setGeometry(QRect(10, 270, 70, 15))

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.filterButton.setText(QCoreApplication.translate("Widget", u"Filter", None))
        self.labelStartDate.setText(QCoreApplication.translate("Widget", u"Start Date", None))
        self.exitButton.setText(QCoreApplication.translate("Widget", u"exit", None))
        self.dateEditStart.setDisplayFormat(QCoreApplication.translate("Widget", u"M/d/yyyy", None))
        self.labelEndDate.setText(QCoreApplication.translate("Widget", u"End Date", None))
        self.dateEditEnd.setDisplayFormat(QCoreApplication.translate("Widget", u"M/d/yyyy", None))
        self.radioButtonOptions.setText(QCoreApplication.translate("Widget", u"Options", None))
        self.radioButtonPuts.setText(QCoreApplication.translate("Widget", u"Puts", None))
        self.radioButtonCalls.setText(QCoreApplication.translate("Widget", u"Calls", None))
        self.radioButtonStocks.setText(QCoreApplication.translate("Widget", u"Stocks", None))
        self.radioButtonAll.setText(QCoreApplication.translate("Widget", u"All", None))
        self.labelType.setText(QCoreApplication.translate("Widget", u"Type", None))
        self.labelTicker.setText(QCoreApplication.translate("Widget", u"End Date", None))
    # retranslateUi

