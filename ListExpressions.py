
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import Utils, DlgAddExp

class ListExpressions(QDockWidget):

    # 2018.2.18 Additional item roles
    StrokeColorRole = Qt.UserRole + 1

    # 2018.2.18 Signals
    expressionAdded = pyqtSignal(str, QColor)

    def __init__(self, parent):
        super(ListExpressions, self).__init__(parent)

        self.defaultColorList = [QColor(v) for v in [Qt.blue, Qt.green, Qt.red, Qt.darkYellow, Qt.darkGray, Qt.cyan]]

        self.listExps = QListWidget(self)
        self.listExps.setIconSize(QSize(16, 14))
        self.setWidget(self.listExps)

        self.actionAdd = QAction(self)
        self.actionAdd.setText("Add ...")
        self.actionAdd.setToolTip("Add New Formula ...")
        self.actionAdd.setIcon(QIcon("./images/btn_add.png"))
        self.actionAdd.triggered.connect(self.onAddExpression)

        self.actionDel = QAction(self)
        self.actionDel.setEnabled(False)
        self.actionDel.setText("Delete ...")
        self.actionDel.setToolTip("Delete Selected Formula ...")
        self.actionDel.setIcon(QIcon("./images/btn_del.png"))

        self.actionEdit = QAction(self)
        self.actionEdit.setEnabled(False)
        self.actionEdit.setText("Edit ...")
        self.actionEdit.setToolTip("Edit Selected Formula ...")
        self.actionEdit.setIcon(QIcon("./images/btn_edit.png"))

        self.titleBar = QToolBar(self)
        self.titleBar.setIconSize(QSize(16, 16))
        self.titleBar.addAction(self.actionAdd)
        self.titleBar.addAction(self.actionDel)
        self.titleBar.addAction(self.actionEdit)

        self.setTitleBarWidget(self.titleBar)

    def addExpression(self, exp, strokeColor):
        item = QListWidgetItem()
        item.setText(exp)
        item.setIcon(QIcon(Utils.makeColorBlock(strokeColor, self.listExps.iconSize())))
        item.setData(ListExpressions.StrokeColorRole, strokeColor)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Checked)
        self.listExps.addItem(item)

    def findUniqueLineColor(self):
        selColor = QColor(Qt.black)
        for color in self.defaultColorList:
            occupied = False
            for row in range(self.listExps.count()):
                item = self.listExps.item(row)
                if item.data(ListExpressions.StrokeColorRole) == color:
                    occupied = True
                    break
            if not occupied:
                selColor = color
                break
        return selColor

    def onAddExpression(self):
        dlg = DlgAddExp.DlgAddExp(self.findUniqueLineColor(), self)
        if dlg.exec_():
            self.addExpression(dlg.expression, dlg.strokeColor)
            self.expressionAdded.emit(dlg.expression, dlg.strokeColor)
