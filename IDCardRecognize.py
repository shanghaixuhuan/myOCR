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

class IDCardRecognize(QDialog):
    def __init__(self):
        super(IDCardRecognize,self).__init__()
        self.filePath_f = ""
        self.filePath_b = ""
        self.initUI()

    def initUI(self):
        self.resize(1200,600)
        self.setWindowTitle("myOCR——身份证识别")
        self.setWindowIcon(QIcon("./images/Icon.png"))
        self.plabel_f = QLabel(self)
        self.plabel_f.setFixedSize(350,280)
        self.plabel_b = QLabel(self)
        self.plabel_b.setFixedSize(350,280)
        self.v1box = QVBoxLayout()
        self.v1box.addWidget(self.plabel_f)
        self.v1box.addWidget(self.plabel_b)

        self.fbutton = QPushButton(self)
        self.fbutton.setText("上传身份证正面")
        self.fbutton.setFont(QFont("苏新诗柳楷繁", 15))
        self.fbutton.setFixedSize(180,35)
        self.fbutton.clicked.connect(self.openImage_f)
        self.bbutton = QPushButton(self)
        self.bbutton.setText("上传身份证背面")
        self.bbutton.setFont(QFont("苏新诗柳楷繁", 15))
        self.bbutton.setFixedSize(180,35)
        self.bbutton.clicked.connect(self.openImage_b)
        self.rbutton = QPushButton(self)
        self.rbutton.setText("开始识别")
        self.rbutton.setFont(QFont("苏新诗柳楷繁", 15))
        self.rbutton.setFixedSize(180,35)
        self.rbutton.clicked.connect(self.recognize)
        self.v2box = QVBoxLayout()
        self.v2box.addWidget(self.fbutton)
        self.v2box.addWidget(self.bbutton)
        self.v2box.addWidget(self.rbutton)

        self.tlabel = QLabel(self)
        self.tlabel.setText("识别结果")
        self.tlabel.setFont(QFont("苏新诗柳楷繁", 15))
        self.tedit = QPlainTextEdit(self)
        self.tedit.setFont(QFont("宋体",10))
        self.tedit.setFixedSize(400,400)
        self.v3box = QVBoxLayout()
        self.v3box.addStretch(1)
        self.v3box.addWidget(self.tlabel)
        self.v3box.addStretch(1)
        self.v3box.addWidget(self.tedit)
        self.v3box.addStretch(1)

        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.v1box)
        self.hbox.addLayout(self.v2box)
        self.hbox.addLayout(self.v3box)
        self.setLayout(self.hbox)

    def openImage_f(self):
        self.filePath_f, imgType = QFileDialog.getOpenFileName(self, "打开本地图片", "", "*.jpg;;*.png;;All Files(*)")
        self.jpg_f = QtGui.QPixmap(self.filePath_f).scaled(self.plabel_f.width(), self.plabel_f.height())
        self.plabel_f.setPixmap(self.jpg_f)

    def openImage_b(self):
        self.filePath_b, imgType = QFileDialog.getOpenFileName(self, "打开本地图片", "", "*.jpg;;*.png;;All Files(*)")
        self.jpg_b = QtGui.QPixmap(self.filePath_b).scaled(self.plabel_b.width(), self.plabel_b.height())
        self.plabel_b.setPixmap(self.jpg_b)

    def recognize(self):
        if(self.filePath_f == "" or self.filePath_b == ""):
            print(QMessageBox.warning(self, "警告", "请将身份证正反面上传", QMessageBox.Yes, QMessageBox.Yes))
            return
        now = int(time.time())
        timeStruct = time.localtime(now)
        self.strTime = time.strftime("%Y/%m/%d %H:%M", timeStruct)
        self.cardid = 'i' + str(time.strftime("%g%m%d")) + str(random.randint(0, 9999)).zfill(4)
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName('./db/myOCR.db')
        db.open()
        query = QSqlQuery()
        sql = "select * from records where RecordId = '%s'" % (self.cardid)
        query.exec_(sql)
        if (query.next()):
            print(QMessageBox.warning(self, "警告", "系统错误，请重新提交", QMessageBox.Yes, QMessageBox.Yes))
            return
        result = aipOcr.idcard(self.get_file_content(self.filePath_f),"front",options)
        address = result['words_result']['住址']['words']
        birthday = result['words_result']['出生']['words']
        year_i = birthday[0:4]
        month_i = birthday[4:6]
        day_i = birthday[6:8]
        name = result['words_result']['姓名']['words']
        id = result['words_result']['公民身份号码']['words']
        sex = result['words_result']['性别']['words']
        nation =result['words_result']['民族']['words']
        result = aipOcr.idcard(self.get_file_content(self.filePath_b), "back", options)
        date_q = result['words_result']['签发日期']['words']
        date_q_y = date_q[0:4]
        date_q_m = date_q[4:6]
        date_q_d = date_q[6:8]
        office = result['words_result']['签发机关']['words']
        date_s = result['words_result']['失效日期']['words']
        date_s_y = date_s[0:4]
        date_s_m = date_s[4:6]
        date_s_d = date_s[6:8]
        self.text = "姓名：" + name + "\n性别：" + sex + "  民族：" + nation \
                    + "\n出生：" + year_i + "年" + month_i + "月" + day_i + "日\n住址：" \
                    + address + "\n公民身份号码：" + id + "\n\n签发日期：" + date_q_y \
                    + "年" + date_q_m + "月" + date_q_d + "日\n签发机关：" + office \
                    + "\n失效日期：" + date_s_y + "年" + date_s_m + "月" + date_s_d + "日"
        sql = "insert into records values('%s','%s','%s','身份证识别','%s','%s')" % (
            self.cardid, self.filePath_f, self.strTime, self.text,self.filePath_b)
        query.exec_(sql)
        db.commit()
        db.close()
        print(QMessageBox.information(self, "提醒", "您已成功识别身份证!", QMessageBox.Yes, QMessageBox.Yes))
        self.tedit.setPlainText(self.text)

    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    idcardrecognizeWindow = IDCardRecognize()
    idcardrecognizeWindow.show()
    sys.exit(app.exec_())