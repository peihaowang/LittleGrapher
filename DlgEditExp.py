
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import ComboBoxColor

class DlgEditExp(QDialog):

    def __init__(self, defExp, defColor, parent):
        super(DlgEditExp, self).__init__(parent)

        self.setWindowTitle("Add New Expression ...")

        self.expression = ""
        self.strokeColor = QColor(Qt.black)

        self.editExp = QLineEdit(self)
        self.editExp.setText(defExp)
        self.editExp.textChanged.connect(self.onExpChanged)

        self.comboStrokeColor = ComboBoxColor.ComboBoxColor(self)
        self.comboStrokeColor.setCurrentColor(defColor)

        self.btnOk = QPushButton("&OK", self)
        self.btnOk.setEnabled(self.editExp.text() != "")
        self.btnOk.clicked.connect(self.accept)

        self.btnCancel = QPushButton("&Cancel", self)
        self.btnCancel.clicked.connect(self.reject)

        layoutForm = QFormLayout()
        layoutForm.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        layoutForm.addRow("&Expression", self.editExp)
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
        self.expression = self.editExp.text()
        self.strokeColor = self.comboStrokeColor.currentColor()
        super(DlgEditExp, self).accept()

    def onExpChanged(self, text):
        self.btnOk.setEnabled(bool(text))
