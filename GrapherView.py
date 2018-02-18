
import sys, threading
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from sympy.core.relational import Equality
from sympy.parsing.sympy_parser import parse_expr, implicit_multiplication_application
from sympy import plot_implicit, symbols, Eq

import Utils

g_xThreadLock = threading.RLock()

class GrapherView(QWidget):

    def __init__(self, parent):
        super(GrapherView, self).__init__(parent)

        self.plots = []
        self.scaleDivision = 10     # in pixels
        self.pixmapGraph = QPixmap()

    def addPlot(self, plot):
        succ = False
        if isinstance(self.parseEquation(plot["exp"]), Equality):
            self.plots.append(plot)
            succ = True
        else:
            self.plots.append({"exp": "", "color": ""})
        return succ

    def setPlot(self, index, plot):
        succ = False
        if isinstance(self.parseEquation(plot["exp"]), Equality):
            self.plots[index] = plot
            succ = True
        else:
            self.plots[index] = {"exp": "", "color": ""}
        return succ

    def delPlot(self, index):
        del self.plots[index]

    def clearPlots(self):
        self.plots = []

    def parseEquation(self, exp, varX = None, varY = None):
        if not varX or not varY: varX, varY = symbols("x y")

        parseExpr = lambda exp0: parse_expr(exp0, local_dict = {"x": varX, "y": varY}, transformations = (implicit_multiplication_application,))
        # 2019.2.18 Split equation into left part and right part
        eq = None
        v = exp.split("=")
        if(len(v) == 2):
            try:
                eq = Eq(parseExpr(v[0]), parseExpr(v[1]))
            except Exception as e:
                pass
        return eq

    def plotFigure(self):
        w = self.size().width(); h = self.size().height()
        emptyCanvas = True

        if self.plots:

            x, y = symbols("x y")
            varXEnd = (w / 2) / self.scaleDivision; varXBegin = -varXEnd
            varYEnd = (h / 2) / self.scaleDivision; varYBegin = -varYEnd

            def ezplot(exp, color):
                try:
                    plot = plot_implicit(
                        self.parseEquation(exp, x, y)
                        , (x, varXBegin, varXEnd)
                        , (y, varYBegin, varYEnd)
                        , show = False
                        , line_color = color
                    )
                except Exception as e:
                    plot = None

                if not plot:
                    print("Failed to plot expression: ", exp)
                return plot

            p = None
            for i in range(len(self.plots)):
                exp, color = self.plots[i]["exp"], self.plots[i]["color"]
                if exp and color:
                    pn = ezplot(exp, color)
                    if pn:
                        if not p: p = pn
                        else: p.extend(pn)

            if p:
                try:
                    backend = p.backend(p)
                    backend.process_series()

                    path = Utils.getTempFileName("matplot.png")
                    if path:
                        dpi = 100
                        inchWidth = w / dpi; inchHeight = h / dpi

                        backend.fig.set_figwidth(inchWidth)
                        backend.fig.set_figheight(inchHeight)
                        backend.fig.savefig(path, dpi = dpi)

                        self.pixmapGraph.load(path)
                        emptyCanvas = False

                        if not QFile.remove(path):
                            print("Failed to remove temp file: %s" % path)
                except Exception as e:
                    print("Unable to plot figures: ", e)
                    
        if emptyCanvas: self.pixmapGraph = QPixmap(w, h); self.pixmapGraph.fill(Qt.white)

    def updateGraph(self):
        def queuePlotting():
            global g_xThreadLock
            isCurrentThread = isinstance(threading.current_thread(), threading._MainThread)
            if not isCurrentThread: g_xThreadLock.acquire()
            self.plotFigure()
            self.update()
            if not isCurrentThread: g_xThreadLock.release()

        thread = threading.Thread(target = queuePlotting)
        thread.setDaemon(True)
        thread.start()

    def resizeEvent(self, event):
        self.updateGraph()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(QRect(0, 0, self.width(), self.height()), QBrush(Qt.white))
        if not self.pixmapGraph.isNull():
            pixmap = self.pixmapGraph.scaled(QSize(self.width(), self.height()), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            x, y = (self.width() - pixmap.width()) / 2, (self.height() - pixmap.height()) / 2
            painter.drawPixmap(x, y, pixmap)
