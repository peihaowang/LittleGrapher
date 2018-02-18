
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import ListExpressions, GrapherView
import DlgEditExp

class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("SimpleGrapher")

        self.defaultColorList = [QColor(v) for v in [Qt.blue, Qt.green, Qt.red, Qt.darkYellow, Qt.darkGray, Qt.cyan]]

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
        self.actionDel.triggered.connect(self.onDelExpression)

        self.actionEdit = QAction(self)
        self.actionEdit.setEnabled(False)
        self.actionEdit.setText("Edit ...")
        self.actionEdit.setToolTip("Edit Selected Formula ...")
        self.actionEdit.setIcon(QIcon("./images/btn_edit.png"))
        self.actionEdit.triggered.connect(self.onEditExpression)

        self.listExps = ListExpressions.ListExpressions(self)
        self.listExps.setIconSize(QSize(16, 14))
        self.listExps.currentRowChanged.connect(self.onExpListCurrentRowChanged)

        self.dockExpList = QDockWidget(self)
        self.dockExpList.setWidget(self.listExps)

        titleBar = QToolBar(self)
        titleBar.setIconSize(QSize(16, 16))
        titleBar.addAction(self.actionAdd)
        titleBar.addAction(self.actionDel)
        titleBar.addAction(self.actionEdit)
        self.dockExpList.setTitleBarWidget(titleBar)

        self.addDockWidget(Qt.RightDockWidgetArea, self.dockExpList)

        self.grapherView = GrapherView.GrapherView(self)
        self.setCentralWidget(self.grapherView)

    def findUniqueStrokeColor(self):
        selColor = QColor(Qt.black)
        for color in self.defaultColorList:
            occupied = False
            for row in range(self.listExps.count()):
                item = self.listExps.item(row)
                if item.data(ListExpressions.ListExpressions.StrokeColorRole) == color:
                    occupied = True
                    break
            if not occupied:
                selColor = color
                break
        return selColor

    def onAddExpression(self):
        dlg = DlgEditExp.DlgEditExp("", self.findUniqueStrokeColor(), self)
        if dlg.exec_():
            self.listExps.addExpression(dlg.expression, dlg.strokeColor)
            if self.grapherView.addPlot({"exp": dlg.expression, "color": dlg.strokeColor.name()}):
                self.grapherView.updateGraph()
            else:
                self.listExps.setExpressionValidity(self.listExps.count() - 1, False)

    def onDelExpression(self):
        index = self.listExps.currentRow()
        self.listExps.takeItem(index)
        self.grapherView.delPlot(index)
        self.grapherView.updateGraph()

    def onEditExpression(self):
        index = self.listExps.currentRow()
        currentExp, currentColor = self.listExps.expressionOf(index)
        if not currentColor: currentColor = self.findUniqueStrokeColor()

        dlg = DlgEditExp.DlgEditExp(currentExp, currentColor, self)
        if dlg.exec_():
            self.listExps.setExpression(index, dlg.expression, dlg.strokeColor)
            if not self.grapherView.setPlot(index, {"exp": dlg.expression, "color": dlg.strokeColor.name()}):
                self.listExps.setExpressionValidity(index, False)
            self.grapherView.updateGraph()

    def onExpListCurrentRowChanged(self, currentRow):
        enabled = (currentRow >= 0)
        self.actionDel.setEnabled(enabled)
        self.actionEdit.setEnabled(enabled)
