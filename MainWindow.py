
import sys, os, platform
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# 2018.2.22 Use .qrc resource file
import qt_resource

import Utils
import ListExpressions, GrapherView
import DlgEditExpr

class MainWindow(QMainWindow):

    def __init__(self, parent = None):

        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("LittleGrapher")
        # 20189.2.27 Select window icon for different operating systems
        if platform.system() == "Darwin":
            self.setWindowIcon(QIcon(":/images/ico_app_logo.icns"))
        else:
            self.setWindowIcon(QIcon(":/images/ico_app_logo.ico"))

        self.defaultColorList = [QColor(v) for v in [Qt.blue, Qt.green, Qt.red, Qt.darkYellow, Qt.darkGray, Qt.cyan]]

        self.actionOpen = QAction(self)
        self.actionOpen.setText("Open ...")
        self.actionOpen.setStatusTip("Import expression list(s) and plot figures out")
        self.actionOpen.setShortcut(QKeySequence(QKeySequence.Open))
        self.actionOpen.triggered.connect(self.onOpen)

        self.actionSaveAs = QAction(self)
        self.actionSaveAs.setText("Save As ...")
        self.actionSaveAs.setStatusTip("Export the currently displayed figures as images or expression list")
        self.actionSaveAs.setShortcut(QKeySequence(QKeySequence.Save))
        self.actionSaveAs.triggered.connect(self.onSaveAs)

        self.actionAdd = QAction(self)
        self.actionAdd.setText("Add Expression ...")
        self.actionAdd.setStatusTip("Add new expression")
        self.actionAdd.setToolTip("Add New Expression ...")
        self.actionAdd.setIcon(QIcon(":/images/btn_add.png"))
        self.actionAdd.triggered.connect(self.onAddExpression)

        self.actionDel = QAction(self)
        self.actionDel.setEnabled(False)
        self.actionDel.setText("Delete Expression ...")
        self.actionDel.setStatusTip("Delete selected expression(s)")
        self.actionDel.setToolTip("Delete Selected Expression(s) ...")
        self.actionDel.setIcon(QIcon(":/images/btn_del.png"))
        self.actionDel.triggered.connect(self.onDelExpression)

        self.actionEdit = QAction(self)
        self.actionEdit.setEnabled(False)
        self.actionEdit.setText("Edit Expression ...")
        self.actionEdit.setStatusTip("Edit selected expression")
        self.actionEdit.setToolTip("Edit Selected Expression ...")
        self.actionEdit.setIcon(QIcon(":/images/btn_edit.png"))
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
        self.actionRestore.setStatusTip("Center axes and restore the zoom")
        self.actionRestore.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_0))
        self.actionRestore.triggered.connect(self.grapherView.onRestore)

        self.actionAbout = QAction(self)
        self.actionAbout.setText("About ...")
        self.actionAbout.setStatusTip("About this program")
        self.actionAbout.triggered.connect(self.onAbout)

        # 2018.2.21 Initialize menu bar
        menu = self.menuBar().addMenu("Menu")
        menu.addSection("File")
        menu.addAction(self.actionOpen)
        menu.addAction(self.actionSaveAs)
        menu.addSection("Expression")
        menu.addAction(self.actionAdd)
        menu.addAction(self.actionDel)
        menu.addAction(self.actionEdit)
        menu.addSection("Figure")
        menu.addAction(self.actionZoomIn)
        menu.addAction(self.actionZoomOut)
        menu.addSeparator()
        menu.addAction(self.actionMoveLeft)
        menu.addAction(self.actionMoveRight)
        menu.addAction(self.actionMoveUp)
        menu.addAction(self.actionMoveDown)
        menu.addSeparator()
        menu.addAction(self.actionRestore)
        menu.addSection("About")
        menu.addAction(self.actionAbout)

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

    def onOpen(self):
        files = QFileDialog.getOpenFileNames(
            self
            , "Import expression lists"
            , QDir.homePath()
            , "Expr Lists (*.exli);;Text (*.txt *.li);;All files (*.*)"
        )[0]
        if files:
            for path in files:
                f = open(path, "rb")
                content, text = f.read(), ""
                if len(content) > 3 and content[:3] == b'\xEF\xBB\xBF': text = content[3:].decode("utf-8")
                else: text = content.decode("ascii")
                lines = [s.strip() for s in text.split("\n")]
                for line in lines:
                    pair = line.split("\t")
                    if pair and pair[0]:
                        color = None
                        if len(pair) >= 2 and QColor.isValidColor(pair[1]): color = QColor(pair[1])
                        if not color or not color.isValid(): color = self.findUniqueStrokeColor()
                        self.listExprs.addExpression(pair[0], color)

        self.syncListAndGraph()

    def onSaveAs(self):
        fileName = QFileDialog.getSaveFileName(
            self
            , "Save As ..."
            , QDir.homePath()
            , "Expr Lists (*.exli);;PNG Images (*.png);;JPEG Images (*.jpg *.jpeg);;All files (*.*)"
        )[0]
        if fileName:
            ext = QFileInfo(fileName).suffix().lower()
            if ext in ["exli", "txt"]:
                f = open(fileName, "wb+")
                try:
                    f = open(fileName, 'wb+')
                    # if os.path.getsize(g_xConfig.sFnForwardedDomains) == 0:
                    f.write(b'\xEF\xBB\xBF')
                    for i in range(self.listExprs.count()):
                        expr, color = self.listExprs.expressionOf(i)
                        text = '\t'.join([expr, color.name()]) + os.linesep
                        f.write(text.encode('utf-8'))
                    f.close()
                except IOError as e:
                    QMessageBox.warning(self, "Warning - LittleGrapher", "Failed to export to:\n" + fileName)
            elif ext in ["png", "jpg", "jpeg", "xpm", "bmp"]:
                self.grapherView.exportGraph(fileName)
            else:
                QMessageBox.warning(self, "Warning - LittleGrapher", "Unsupported file format:\n" + fileName)

        self.syncListAndGraph()

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

    def onAbout(self):
        text = """<b style='font-size:20px;'>LittleGrapher</b>
            <br/>Copyright %s Peihao Wang. All rights reserved.
            <br/><br/><a href='https://github.com/peihaowang'>github.com/peihaowang</a>
            <br/><a href='mailto:wangpeihao@gmail.com'>mailto:wangpeihao@gmail.com</a>
            <br/><br/>A lightweight application for plotting figures of mathematical functions and equations, powered by PyQt5 and SymPy.""" \
            % ("2018" if QDate.currentDate().year() == 2018 else ("2018 ~ %1") % (QDate.currentDate().year()))

        QMessageBox.about(self, "About LittleGrapher", text);
