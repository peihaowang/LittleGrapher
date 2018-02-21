
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
        self.actionAdd.setText("Add Expression ...")
        self.actionAdd.setStatusTip("Add new expression")
        self.actionAdd.setToolTip("Add New Expression ...")
        self.actionAdd.setIcon(QIcon("./images/btn_add.png"))
        self.actionAdd.triggered.connect(self.onAddExpression)

        self.actionDel = QAction(self)
        self.actionDel.setEnabled(False)
        self.actionDel.setText("Delete Expression ...")
        self.actionDel.setStatusTip("Delete selected expression(s)")
        self.actionDel.setToolTip("Delete Selected Expression(s) ...")
        self.actionDel.setIcon(QIcon("./images/btn_del.png"))
        self.actionDel.triggered.connect(self.onDelExpression)

        self.actionEdit = QAction(self)
        self.actionEdit.setEnabled(False)
        self.actionEdit.setText("Edit Expression ...")
        self.actionEdit.setStatusTip("Edit selected expression")
        self.actionEdit.setToolTip("Edit Selected Expression ...")
        self.actionEdit.setIcon(QIcon("./images/btn_edit.png"))
        self.actionEdit.triggered.connect(self.onEditExpression)

        self.dockExprList = QDockWidget(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockExprList)

        self.listExprs = ListExpressions.ListExpressions(self)
        self.listExprs.setIconSize(QSize(16, 14))
        self.listExprs.itemCheckStateChanged.connect(self.onExprCheckStateChanged)
        self.listExprs.itemSelectionChanged.connect(self.onExprListSelectionChanged)
        self.dockExprList.setWidget(self.listExprs)

        titleBar = QToolBar(self)
        titleBar.setIconSize(QSize(16, 16))
        titleBar.addAction(self.actionAdd)
        titleBar.addAction(self.actionDel)
        titleBar.addAction(self.actionEdit)
        self.dockExprList.setTitleBarWidget(titleBar)

        self.grapherView = GrapherView.GrapherView(self)
        self.grapherView.plotsChanged.connect(self.onPlotsChanged)
        self.setCentralWidget(self.grapherView)

        self.actionZoomIn = QAction(self)
        self.actionZoomIn.setEnabled(False)
        self.actionZoomIn.setText("Zoom In")
        self.actionZoomIn.setStatusTip("Zoom in the currently displayed figures")
        self.actionZoomIn.setShortcut(QKeySequence(Qt.Key_Equal))
        self.actionZoomIn.triggered.connect(self.grapherView.onZoomIn)

        self.actionZoomOut = QAction(self)
        self.actionZoomOut.setEnabled(False)
        self.actionZoomOut.setText("Zoom Out")
        self.actionZoomOut.setStatusTip("Zoom out the currently displayed figures")
        self.actionZoomOut.setShortcut(QKeySequence(Qt.Key_Minus))
        self.actionZoomOut.triggered.connect(self.grapherView.onZoomOut)

        self.actionMoveLeft = QAction(self)
        self.actionMoveLeft.setEnabled(False)
        self.actionMoveLeft.setText("Shift Left")
        self.actionMoveLeft.setStatusTip("Shift the currently displayed figures left")
        self.actionMoveLeft.setShortcut(QKeySequence(Qt.Key_Left))
        self.actionMoveLeft.triggered.connect(self.grapherView.onMoveLeft)

        self.actionMoveRight = QAction(self)
        self.actionMoveRight.setEnabled(False)
        self.actionMoveRight.setText("Shift Right")
        self.actionMoveRight.setStatusTip("Shift the currently displayed figures right")
        self.actionMoveRight.setShortcut(QKeySequence(Qt.Key_Right))
        self.actionMoveRight.triggered.connect(self.grapherView.onMoveRight)

        self.actionMoveUp = QAction(self)
        self.actionMoveUp.setEnabled(False)
        self.actionMoveUp.setText("Shift Up")
        self.actionMoveUp.setStatusTip("Shift the currently displayed figures up")
        self.actionMoveUp.setShortcut(QKeySequence(Qt.Key_Up))
        self.actionMoveUp.triggered.connect(self.grapherView.onMoveUp)

        self.actionMoveDown = QAction(self)
        self.actionMoveDown.setEnabled(False)
        self.actionMoveDown.setText("Shift Down")
        self.actionMoveDown.setStatusTip("Shift the currently displayed figures down")
        self.actionMoveDown.setShortcut(QKeySequence(Qt.Key_Down))
        self.actionMoveDown.triggered.connect(self.grapherView.onMoveDown)

        self.actionRestore = QAction(self)
        self.actionRestore.setEnabled(False)
        self.actionRestore.setText("Center and Restore")
        self.actionRestore.setStatusTip("Center the axes and restore the zoom")
        self.actionRestore.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_0))
        self.actionRestore.triggered.connect(self.grapherView.onRestore)

        # 2018.2.21 Initialize menu bar
        menu = self.menuBar().addMenu("Menu")
        menu.addSection("Expressions")
        menu.addAction(self.actionAdd)
        menu.addAction(self.actionDel)
        menu.addAction(self.actionEdit)
        menu.addSection("Figures")
        menu.addAction(self.actionZoomIn)
        menu.addAction(self.actionZoomOut)
        menu.addSeparator()
        menu.addAction(self.actionMoveLeft)
        menu.addAction(self.actionMoveRight)
        menu.addAction(self.actionMoveUp)
        menu.addAction(self.actionMoveDown)
        menu.addSeparator()
        menu.addAction(self.actionRestore)

        # 2018.2.19 Initialize status bar
        statusBar = self.statusBar()
        statusBar.setSizeGripEnabled(True)
        statusBar.setVisible(True)
        textDefaultStatus = QLabel("Ready", self)
        statusBar.addWidget(textDefaultStatus)
        self.grapherView.statusMesssage.connect(statusBar.showMessage)

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

    def onPlotsChanged(self, count):
        enabled = (count > 0)
        self.actionZoomIn.setEnabled(enabled)
        self.actionZoomOut.setEnabled(enabled)
        self.actionMoveLeft.setEnabled(enabled)
        self.actionMoveRight.setEnabled(enabled)
        self.actionMoveUp.setEnabled(enabled)
        self.actionMoveDown.setEnabled(enabled)
        self.actionRestore.setEnabled(enabled)
