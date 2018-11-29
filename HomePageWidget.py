import sys
from PyQt5.QtWidgets import (QPushButton,QLabel,QWidget,QApplication,
                             QHBoxLayout,QVBoxLayout)
from PyQt5.QtGui import QPixmap,QIcon,QFont
from PyQt5.QtCore import QCoreApplication
from AboutDialog import AboutDialog
from BasicRecognize import BasicRecognize
from RecordsViewer import RecordsViewer
from IDCardRecognize import IDCardRecognize
from BankCardRecognize import BankCardRecognize
from DriveCardRecognize import DriveCardRecognize
from CarCardRecognize import CarCardRecognize
from PlateRecognize import PlateRecognize
import qdarkstyle

class HomePageWidget(QWidget):
    def __init__(self):
        super(HomePageWidget,self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(800,600)
        self.setWindowIcon(QIcon('./images/icon.png'))
        self.setWindowTitle('myOCR——启动界面')

        self.titleLabel = QLabel(self)
        pixmap = QPixmap('./images/title.png')
        self.titleLabel.setPixmap(pixmap)
        self.h1box = QHBoxLayout()
        self.h1box.addStretch(1)
        self.h1box.addWidget(self.titleLabel)
        self.h1box.addStretch(1)

        self.basicbtn = QPushButton(self)
        self.basicbtn.setText("普通文字识别")
        self.basicbtn.setFont(QFont("苏新诗柳楷繁", 15))
        self.basicbtn.setFixedSize(180,45)
        self.basicbtn.clicked.connect(self.basicrecognizedialog)
        self.idcardbtn = QPushButton(self)
        self.idcardbtn.setText("身份证识别")
        self.idcardbtn.setFont(QFont("苏新诗柳楷繁", 15))
        self.idcardbtn.setFixedSize(180, 45)
        self.idcardbtn.clicked.connect(self.idcardrecognizedialog)
        self.bankcardbtn = QPushButton(self)
        self.bankcardbtn.setText("银行卡识别")
        self.bankcardbtn.setFont(QFont("苏新诗柳楷繁", 15))
        self.bankcardbtn.setFixedSize(180, 45)
        self.bankcardbtn.clicked.connect(self.bankcardrecognizedialog)
        self.h2box = QHBoxLayout()
        self.h2box.addStretch(1)
        self.h2box.addWidget(self.basicbtn)
        self.h2box.addStretch(1)
        self.h2box.addWidget(self.idcardbtn)
        self.h2box.addStretch(1)
        self.h2box.addWidget(self.bankcardbtn)
        self.h2box.addStretch(1)

        self.drivecardbtn = QPushButton(self)
        self.drivecardbtn.setText("驾驶证识别")
        self.drivecardbtn.setFont(QFont("苏新诗柳楷繁", 15))
        self.drivecardbtn.setFixedSize(180, 45)
        self.drivecardbtn.clicked.connect(self.drivecardrecognizedialog)
        self.carcardbtn = QPushButton(self)
        self.carcardbtn.setText("行驶证识别")
        self.carcardbtn.setFont(QFont("苏新诗柳楷繁", 15))
        self.carcardbtn.setFixedSize(180, 45)
        self.carcardbtn.clicked.connect(self.carcardrecognizedialog)
        self.platecardbtn = QPushButton(self)
        self.platecardbtn.setText("车牌识别")
        self.platecardbtn.setFont(QFont("苏新诗柳楷繁", 15))
        self.platecardbtn.setFixedSize(180, 45)
        self.platecardbtn.clicked.connect(self.platecardrecognize)
        self.h3box = QHBoxLayout()
        self.h3box.addStretch(1)
        self.h3box.addWidget(self.drivecardbtn)
        self.h3box.addStretch(1)
        self.h3box.addWidget(self.carcardbtn)
        self.h3box.addStretch(1)
        self.h3box.addWidget(self.platecardbtn)
        self.h3box.addStretch(1)

        self.hbtn = QPushButton(self)
        self.hbtn.setText("我的识别历史")
        self.hbtn.setFont(QFont("苏新诗柳楷繁", 15))
        self.hbtn.clicked.connect(self.myhistorydialog)
        self.hbtn.setFixedSize(160, 40)
        self.abtn = QPushButton(self)
        self.abtn.setText("关    于")
        self.abtn.setFont(QFont("苏新诗柳楷繁", 15))
        self.abtn.clicked.connect(self.aboutdialog)
        self.abtn.setFixedSize(160,40)
        self.qbtn = QPushButton(self)
        self.qbtn.setText("退    出")
        self.qbtn.setFont(QFont("苏新诗柳楷繁", 15))
        self.qbtn.clicked.connect(QCoreApplication.instance().quit)
        self.qbtn.setFixedSize(160, 40)
        self.hbbox = QHBoxLayout()
        self.hbbox.addStretch(1)
        self.hbbox.addWidget(self.hbtn)
        self.hbbox.addStretch(1)
        self.hbbox.addWidget(self.abtn)
        self.hbbox.addStretch(1)
        self.hbbox.addWidget(self.qbtn)
        self.hbbox.addStretch(1)

        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h1box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h2box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h3box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbbox)
        self.vbox.addStretch(1)
        self.setLayout(self.vbox)

    def aboutdialog(self):
        aboutdialogWindow = AboutDialog()
        aboutdialogWindow.show()
        aboutdialogWindow.exec_()

    def basicrecognizedialog(self):
        basicrecognize = BasicRecognize()
        basicrecognize.show()
        basicrecognize.exec_()

    def myhistorydialog(self):
        recordsviewer = RecordsViewer()
        recordsviewer.show()
        recordsviewer.exec_()

    def idcardrecognizedialog(self):
        idcardrecognize = IDCardRecognize()
        idcardrecognize.show()
        idcardrecognize.exec_()

    def bankcardrecognizedialog(self):
        bankcardrecognize = BankCardRecognize()
        bankcardrecognize.show()
        bankcardrecognize.exec_()

    def drivecardrecognizedialog(self):
        drivecardrecognize = DriveCardRecognize()
        drivecardrecognize.show()
        drivecardrecognize.exec_()

    def carcardrecognizedialog(self):
        carcardrecognize = CarCardRecognize()
        carcardrecognize.show()
        carcardrecognize.exec_()

    def platecardrecognize(self):
        platecardrecognize = PlateRecognize()
        platecardrecognize.show()
        platecardrecognize.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    HomePageWidget = HomePageWidget()
    HomePageWidget.show()
    sys.exit(app.exec_())