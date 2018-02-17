
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import ListExpressions, GrapherView

class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("SimpleGrapher")

        self.dockExpList = ListExpressions.ListExpressions(self)
        self.dockExpList.expressionAdded.connect(self.onExpressionAdded)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockExpList)

        self.grapherView = GrapherView.GrapherView(self)
        self.setCentralWidget(self.grapherView)

    def onExpressionAdded(self, exp, strokeColor):
        self.grapherView.addPlot({"exp": exp, "color": strokeColor.name()})
        self.grapherView.updateGraph()
