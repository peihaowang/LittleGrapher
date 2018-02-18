
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import Utils

class ListExpressions(QListWidget):

    # 2018.2.18 Additional item roles
    ExpressionRole = Qt.UserRole + 1
    StrokeColorRole = Qt.UserRole + 2

    # # 2018.2.18 Signals
    # expressionAdded = pyqtSignal(str, QColor)

    def __init__(self, parent):
        super(ListExpressions, self).__init__(parent)
        #
        # self.defaultColorList = [QColor(v) for v in [Qt.blue, Qt.green, Qt.red, Qt.darkYellow, Qt.darkGray, Qt.cyan]]
        #
        # self.listExps = QListWidget(self)
        # self.listExps.setIconSize(QSize(16, 14))
        # self.setWidget(self.listExps)
        #
        # self.actionAdd = QAction(self)
        # self.actionAdd.setText("Add ...")
        # self.actionAdd.setToolTip("Add New Formula ...")
        # self.actionAdd.setIcon(QIcon("./images/btn_add.png"))
        # self.actionAdd.triggered.connect(self.onAddExpression)
        #
        # self.actionDel = QAction(self)
        # self.actionDel.setEnabled(False)
        # self.actionDel.setText("Delete ...")
        # self.actionDel.setToolTip("Delete Selected Formula ...")
        # self.actionDel.setIcon(QIcon("./images/btn_del.png"))
        #
        # self.actionEdit = QAction(self)
        # self.actionEdit.setEnabled(False)
        # self.actionEdit.setText("Edit ...")
        # self.actionEdit.setToolTip("Edit Selected Formula ...")
        # self.actionEdit.setIcon(QIcon("./images/btn_edit.png"))
        #
        # self.titleBar = QToolBar(self)
        # self.titleBar.setIconSize(QSize(16, 16))
        # self.titleBar.addAction(self.actionAdd)
        # self.titleBar.addAction(self.actionDel)
        # self.titleBar.addAction(self.actionEdit)
        #
        # self.setTitleBarWidget(self.titleBar)

    def addExpression(self, exp, strokeColor):
        item = QListWidgetItem()
        self.addItem(item)
        self.setExpression(self.count() - 1, exp, strokeColor)
        # item.setText(exp)
        # item.setIcon(QIcon(Utils.makeColorBlock(strokeColor, self.iconSize())))
        # item.setData(ListExpressions.ExpressionRole, exp)
        # item.setData(ListExpressions.StrokeColorRole, strokeColor)
        # item.setForeground(QBrush(Qt.black))
        # item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        # item.setCheckState(Qt.Checked)

    def setExpression(self, row, exp, strokeColor):
        item = self.item(row)
        if item:
            item.setText(exp)
            item.setIcon(QIcon(Utils.makeColorBlock(strokeColor, self.iconSize())))
            item.setData(ListExpressions.ExpressionRole, exp)
            item.setData(ListExpressions.StrokeColorRole, strokeColor)
            item.setForeground(QBrush(Qt.black))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked)

    def expressionOf(self, row):
        exp, strokeColor = "", None
        item = self.item(row)
        if item: exp, strokeColor = item.data(ListExpressions.ExpressionRole), item.data(ListExpressions.StrokeColorRole)
        return (exp, strokeColor)

    def setExpressionValidity(self, row, valid):
        item = self.item(row)
        if item: item.setForeground(QBrush(Qt.black if valid else Qt.red))
