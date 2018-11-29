import sys
import qdarkstyle
from PyQt5.QtWidgets import (QDialog,QApplication,QHBoxLayout,QLabel,
                             QVBoxLayout,QPlainTextEdit)
from PyQt5.QtGui import QIcon,QPixmap,QFont
from PyQt5.QtSql import QSqlDatabase,QSqlQuery


class RecordDetailDialog_id(QDialog):
    def __init__(self,RecordId):
        super(RecordDetailDialog_id,self).__init__()
        self.str = RecordId
        self.resize(900,600)
        self.setWindowTitle("myOCR——识别详情")
        self.setWindowIcon(QIcon('./images/icon.png'))
        self.initUI()

    def initUI(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('./db/myOCR.db')
        self.db.open()
        self.query = QSqlQuery()
        sql = "select * from records where RecordId = '%s'" %(self.str)
        self.query.exec_(sql)
        self.query.next()
        id = self.query.value(0)
        path = self.query.value(1)
        time = self.query.value(2)
        type = self.query.value(3)
        text = self.query.value(4)
        path_1 = self.query.value(5)

        self.labeltitle = QLabel(self)
        self.imagetitle = QPixmap()
        self.imagetitle.load(path)
        self.labeltitle.setFixedSize(400,300)
        self.labeltitle.setPixmap(self.imagetitle.scaled(self.labeltitle.width(), self.labeltitle.height()))

        self.labeltitle_1 = QLabel(self)
        self.imagetitle_1 = QPixmap()
        self.imagetitle_1.load(path_1)
        self.labeltitle_1.setFixedSize(400,300)
        self.labeltitle_1.setPixmap(self.imagetitle_1.scaled(self.labeltitle_1.width(), self.labeltitle_1.height()))

        self.idlabel = QLabel()
        self.idlabel.setText('识别编号：')
        self.idlabel.setFont(QFont("苏新诗柳楷繁", 13))
        self.idlabel_ = QLabel()
        self.idlabel_.setFont(QFont("苏新诗柳楷繁", 13))
        self.idlabel_.setText(id)
        self.h2box = QHBoxLayout()
        self.h2box.addStretch(1)
        self.h2box.addWidget(self.idlabel)
        self.h2box.addWidget(self.idlabel_)
        self.h2box.addStretch(1)

        self.typelabel = QLabel()
        self.typelabel.setText('识别类型：')
        self.typelabel.setFont(QFont("苏新诗柳楷繁", 13))
        self.typelabel_ = QLabel()
        self.typelabel_.setFont(QFont("苏新诗柳楷繁", 13))
        self.typelabel_.setText(type)
        self.h3box = QHBoxLayout()
        self.h3box.addStretch(1)
        self.h3box.addWidget(self.typelabel)
        self.h3box.addWidget(self.typelabel_)
        self.h3box.addStretch(1)

        self.timelabel = QLabel()
        self.timelabel.setText('识别时间：')
        self.timelabel.setFont(QFont("苏新诗柳楷繁", 13))
        self.timelabel_ = QLabel()
        self.timelabel_.setFont(QFont("苏新诗柳楷繁", 13))
        self.timelabel_.setText(time)
        self.h4box = QHBoxLayout()
        self.h4box.addStretch(1)
        self.h4box.addWidget(self.timelabel)
        self.h4box.addWidget(self.timelabel_)
        self.h4box.addStretch(1)

        self.text = QPlainTextEdit(self)
        self.text.setFixedSize(400,400)
        self.text.setFont(QFont("苏新诗柳楷繁", 12))
        self.text.setPlainText(text)
        self.h5box = QHBoxLayout()
        self.h5box.addWidget(self.text)

        self.v1box = QVBoxLayout()
        self.v1box.addWidget(self.labeltitle)
        self.v1box.addWidget(self.labeltitle_1)

        self.v2box = QVBoxLayout()
        self.v2box.addStretch(1)
        self.v2box.addLayout(self.h2box)
        self.v2box.addStretch(1)
        self.v2box.addLayout(self.h3box)
        self.v2box.addStretch(1)
        self.v2box.addLayout(self.h4box)
        self.v2box.addStretch(1)
        self.v2box.addLayout(self.h5box)
        self.v2box.addStretch(1)
        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addLayout(self.v1box)
        self.hbox.addStretch(1)
        self.hbox.addLayout(self.v2box)
        self.hbox.addStretch(1)
        self.setLayout(self.hbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    recorddetailDialog_id = RecordDetailDialog_id("i1811276394")
    recorddetailDialog_id.show()
    recorddetailDialog_id.exec_()
