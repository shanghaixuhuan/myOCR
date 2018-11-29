import sys
from PyQt5.QtWidgets import QApplication,QDesktopWidget,QMainWindow
from PyQt5.QtGui import QIcon
from HomePageWidget import HomePageWidget
import qdarkstyle


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(800, 600)
        self.setWindowTitle("myOCR——免费的OCR文字识别系统")
        self.setWindowIcon(QIcon('./images/icon.png'))
        self.center()

        self.widget = HomePageWidget()
        self.setCentralWidget(self.widget)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
