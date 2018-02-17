
import sys, platform
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 2018.2.17 Enable high dpi pixmaps to show high definition icons for MacOsX
    if platform.system() == "Darwin":
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True);

    w = MainWindow.MainWindow()
    w.resize(800, 640)
    w.show()

    # 2018.2.17 Center main window
    # frameGeometry() can only return the right geometry after the window has shown up
    currentGeometry = w.frameGeometry()
    screenCenter = QDesktopWidget().availableGeometry().center()
    currentGeometry.moveCenter(screenCenter)
    w.move(currentGeometry.topLeft())

    sys.exit(app.exec_())
