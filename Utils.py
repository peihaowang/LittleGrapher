
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# 2018.2.17 Specify the base name and extension of a temporary file
def getTempFileName(templateName):
	fileName = ""
	tempFile = QTemporaryFile(QFileInfo(templateName).baseName())
	if tempFile.open():
	    fileName = tempFile.fileName() + "." + QFileInfo(templateName).completeSuffix()
	    tempFile.close()
	return fileName

def makeColorBlock(color, size, fillStyle = Qt.SolidPattern, frameless = False, borderColor = QColor(Qt.black), borderWidth = 1.0, borderStyle = Qt.SolidLine, roundedBorder = False, roundedRadius = 0.0):
	useHighDpiPixmaps = QCoreApplication.testAttribute(Qt.AA_UseHighDpiPixmaps)

	imageSize = size
	if useHighDpiPixmaps: imageSize *= 2

	image = QPixmap(imageSize)
	if useHighDpiPixmaps: image.setDevicePixelRatio(2.0)
	image.fill(Qt.transparent)

	painter = QPainter(image)
	painter.setRenderHint(QPainter.Antialiasing, True)

	if not frameless: painter.setPen(QPen(QBrush(borderColor), borderWidth, borderStyle))
	else: painter.setPen(QPen(Qt.NoPen))
	painter.setBrush(QBrush(color, fillStyle))

	rect = QRect(0, 0, size.width(), size.height())
	if roundedBorder: painter.drawRoundedRect(rect, roundedRadius, roundedRadius)
	else: painter.drawRect(rect)

	return image
	
class Switch:

	def __init__(self, initVal: bool):
		self.val = initVal

	def __bool__(self):
		return self.val

	def __enter__(self):
		self.val = not self.val

	def __exit__(self, type, value, trace):
		self.val = not self.val
