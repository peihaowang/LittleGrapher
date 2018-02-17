
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import Utils

g_vColorList = []

g_vColorList.append(("Black", QColor(0, 0, 0)))
g_vColorList.append(("Brown", QColor(153, 52, 0)))
g_vColorList.append(("Olive", QColor(51, 51, 0)))
g_vColorList.append(("Dark Green", QColor(0, 51, 0)))
g_vColorList.append(("Deep Grayish Blue", QColor(0, 51, 102)))
g_vColorList.append(("Dark Blue", QColor(0, 0, 128)))
g_vColorList.append(("Indigo", QColor(51, 51, 153)))
g_vColorList.append(("Dark Gray", QColor(51, 51, 51)))

g_vColorList.append(("Dark Red", QColor(128, 0, 0)))
g_vColorList.append(("Orange Red", QColor(255, 102, 0)))
g_vColorList.append(("Dark Yellow", QColor(128, 128, 0x00)))
g_vColorList.append(("Green", QColor(0, 128, 0)))
g_vColorList.append(("Cyan", QColor(0, 128, 128)))
g_vColorList.append(("Blue", QColor(0, 0, 255)))
g_vColorList.append(("Blue Ash", QColor(102, 102, 153)))
g_vColorList.append(("Gray", QColor(128, 128, 128)))

g_vColorList.append(("Red", QColor(255, 0, 0)))
g_vColorList.append(("Orange", QColor(255, 153, 0)))
g_vColorList.append(("Lime", QColor(153, 204, 0)))
g_vColorList.append(("Sea Green", QColor(51, 153, 102)))
g_vColorList.append(("Sapphire", QColor(51, 204, 204)))
g_vColorList.append(("Light Blue", QColor(51, 102, 255)))
g_vColorList.append(("Purple", QColor(128, 0, 128)))
g_vColorList.append(("Light Gray", QColor(153, 153, 153)))

g_vColorList.append(("Fuchsia", QColor(255, 0, 255)))
g_vColorList.append(("Gold", QColor(255, 204, 0)))
g_vColorList.append(("Yellow", QColor(255, 255, 0)))
g_vColorList.append(("Bright Green", QColor(0, 255, 0)))
g_vColorList.append(("Aqua", QColor(0, 255, 255)))
g_vColorList.append(("Sky Blue", QColor(0, 204, 255)))
g_vColorList.append(("Plum", QColor(153, 51, 102)))
g_vColorList.append(("Silver", QColor(192, 192, 192)))

g_vColorList.append(("Pink", QColor(255, 153, 204)))
g_vColorList.append(("Light Brown", QColor(255, 204, 153)))
g_vColorList.append(("Light Yellow", QColor(255, 255, 153)))
g_vColorList.append(("Light Green", QColor(204, 255, 204)))
g_vColorList.append(("Light Aqua", QColor(204, 255, 255)))
g_vColorList.append(("Pale Blue", QColor(153, 204, 255)))
g_vColorList.append(("Pale Purple", QColor(204, 153, 255)))
g_vColorList.append(("White", QColor(255, 255, 255)))

class ComboBoxColor(QComboBox):

    def __init__(self, parent):
        super(ComboBoxColor, self).__init__(parent)

        self.setIconSize(QSize(16, 12))

        # 2018.2.17 Add default colors
        global g_vColorList
        for pair in g_vColorList:
            self.addColor(-1, pair[0], pair[1])
        self.addItem("More colors ...")
        self.setCurrentIndex(0)
        self.setMaxVisibleItems(32)
        self.currentIndexChanged.connect(self.onCurrentIndexChanged)

        self.canPickMoreColor = True
        self.indexLastItem = self.currentIndex()


    def currentColor(self):
        return self.itemData(self.currentIndex())

    def setCurrentColor(self, color):
        found = False
        for i in range(self.count()):
            itemColor = self.itemData(i)
            if itemColor.isValid() and itemColor == color:
                self.setCurrentIndex(i)
                found = True
                break
        if not found:
            self.addColor(self.count() - 1, color.name, color)
            self.setCurrentIndex(self.count() - 2)

    def addColor(self, pos, name, color):
        # 2018.2.17 Use frameless color icons, because the frame effect rendered on high-dpi screen is too bad
        framlessIcon = QCoreApplication.testAttribute(Qt.AA_UseHighDpiPixmaps)
        icon = QIcon(Utils.makeColorBlock(color, self.iconSize(), Qt.SolidPattern, framlessIcon))
        if pos < 0:
            self.addItem(icon, name, color)
        else:
            self.insertItem(pos, icon, name, color)

    def onCurrentIndexChanged(self, index):
        if index == self.count() - 1:
            dlgColor = QColorDialog(self.itemData(self.indexLastItem), QApplication.activeWindow())
            dlgColor.setWindowTitle("Pick a color ...")
            if(dlgColor.exec_() == QColorDialog.Accepted):
                selColor = dlgColor.selectedColor()

                self.canPickMoreColor = False
                self.addColor(self.count() - 1, selColor.name(), selColor)
                self.setCurrentIndex(self.count() - 2)
                self.canPickMoreColor = True
            else:
            	self.setCurrentIndex(self.indexLastItem)
        else:
            self.indexLastItem = self.currentIndex()
