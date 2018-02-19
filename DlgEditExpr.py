
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import ComboBoxColor

class DlgEditExpr(QDialog):

    def __init__(self, defExpr, defColor, title, parent):
        super(DlgEditExpr, self).__init__(parent)

        self.setWindowTitle(title)

        self.expression = ""
        self.strokeColor = QColor(Qt.black)

        self.editExpr = QLineEdit(self)
        self.editExpr.setText(defExpr)
        self.editExpr.textChanged.connect(self.onExprChanged)

        self.comboStrokeColor = ComboBoxColor.ComboBoxColor(self)
        self.comboStrokeColor.setCurrentColor(defColor)

        self.btnOk = QPushButton("&OK", self)
        self.btnOk.setEnabled(self.editExpr.text() != "")
        self.btnOk.clicked.connect(self.accept)

        self.btnCancel = QPushButton("&Cancel", self)
        self.btnCancel.clicked.connect(self.reject)

        layoutForm = QFormLayout()
        layoutForm.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        layoutForm.addRow("&Expression", self.editExpr)
        layoutForm.addRow("&Stroke Color", self.comboStrokeColor)

        layoutButtons = QHBoxLayout()
        layoutButtons.addStretch()
        layoutButtons.addWidget(self.btnOk)
        layoutButtons.addWidget(self.btnCancel)

        layoutMain = QVBoxLayout()
        layoutMain.addLayout(layoutForm)
        layoutMain.addLayout(layoutButtons)

        self.setLayout(layoutMain)

    def accept(self):
        self.expression = self.editExpr.text()
        self.strokeColor = self.comboStrokeColor.currentColor()
        super(DlgEditExpr, self).accept()

    def onExprChanged(self, text):
        self.btnOk.setEnabled(bool(text))
