#/home/fed/code/par_2/test2.py (ffe2a7e)

# from PyQt5 import QtWidgets, uic
# import sys

# app = QtWidgets.QApplication([])
# # расположение вашего файла .ui
# win = uic.loadUi("/home/fed/dev/src/pyqt_test/t1/mainwindow.ui")

# win.show()
# sys.exit(app.exec())


# from PyQt5 import QtWidgets

# # Импортируем наш шаблон.
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

# Импортируем наш шаблон.
from myform import Ui_MainWindow
from db_soc2 import *
import sys


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        query_1 = 'SELECT region_name FROM soc2.region;'
        headers = query_with_fetchall(query_1)
        for reg in headers:
            root = QTreeWidgetItem(self.ui.tree_widget, [reg[0]])
            items = query_with_fetchall(""" SELECT t.tournament_name
                      FROM soc2.tournament as t
                      where t.region_id_region=
                      (select r.`id_region` from soc2.region as r where r.`region_name`=\'%s\')
                       order by t.tournament_name; """ % reg[0])
            for val in items:
                item = QTreeWidgetItem(val)
                root.addChild(item)
        self.ui.sezon_comboBox.addItem('Выберите турнир')
        self.ui.sezon_comboBox.setEnabled(False)

        self.ui.tree_widget.itemClicked.connect(self.onItemClicked)

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def onItemClicked(self, it, col):
        if query_with_fetchone('SELECT id_region FROM soc2.region where region_name=\'%s\';' % it.text(col)):
            return
        self.ui.sezon_comboBox.setEnabled(True)
        self.ui.sezon_comboBox.clear()
        print(it, col, it.text(col))
        name_parent = self.ui.tree_widget.currentItem().parent().text(0)
        query_1 = """ SELECT sezon_name FROM soc2.sezon where id_sezon in 
                    (select sezon_id_sezon from sezon_has_tournament 
                    where tournament_id_tournament=
                    (select id_tournament from tournament where tournament_name=\'%s\'  
                    and region_id_region= (select id_region from region where region_name=\'%s\')))
                    order by sezon_name desc; """ % (it.text(col), name_parent)
        headers = query_with_fetchall(query_1)
        for s in headers:
            self.ui.sezon_comboBox.addItem(s[0])


app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())

# import sys

# from PyQt5.QtWidgets import *

# from db_soc2 import *


# app = QApplication(sys.argv)

# tree = QTreeWidget()

# query_1 = 'SELECT region_name FROM soc2.region;'
# headers = query_with_fetchall(query_1)
# for reg in headers:
#     root = QTreeWidgetItem(tree, [reg[0]])
#     items = query_with_fetchall(""" SELECT t.tournament_name
#               FROM soc2.tournament as t
#               where t.region_id_region=
#               (select r.`id_region` from soc2.region as r where r.`region_name`=\'%s\')
#                order by t.tournament_name; """ % reg[0])
#     for val in items:
#         item = QTreeWidgetItem(val)
#         root.addChild(item)

# # tree.expandAll()
# tree.show()
# sys.exit(app.exec_())

