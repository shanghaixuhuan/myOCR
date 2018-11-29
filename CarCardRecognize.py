import sys
import time
import random
from aip import AipOcr
from PyQt5.QtWidgets import (QDialog,QApplication,QLabel,QPushButton,
                             QFileDialog,QMessageBox,QPlainTextEdit,QHBoxLayout,
                             QVBoxLayout)
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtSql import QSqlQuery,QSqlDatabase
import qdarkstyle
from PyQt5 import QtGui

APP_ID = '14868017'
API_KEY = '6epPHS8EPX1k8GjdCzez7OLT'
SECRET_KEY = 'onZaVAlgYzEBchooR91xQf8j7kgoFG4W'
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
options = {
            'detect_direction': 'true',
            'language_type': 'CHN_ENG',
        }

class CarCardRecognize(QDialog):
    def __init__(self):
        super(CarCardRecognize,self).__init__()
        self.text = ""
        self.strTime = ""
        self.carid = ""
        self.filePath = ""
        self.initUI()

    def initUI(self):
        self.resize(700,600)
        self.setWindowTitle("myOCR——行驶证识别")
        self.setWindowIcon(QIcon("./images/Icon.png"))

        self.plabel = QLabel(self)
        self.plabel.setFixedSize(400,300)

        self.obtn = QPushButton(self)
        self.obtn.setText("打开本地图片")
        self.obtn.setFont(QFont("苏新诗柳楷繁", 15))
        self.obtn.clicked.connect(self.openimage)
        self.obtn.setFixedSize(180,40)
        self.sbtn = QPushButton(self)
        self.sbtn.setText("开 始 识 别")
        self.sbtn.setFont(QFont("苏新诗柳楷繁", 15))
        self.sbtn.clicked.connect(self.recognize)
        self.sbtn.setFixedSize(180,40)

        self.v1box = QVBoxLayout()
        self.v1box.addWidget(self.obtn)
        self.v1box.addWidget(self.sbtn)

        self.h1box = QHBoxLayout()
        self.h1box.addWidget(self.plabel)
        self.h1box.addLayout(self.v1box)

        self.tlabel = QLabel(self)
        self.tlabel.setText("识\n别\n结\n果")
        self.tlabel.setFont(QFont("苏新诗柳楷繁", 15))
        self.tlabel.resize(200, 50)

        self.tedit = QPlainTextEdit(self)
        self.tedit.setFont(QFont("宋体",10))
        self.tedit.setFixedSize(600,350)

        self.h2box = QHBoxLayout()
        self.h2box.addStretch(1)
        self.h2box.addWidget(self.tlabel)
        self.h2box.addStretch(1)
        self.h2box.addWidget(self.tedit)
        self.h2box.addStretch(1)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.h1box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h2box)
        self.setLayout(self.vbox)


    def openimage(self):
        self.filePath, imgType = QFileDialog.getOpenFileName(self, "打开本地图片", "", "*.jpg;;*.png;;All Files(*)")
        self.jpg = QtGui.QPixmap(self.filePath).scaled(self.plabel.width(), self.plabel.height())
        self.plabel.setPixmap(self.jpg)

    def recognize(self):
        if(self.filePath == ""):
            print(QMessageBox.warning(self, "警告", "请插入图片", QMessageBox.Yes, QMessageBox.Yes))
            return
        now = int(time.time())
        timeStruct = time.localtime(now)
        self.strTime = time.strftime("%Y/%m/%d %H:%M", timeStruct)
        self.carid = 'c' + str(time.strftime("%g%m%d")) + str(random.randint(0, 9999)).zfill(4)
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName('./db/myOCR.db')
        db.open()
        query = QSqlQuery()
        sql = "select * from records where RecordId = '%s'"%(self.carid)
        query.exec_(sql)
        if (query.next()):
            print(QMessageBox.warning(self, "警告", "系统错误，请重新提交", QMessageBox.Yes, QMessageBox.Yes))
            return
        result = aipOcr.vehicleLicense(self.get_file_content(self.filePath),options)
        type = result['words_result']['品牌型号']['words']
        date = result['words_result']['发证日期']['words']
        property = result['words_result']['使用性质']['words']
        id = result['words_result']['发动机号码']['words']
        carid = result['words_result']['号牌号码']['words']
        person = result['words_result']['所有人']['words']
        address = result['words_result']['住址']['words']
        setup = result['words_result']['注册日期']['words']
        reco = result['words_result']['车辆识别代号']['words']
        car_type = result['words_result']['车辆类型']['words']
        self.text = "中华人民共和国机动车行驶证\n号牌号码：" + carid + " 车辆类型：" \
                    + car_type + "\n所有人：" + person + "\n住址：" + address + "\n\n使用性质：" \
                    + property + " 品牌型号：" + type + "\n车辆识别代码：" + reco + "\n发动机号码：" \
                    + id + "\n注册日期：" + setup + " 发证日期：" + date
        sql = "insert into records values('%s','%s','%s','行驶证识别','%s','')"%(
            self.carid,self.filePath,self.strTime,self.text)
        query.exec_(sql)
        db.commit()
        db.close()
        print(QMessageBox.information(self, "提醒", "您已成功识别行驶证!", QMessageBox.Yes, QMessageBox.Yes))
        self.tedit.setPlainText(self.text)

    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    carrecognizeWindow = CarCardRecognize()
    carrecognizeWindow.show()
    sys.exit(app.exec_())