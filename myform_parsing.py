# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsing.ui'
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
        self.region_treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.region_treeWidget.setGeometry(QtCore.QRect(0, 0, 256, 571))
        self.region_treeWidget.setObjectName("region_treeWidget")
        self.tournament_listView = QtWidgets.QListView(self.centralwidget)
        self.tournament_listView.setGeometry(QtCore.QRect(260, 0, 256, 192))
        self.tournament_listView.setObjectName("tournament_listView")
        self.parsing_tour_sezon_tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.parsing_tour_sezon_tableWidget.setGeometry(QtCore.QRect(260, 241, 531, 261))
        self.parsing_tour_sezon_tableWidget.setObjectName("parsing_tour_sezon_tableWidget")
        self.parsing_tour_sezon_tableWidget.setColumnCount(0)
        self.parsing_tour_sezon_tableWidget.setRowCount(0)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(409, 510, 381, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.parsing_pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.parsing_pushButton.setObjectName("parsing_pushButton")
        self.horizontalLayout.addWidget(self.parsing_pushButton)
        self.clear_pushButton_3 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.clear_pushButton_3.setObjectName("clear_pushButton_3")
        self.horizontalLayout.addWidget(self.clear_pushButton_3)
        self.exit_pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.exit_pushButton.setObjectName("exit_pushButton")
        self.horizontalLayout.addWidget(self.exit_pushButton)
        self.sezon_listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.sezon_listWidget.setGeometry(QtCore.QRect(540, 0, 256, 192))
        self.sezon_listWidget.setObjectName("sezon_listWidget")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(410, 200, 381, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.input_pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.input_pushButton.setObjectName("input_pushButton")
        self.horizontalLayout_2.addWidget(self.input_pushButton)
        self.input_all_pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.input_all_pushButton.setObjectName("input_all_pushButton")
        self.horizontalLayout_2.addWidget(self.input_all_pushButton)
        self.input_no_pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.input_no_pushButton.setObjectName("input_no_pushButton")
        self.horizontalLayout_2.addWidget(self.input_no_pushButton)
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
        self.region_treeWidget.headerItem().setText(0, _translate("MainWindow", "Страна/Регион"))
        self.parsing_pushButton.setText(_translate("MainWindow", "парсить"))
        self.clear_pushButton_3.setText(_translate("MainWindow", "очистить"))
        self.exit_pushButton.setText(_translate("MainWindow", "отмена"))
        self.input_pushButton.setText(_translate("MainWindow", "парсить"))
        self.input_all_pushButton.setText(_translate("MainWindow", "парсить все сезоны"))
        self.input_no_pushButton.setText(_translate("MainWindow", "не парсить"))


