import sys
from PyQt5.QtWidgets import (QDialog,QApplication,QLabel,QVBoxLayout,
                             QHBoxLayout)
import qdarkstyle
from PyQt5.QtGui import QIcon,QFont
from PyQt5.Qt import Qt

class AboutDialog(QDialog):
    def __init__(self):
        super(AboutDialog,self).__init__()
        self.setWindowModality (Qt.WindowModal)
        self.initUI()

    def initUI(self):
        self.resize(600,400)
        self.setWindowTitle("myOCR——关于")
        self.setWindowIcon(QIcon("./images/Icon.png"))
        self.setStyleSheet (qdarkstyle.load_stylesheet_pyqt5 ())

        self.tlabel = QLabel(self)
        self.tlabel.setText("myOCR")
        self.tlabel.setFont (QFont ("Mlungker", 90))
        self.h1box = QHBoxLayout()
        self.h1box.addStretch(1)
        self.h1box.addWidget(self.tlabel)
        self.h1box.addStretch(1)

        self.textlabel = QLabel(self)
        self.textlabel.setText("    本程序为华东理工大学信息与工程学院创新\n"
                               "育人项目 图片文字识别（OCR）系统研究与实现\n"
                               "课程设计。\n\n"
                               "    当前版本：  1 . 0 . 0\n"
                               "    开发工具：  Python3 \n"
                               "    开发库： PyQt5 aip\n"
                               "    开发人员：计162 徐涣 10161762")
        self.textlabel.setFont(QFont("北岸钢笔楷书书法字体",15))
        self.h2box = QHBoxLayout()
        self.h2box.addStretch(1)
        self.h2box.addWidget(self.textlabel)
        self.h2box.addStretch(1)

        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h1box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h2box)
        self.vbox.addStretch(1)
        self.setLayout(self.vbox)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    aboutWindow = AboutDialog()
    aboutWindow.show()
    sys.exit(app.exec_())