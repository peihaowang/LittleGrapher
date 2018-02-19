
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

    # 2018.2.19 Signals
    statusMesssage = pyqtSignal(str, int)

    def __init__(self, parent):
        super(GrapherView, self).__init__(parent)

        self.plots = []
        self.scaleDivision = 10     # in pixels
        self.pixmapGraph = QPixmap()

    def addPlot(self, plot):
        succ = False
        if isinstance(self.parseEquation(plot["expr"]), Equality):
            self.plots.append(plot)
            succ = True
        return succ

    def clearPlots(self):
        self.plots = []

    def parseEquation(self, expr, varX = None, varY = None):
        if not varX or not varY: varX, varY = symbols("x y")

        parseExpr = lambda expr0: parse_expr(expr0, local_dict = {"x": varX, "y": varY}, transformations = (implicit_multiplication_application,))
        # 2019.2.18 Split equation into left part and right part
        eq = None
        v = expr.split("=")
        if(len(v) == 2):
            try:
                eq = Eq(parseExpr(v[0]), parseExpr(v[1]))
            except Exception as e:
                pass
        return eq

    def plotFigure(self):

        self.sendStatusMessage("Start plotting ...")

        w = self.size().width(); h = self.size().height()
        emptyCanvas = True

        if self.plots:

            self.sendStatusMessage("Construct variables: x, y")

            x, y = symbols("x y")
            varXEnd = (w / 2) / self.scaleDivision; varXBegin = -varXEnd
            varYEnd = (h / 2) / self.scaleDivision; varYBegin = -varYEnd

            def ezplot(expr, color):
                try:
                    plot = plot_implicit(
                        self.parseEquation(expr, x, y)
                        , (x, varXBegin, varXEnd)
                        , (y, varYBegin, varYEnd)
                        , show = False
                        , line_color = color
                    )
                except Exception as e:
                    plot = None

                if not plot:
                    print("Failed to plot expression: ", expr)
                return plot

            p = None
            for i in range(len(self.plots)):
                expr, color = self.plots[i]["expr"], self.plots[i]["color"]
                if expr and color:

                    self.sendStatusMessage("Plotting expression: " + expr)

                    pn = ezplot(expr, color)
                    if pn:
                        if not p: p = pn
                        else: p.extend(pn)
            if p:
                try:

                    self.sendStatusMessage("Start processing series ...")

                    backend = p.backend(p)
                    backend.process_series()

                    self.sendStatusMessage("Finished processing series")

                    path = Utils.getTempFileName("matplot.png")
                    if path:

                        self.sendStatusMessage("Saving figures ...")

                        dpi = 100
                        inchWidth = w / dpi; inchHeight = h / dpi

                        backend.fig.set_figwidth(inchWidth)
                        backend.fig.set_figheight(inchHeight)
                        backend.fig.savefig(path, dpi = dpi)

                        self.sendStatusMessage("Loading figures ...")

                        self.pixmapGraph.load(path)
                        emptyCanvas = False

                        if not QFile.remove(path):
                            print("Failed to remove temp file: %s" % path)
                except Exception as e:
                    print("Unable to plot figures: ", e)
        if emptyCanvas: self.pixmapGraph = QPixmap(w, h); self.pixmapGraph.fill(Qt.white)

        self.sendStatusMessage("Finished plotting", 1000)

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

    def sendStatusMessage(self, message, timeout = -1):
        self.statusMesssage.emit(message, timeout)
