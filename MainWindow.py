
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import ListExpressions, GrapherView
import DlgEditExpr

class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("LittleGrapher")

        self.defaultColorList = [QColor(v) for v in [Qt.blue, Qt.green, Qt.red, Qt.darkYellow, Qt.darkGray, Qt.cyan]]

        self.actionAdd = QAction(self)
        self.actionAdd.setText("Add ...")
        self.actionAdd.setToolTip("Add New Expression ...")
        self.actionAdd.setIcon(QIcon("./images/btn_add.png"))
        self.actionAdd.triggered.connect(self.onAddExpression)

        self.actionDel = QAction(self)
        self.actionDel.setEnabled(False)
        self.actionDel.setText("Delete ...")
        self.actionDel.setToolTip("Delete Selected Expression(s) ...")
        self.actionDel.setIcon(QIcon("./images/btn_del.png"))
        self.actionDel.triggered.connect(self.onDelExpression)

        self.actionEdit = QAction(self)
        self.actionEdit.setEnabled(False)
        self.actionEdit.setText("Edit ...")
        self.actionEdit.setToolTip("Edit Selected Expression ...")
        self.actionEdit.setIcon(QIcon("./images/btn_edit.png"))
        self.actionEdit.triggered.connect(self.onEditExpression)

        self.listExprs = ListExpressions.ListExpressions(self)
        self.listExprs.setIconSize(QSize(16, 14))
        self.listExprs.itemCheckStateChanged.connect(self.onExprCheckStateChanged)
        self.listExprs.itemSelectionChanged.connect(self.onExprListSelectionChanged)

        self.dockExprList = QDockWidget(self)
        self.dockExprList.setWidget(self.listExprs)

        titleBar = QToolBar(self)
        titleBar.setIconSize(QSize(16, 16))
        titleBar.addAction(self.actionAdd)
        titleBar.addAction(self.actionDel)
        titleBar.addAction(self.actionEdit)
        self.dockExprList.setTitleBarWidget(titleBar)

        self.addDockWidget(Qt.RightDockWidgetArea, self.dockExprList)

        self.grapherView = GrapherView.GrapherView(self)
        self.setCentralWidget(self.grapherView)

    def syncListAndGraph(self):
        self.grapherView.clearPlots()
        for row in range(self.listExprs.count()):
            expr, color = self.listExprs.expressionOf(row)
            vaild, checked = self.listExprs.isExpressionValid(row), self.listExprs.isExpressionChecked(row)
            if expr and color and vaild and checked:
                if not self.grapherView.addPlot({"expr": expr, "color": color.name()}):
                    self.listExprs.setExpressionValidity(row, False)
        self.grapherView.updateGraph()

    def findUniqueStrokeColor(self):
        selColor = QColor(Qt.black)
        for color in self.defaultColorList:
            occupied = False
            for row in range(self.listExprs.count()):
                item = self.listExprs.item(row)
                if item.data(ListExpressions.ListExpressions.StrokeColorRole) == color:
                    occupied = True
                    break
            if not occupied:
                selColor = color
                break
        return selColor

    def onAddExpression(self):
        dlg = DlgEditExpr.DlgEditExpr("", self.findUniqueStrokeColor(), "Add New Expression ...", self)
        if dlg.exec_():
            self.listExprs.addExpression(dlg.expression, dlg.strokeColor)
            self.syncListAndGraph()

    def onDelExpression(self):
        selItems = self.listExprs.selectedItems()
        for item in selItems:
            self.listExprs.takeItem(self.listExprs.row(item))
        self.syncListAndGraph()

    def onEditExpression(self):
        index = self.listExprs.currentRow()
        currentExpr, currentColor = self.listExprs.expressionOf(index)
        if not currentColor: currentColor = self.findUniqueStrokeColor()

        dlg = DlgEditExpr.DlgEditExpr(currentExpr, currentColor, "Edit Expression ...", self)
        if dlg.exec_():
            self.listExprs.setExpression(index, dlg.expression, dlg.strokeColor)
            self.syncListAndGraph()

    def onExprCheckStateChanged(self, row, checked):
        self.syncListAndGraph()

    def onExprListSelectionChanged(self):
        selectedCount = len(self.listExprs.selectedItems())
        self.actionDel.setEnabled(selectedCount > 0)
        self.actionEdit.setEnabled(selectedCount == 1)
