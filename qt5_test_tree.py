#/home/fed/code/par_2/qt5_test_tree.py (ffe2a7e)

# # -*- coding: utf-8 -*-

# import sys
# from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
# from PyQt5.QtGui import QIcon


# class Example(QMainWindow):

#     def __init__(self):
#         super().__init__()

#         self.initUI()


#     def initUI(self):

#         textEdit = QTextEdit()
#         self.setCentralWidget(textEdit)

#         exitAction = QAction(QIcon('exit24.png'), 'Exit', self)
#         exitAction.setShortcut('Ctrl+Q')
#         exitAction.setStatusTip('Exit application')
#         exitAction.triggered.connect(self.close)

#         # self.statusBar()

#         menubar = self.menuBar()
#         fileMenu = menubar.addMenu('&File')
#         fileMenu.addAction(exitAction)

#         toolbar = self.addToolBar('Exit')
#         toolbar.addAction(exitAction)

#         self.setGeometry(300, 300, 350, 250)
#         self.setWindowTitle('Main window')
#         self.show()


# if __name__ == '__main__':

#     app = QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())
# -*- coding: utf-8 -*-

# import sys
# from PyQt5.QtWidgets import (
#     QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication)


# class Example(QWidget):

#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         okButton = QPushButton("OK")
#         cancelButton = QPushButton("Cancel")
#         hbox = QHBoxLayout()
#         hbox.addStretch(1)
#         hbox.addWidget(okButton)
#         hbox.addWidget(cancelButton)
#         vbox = QVBoxLayout()
#         vbox.addStretch(1)
#         vbox.addLayout(hbox)

#         self.setLayout(vbox)

#         self.setGeometry(300, 300, 300, 150)
#         self.setWindowTitle('Buttons')
#         self.show()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())
#
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtCore import *


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        db = QSqlDatabase.addDatabase('QMYSQL')
        db.setDatabaseName('soc2')
        db.setHostName('localhost:3306')
        db.setUserName('root')
        db.setPassword('trend')
        db.open()

        view = QTableView(self)
        model = QSqlQueryModel(self)
        model.setQuery('SELECT * FROM soc2.region;')
        view.setModel(model)
        view.move(10, 10)
        view.resize(617, 315)

        # Buttons:
        button1 = QPushButton('Exit', self)
        button1.resize(button1.sizeHint())
        button1.move(50, 400)

        def But1Click():
            if db.close():
                print('close')
            else:
                print('db dont close')
                sys.exit()
        button1.clicked.connect(But1Click)

        # Window:
        self.setGeometry(300, 100, 650, 450)
        self.setWindowTitle('Icon')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

