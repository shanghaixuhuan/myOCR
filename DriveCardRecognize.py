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

class DriveCardRecognize(QDialog):
    def __init__(self):
        super(DriveCardRecognize,self).__init__()
        self.text = ""
        self.strTime = ""
        self.driveid = ""
        self.filePath = ""
        self.initUI()

    def initUI(self):
        self.resize(700,600)
        self.setWindowTitle("myOCR——驾驶证识别")
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
        self.driveid = 'd' + str(time.strftime("%g%m%d")) + str(random.randint(0, 9999)).zfill(4)
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName('./db/myOCR.db')
        db.open()
        query = QSqlQuery()
        sql = "select * from records where RecordId = '%s'"%(self.driveid)
        query.exec_(sql)
        if (query.next()):
            print(QMessageBox.warning(self, "警告", "系统错误，请重新提交", QMessageBox.Yes, QMessageBox.Yes))
            return

        result = aipOcr.drivingLicense(self.get_file_content(self.filePath),options)
        id = result['words_result']['证号']['words']
        deadline = result['words_result']['有效期限']['words']
        type = result['words_result']['准驾车型']['words']
        address = result['words_result']['住址']['words']
        to = result['words_result']['至']['words']
        name = result['words_result']['姓名']['words']
        nation = result['words_result']['国籍']['words']
        birthday = result['words_result']['出生日期']['words']
        sex = result['words_result']['性别']['words']
        first = result['words_result']['初次领证日期']['words']
        self.text = "中华人民共和国机动车驾驶证\n证号：" + id + "\n姓名：" + name \
                    + " 性别：" + sex + " 国籍：" + nation + "\n住址：" + address \
                    + "\n\n出生日期：" + birthday + "\n初次领证日期：" + first \
                    + "\n准驾车型：" + type + "\n有效期限：" + deadline + "至" + to
        sql = "insert into records values('%s','%s','%s','驾驶证识别','%s','')"%(
            self.driveid,self.filePath,self.strTime,self.text)
        query.exec_(sql)
        db.commit()
        db.close()
        print(QMessageBox.information(self, "提醒", "您已成功识别驾驶证!", QMessageBox.Yes, QMessageBox.Yes))
        self.tedit.setPlainText(self.text)

    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    driverecognizeWindow = DriveCardRecognize()
    driverecognizeWindow.show()
    sys.exit(app.exec_())