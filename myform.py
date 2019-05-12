#/home/fed/code/par_2/myform.py (ffe2a7e)

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'soc2_1.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tree_widget = QtWidgets.QTreeWidget(self.centralwidget)
        self.tree_widget.setGeometry(QtCore.QRect(0, 0, 201, 561))
        self.tree_widget.setObjectName("tree_widget")
        self.sezon_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.sezon_comboBox.setGeometry(QtCore.QRect(660, 30, 101, 25))
        self.sezon_comboBox.setObjectName("sezon_comboBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tree_widget.headerItem().setText(0, _translate("MainWindow", "Region"))



