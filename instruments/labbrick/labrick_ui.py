# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Labbrick.ui'
#
# Created: Fri Sep 02 15:06:58 2011
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_labbrickWindow(object):
    def setupUi(self, labbrickWindow):
        labbrickWindow.setObjectName("labbrickWindow")
        labbrickWindow.resize(525, 260)
        self.centralwidget = QtGui.QWidget(labbrickWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(380, 50, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.frequencySpinBox = QtGui.QDoubleSpinBox(self.centralwidget)
        self.frequencySpinBox.setGeometry(QtCore.QRect(30, 50, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.frequencySpinBox.setFont(font)
        self.frequencySpinBox.setMinimum(5000.0)
        self.frequencySpinBox.setMaximum(10000.0)
        self.frequencySpinBox.setProperty("value", QtCore.QVariant(5000.0))
        self.frequencySpinBox.setObjectName("frequencySpinBox")
        self.powerSpinBox = QtGui.QDoubleSpinBox(self.centralwidget)
        self.powerSpinBox.setGeometry(QtCore.QRect(210, 50, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.powerSpinBox.setFont(font)
        self.powerSpinBox.setMinimum(-40.0)
        self.powerSpinBox.setMaximum(10.0)
        self.powerSpinBox.setSingleStep(0.5)
        self.powerSpinBox.setProperty("value", QtCore.QVariant(-10.0))
        self.powerSpinBox.setObjectName("powerSpinBox")
        self.pulsewidthSpinBox = QtGui.QDoubleSpinBox(self.centralwidget)
        self.pulsewidthSpinBox.setGeometry(QtCore.QRect(30, 130, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pulsewidthSpinBox.setFont(font)
        self.pulsewidthSpinBox.setDecimals(4)
        self.pulsewidthSpinBox.setMinimum(0.1)
        self.pulsewidthSpinBox.setMaximum(10000000.0)
        self.pulsewidthSpinBox.setSingleStep(0.1)
        self.pulsewidthSpinBox.setObjectName("pulsewidthSpinBox")
        self.pulserepSpinBox = QtGui.QDoubleSpinBox(self.centralwidget)
        self.pulserepSpinBox.setGeometry(QtCore.QRect(210, 130, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pulserepSpinBox.setFont(font)
        self.pulserepSpinBox.setDecimals(4)
        self.pulserepSpinBox.setMinimum(0.1)
        self.pulserepSpinBox.setMaximum(10000000.0)
        self.pulserepSpinBox.setSingleStep(0.1)
        self.pulserepSpinBox.setObjectName("pulserepSpinBox")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(210, 20, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 110, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(210, 110, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.checkBox_2 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(380, 130, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setObjectName("checkBox_2")
        self.updateButton = QtGui.QPushButton(self.centralwidget)
        self.updateButton.setGeometry(QtCore.QRect(30, 180, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.updateButton.setFont(font)
        self.updateButton.setObjectName("updateButton")
        self.checkBox_3 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(120, 180, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_3.setFont(font)
        self.checkBox_3.setObjectName("checkBox_3")
        self.generatorNumber = QtGui.QLCDNumber(self.centralwidget)
        self.generatorNumber.setGeometry(QtCore.QRect(370, 170, 121, 41))
        self.generatorNumber.setObjectName("generatorNumber")
        labbrickWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(labbrickWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 525, 22))
        self.menubar.setObjectName("menubar")
        labbrickWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(labbrickWindow)
        self.statusbar.setObjectName("statusbar")
        labbrickWindow.setStatusBar(self.statusbar)

        self.retranslateUi(labbrickWindow)
        QtCore.QMetaObject.connectSlotsByName(labbrickWindow)

    def retranslateUi(self, labbrickWindow):
        labbrickWindow.setWindowTitle(QtGui.QApplication.translate("labbrickWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("labbrickWindow", "RF Output", None, QtGui.QApplication.UnicodeUTF8))
        self.frequencySpinBox.setSuffix(QtGui.QApplication.translate("labbrickWindow", " MHz", None, QtGui.QApplication.UnicodeUTF8))
        self.powerSpinBox.setSuffix(QtGui.QApplication.translate("labbrickWindow", " dBm", None, QtGui.QApplication.UnicodeUTF8))
        self.pulsewidthSpinBox.setSuffix(QtGui.QApplication.translate("labbrickWindow", " us", None, QtGui.QApplication.UnicodeUTF8))
        self.pulserepSpinBox.setSuffix(QtGui.QApplication.translate("labbrickWindow", " us", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("labbrickWindow", "Frequency", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("labbrickWindow", "Power", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("labbrickWindow", "Pulse width", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("labbrickWindow", "Pulse Rep Interval", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_2.setText(QtGui.QApplication.translate("labbrickWindow", "Pulsed Output", None, QtGui.QApplication.UnicodeUTF8))
        self.updateButton.setText(QtGui.QApplication.translate("labbrickWindow", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_3.setText(QtGui.QApplication.translate("labbrickWindow", "Auto-update", None, QtGui.QApplication.UnicodeUTF8))

