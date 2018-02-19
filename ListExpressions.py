
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import Utils

class ListExpressions(QListWidget):

    # 2018.2.18 Additional item roles
    ExpressionRole = Qt.UserRole + 1
    StrokeColorRole = Qt.UserRole + 2
    ValidityRole = Qt.UserRole + 3

    # 2018.2.18 Signals
    itemCheckStateChanged = pyqtSignal(int, bool)

    def __init__(self, parent):
        super(ListExpressions, self).__init__(parent)

        self.switchUpdWhenItemChanged = Utils.Switch(True)

        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.itemChanged.connect(self.onItemChanged)

    def addExpression(self, expr, strokeColor):
        item = QListWidgetItem()
        self.addItem(item)
        self.setExpression(self.count() - 1, expr, strokeColor)

    def setExpression(self, row, expr, strokeColor):
        item = self.item(row)
        if item:
            with self.switchUpdWhenItemChanged:
                item.setText(expr)
                item.setIcon(QIcon(Utils.makeColorBlock(strokeColor, self.iconSize())))
                item.setData(ListExpressions.ExpressionRole, expr)
                item.setData(ListExpressions.StrokeColorRole, strokeColor)
                item.setData(ListExpressions.ValidityRole, True)
                item.setForeground(QBrush(Qt.black))
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Checked)

    def expressionOf(self, row):
        expr, strokeColor = "", None
        item = self.item(row)
        if item: expr, strokeColor = item.data(ListExpressions.ExpressionRole), item.data(ListExpressions.StrokeColorRole)
        return (expr, strokeColor)

    def isExpressionChecked(self, row):
        checked = False
        item = self.item(row)
        if item: checked = (item.checkState() == Qt.Checked)
        return checked

    def isExpressionValid(self, row):
        valid = False
        item = self.item(row)
        if item: valid = item.data(ListExpressions.ValidityRole)
        return valid

    def setExpressionValidity(self, row, valid):
        item = self.item(row)
        if item:
            with self.switchUpdWhenItemChanged:
                item.setData(ListExpressions.ValidityRole, valid)
                item.setForeground(QBrush(Qt.black if valid else Qt.red))

    def onItemChanged(self, item):
        if self.switchUpdWhenItemChanged:
            self.itemCheckStateChanged.emit(self.row(item), (item.checkState() == Qt.Checked))
