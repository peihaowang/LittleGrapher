
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
    plotsChanged = pyqtSignal(int)

    def __init__(self, parent):
        super(GrapherView, self).__init__(parent)

        self.setFocusPolicy(Qt.TabFocus | Qt.ClickFocus)

        self.plots = []
        self.scaleDivisionBase = 10     # in pixels
        self.scaleDiv = lambda: self.scaleDivisionBase * self.currentTransform["scale"]

        self.currentTransform = {"scale": 1.0, "centerX": 0.0, "centerY": 0.0, "offsetX": 0, "offsetY": 0}
        self.lastTransform = self.currentTransform.copy()

        self.updated = Utils.Switch(True)
        self.pixmapGraph = QPixmap()

        self.threadQueue = []

    def addPlot(self, plot):
        succ = False
        if isinstance(self.parseEquation(plot["expr"]), Equality):
            self.plots.append(plot)
            self.plotsChanged.emit(len(self.plots))
            succ = True
        return succ

    def clearPlots(self):
        self.plots = []
        self.plotsChanged.emit(len(self.plots))

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
            centerX, centerY = self.currentTransform["centerX"], self.currentTransform["centerY"]
            varXEnd = (w / 2) / self.scaleDiv() + centerX; varXBegin = (-w / 2) / self.scaleDiv() + centerX
            varYEnd = (h / 2) / self.scaleDiv() + centerY; varYBegin = (-h / 2) / self.scaleDiv() + centerY

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

                    # 2018.2.21 Fix origin point
                    backend.ax.xaxis.set_ticks_position('bottom')
                    backend.ax.spines['bottom'].set_position(('data', 0))
                    backend.ax.yaxis.set_ticks_position('left')
                    backend.ax.spines['left'].set_position(('data', 0))

                    # 2018.2.21 Clear margins around the figure
                    backend.plt.subplots_adjust(left = 0.0, bottom = 0.0, right = 1.0, top = 1.0, wspace = 0.0, hspace = 0.0)
                    # 2018.2.21 Clear labels of axes, because it doesn't display the labels of axes completely after clearing the margins
                    # The solution is to remove the labels of axes and draw it with QPainter manually
                    backend.plt.xlabel("")
                    backend.plt.ylabel("")

                    self.sendStatusMessage("Finished processing series")
                    self.sendStatusMessage("Adjust axes and labels ...")

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

                    # 2018.2.21 It's essential to close figures to release the memory
                    # Or creating too many figures without closing consumes too much memory, which makes matplotlib stop working
                    backend.close()

                except Exception as e:
                    print("Unable to plot figures: ", e)
        if emptyCanvas: self.pixmapGraph = QPixmap(w, h); self.pixmapGraph.fill(Qt.white)

        self.sendStatusMessage("Finished plotting", 1000)

    def updateGraph(self):

        # 2018.2.19 Apply a simple thread queue to avoid repeat and heavy plotting(e.g when drag to resize window)
        def queuePlotting():
            global g_xThreadLock
            isCurrentThread = isinstance(threading.current_thread(), threading._MainThread)
            if not isCurrentThread: g_xThreadLock.acquire()     # Mutex lock

            # 2018.2.21 To record the last transform, record a temporary value before plotting,
            # and then after plotting, assign the temporary value to self.lastTransform
            tempTransform = self.currentTransform.copy()
            with self.updated:
                self.update()
                self.plotFigure()
            self.lastTransform = tempTransform

            # 2018.2.19 Start next thread
            if self.threadQueue: self.threadQueue.pop(0)
            if self.threadQueue:
                # 2018.2.19 Only response to the lastest plotting request
                nextThread = self.threadQueue.pop()
                self.threadQueue = [nextThread]
                nextThread.start()
            else:
                self.update()

            if not isCurrentThread: g_xThreadLock.release()     # Mutex unlock

        thread = threading.Thread(target = queuePlotting)
        thread.setDaemon(True)
        self.threadQueue.append(thread)
        if len(self.threadQueue) == 1: thread.start()

    def resizeEvent(self, event):
        self.updateGraph()
        super(GrapherView, self).resizeEvent(event)

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Equal: self.onZoomIn()
    #     elif event.key() == Qt.Key_Minus: self.onZoomOut()
    #     elif event.key() == Qt.Key_Left: self.onMoveLeft()
    #     elif event.key() == Qt.Key_Right: self.onMoveRight()
    #     elif event.key() == Qt.Key_Up: self.onMoveUp()
    #     elif event.key() == Qt.Key_Down: self.onMoveDown()
    #     else: super(GrapherView, self).keyPressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(QRect(0, 0, self.width(), self.height()), QBrush(Qt.white))
        if not self.pixmapGraph.isNull():
            pixmap = self.pixmapGraph
            if not self.updated:
                scale = self.currentTransform["scale"] / self.lastTransform["scale"]
                pixmap = pixmap.scaled(pixmap.width() * scale, pixmap.height() * scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            offsetX, offsetY = self.currentTransform["offsetX"] - self.lastTransform["offsetX"], self.currentTransform["offsetY"] - self.lastTransform["offsetY"]
            x, y = (self.width() - pixmap.width()) / 2 + offsetX, (self.height() - pixmap.height()) / 2 + offsetY
            painter.drawPixmap(x, y, pixmap)

    def onZoomIn(self):
        self.currentTransform["scale"] *= 1.5
        self.updateGraph()

    def onZoomOut(self):
        self.currentTransform["scale"] /= 1.5
        self.updateGraph()

    def onMoveLeft(self):
        self.currentTransform["centerX"] += 50 / self.scaleDiv()
        self.currentTransform["offsetX"] -= 50
        self.updateGraph()

    def onMoveRight(self):
        self.currentTransform["centerX"] -= 50 / self.scaleDiv()
        self.currentTransform["offsetX"] += 50
        self.updateGraph()

    def onMoveUp(self):
        self.currentTransform["centerY"] -= 50 / self.scaleDiv()
        self.currentTransform["offsetY"] -= 50
        self.updateGraph()

    def onMoveDown(self):
        self.currentTransform["centerY"] += 50 / self.scaleDiv()
        self.currentTransform["offsetY"] += 50
        self.updateGraph()

    def onRestore(self):
        self.currentTransform = {"scale": 1.0, "centerX": 0.0, "centerY": 0.0, "offsetX": 0, "offsetY": 0}
        self.updateGraph()

    def sendStatusMessage(self, message, timeout = -1):
        self.statusMesssage.emit(message, timeout)
