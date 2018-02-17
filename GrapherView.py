
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from sympy.parsing.sympy_parser import parse_expr
from sympy import plot_implicit, symbols, Eq

import Utils

class GrapherView(QWidget):

    def __init__(self, parent):
        super(GrapherView, self).__init__(parent)

        # self.setAutoFillBackgroud(True)

        self.plots = []
        self.scaleDivision = 10     # in pixels
        self.m_xPixmapGraph = QPixmap()

    def addPlot(self, plot):
        self.plots.append(plot)

    def clearPlots(self):
        self.plots = []

    def resizeEvent(self, event):
        self.updateGraph()

    def updateGraph(self):
        w = self.size().width(); h = self.size().height()
        self.m_xPixmapGraph = QPixmap(w, h); self.m_xPixmapGraph.fill(Qt.white)

        failedList = []

        if self.plots:

            x, y = symbols('x y')
            varXEnd = (w / 2) / self.scaleDivision; varXBegin = -varXEnd
            varYEnd = (h / 2) / self.scaleDivision; varYBegin = -varYEnd

            def ezplot(exp, color):
                plot = None
                v = exp.split("=")
                if(len(v) == 2):
                    try:
                        plot = plot_implicit(
                            Eq(parse_expr(v[0]), parse_expr(v[1]))
                            , (x, varXBegin, varXEnd)
                            , (y, varYBegin, varYEnd)
                            , show = False
                            , line_color = color
                        )
                    except:
                        print("Failed to plot expression: ", exp)
                return plot

            # p1 = ezplot(self.plots[0]["exp"], self.plots[0]["color"])
            # if len(self.plots) >= 2:
            #     for i in range(1, len(self.plots)):
            #         pn = ezplot(self.plots[i]["exp"], self.plots[i]["color"])
            #         p1.extend(pn)

            p = None
            for i in range(len(self.plots)):
                pn = ezplot(self.plots[i]["exp"], self.plots[i]["color"])
                if pn:
                    if not p: p = pn
                    else: p.extend(pn)
                else:
                    failedList.append(i)

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

                    self.m_xPixmapGraph.load(path)

                    if not QFile.remove(path):
                        print("Failed to remove temp file: %s" % path)
            except Exception as e:
                print("Unable to plot figures: ", e)

    def paintEvent(self, event):
        if not self.m_xPixmapGraph.isNull():
            painter = QPainter(self)
            painter.drawPixmap(0, 0, self.m_xPixmapGraph)
