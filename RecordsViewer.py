import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QComboBox, QLabel, QMessageBox,
                             QTableView, QAbstractItemView, QDialog)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel
import qdarkstyle
from RecordDetail import RecordDetailDialog
from RecordDetail_id import RecordDetailDialog_id


class RecordsViewer(QDialog):
    def __init__(self):
        super(RecordsViewer, self).__init__()
        self.resize(800, 500)
        self.setWindowTitle('myOCR——我的识别历史')
        self.setWindowIcon(QIcon('./images/icon.png'))
        self.queryModel = None
        self.tableView = None
        self.currentPage = 0
        self.totalPage = 0
        self.totalRecord = 0
        self.pageRecord = 10
        self.initUI()

    def initUI(self):
        self.vbox = QVBoxLayout()
        self.h1box = QHBoxLayout()
        self.h2box = QHBoxLayout()

        self.searchEdit = QLineEdit()
        self.searchEdit.setFixedHeight(32)
        self.searchEdit.setFont(QFont("苏新诗柳楷繁", 15))

        self.searchButton = QPushButton("查询")
        self.searchButton.setFixedHeight(32)
        self.searchButton.setFont(QFont("苏新诗柳楷繁", 15))

        self.condisionComboBox = QComboBox()
        searchCondision = ['按识别编号查询', '按识别时间查询', '按识别类型查询',
                           '按识别文字查询']
        self.condisionComboBox.setFixedHeight(32)
        self.condisionComboBox.setFont(QFont("苏新诗柳楷繁", 15))
        self.condisionComboBox.addItems(searchCondision)

        self.h1box.addWidget(self.searchEdit)
        self.h1box.addWidget(self.condisionComboBox)
        self.h1box.addWidget(self.searchButton)

        self.jumpToLabel = QLabel(self)
        self.jumpToLabel.setText("跳转到第")
        self.jumpToLabel.setFont(QFont("苏新诗柳楷繁", 12))
        self.jumpToLabel.setFixedWidth(90)
        self.pageEdit = QLineEdit()
        self.pageEdit.setFixedWidth(30)
        self.pageEdit.setFont(QFont("苏新诗柳楷繁", 12))
        s = "/" + str(self.totalPage) + "页"
        self.pageLabel = QLabel(s)
        self.pageLabel.setFont(QFont("苏新诗柳楷繁", 12))
        self.pageLabel.setFixedWidth(40)
        self.jumpToButton = QPushButton(self)
        self.jumpToButton.setText("跳转")
        self.jumpToButton.setFont(QFont("苏新诗柳楷繁", 12))
        self.jumpToButton.setFixedHeight(30)
        self.jumpToButton.setFixedWidth(60)
        self.prevButton = QPushButton("前一页")
        self.prevButton.setFont(QFont("苏新诗柳楷繁", 12))
        self.prevButton.setFixedHeight(30)
        self.prevButton.setFixedWidth(80)
        self.backButton = QPushButton("后一页")
        self.backButton.setFont(QFont("苏新诗柳楷繁", 12))
        self.backButton.setFixedHeight(30)
        self.backButton.setFixedWidth(80)

        self.detailbutton = QPushButton(self)
        self.detailbutton.setText("详细信息")
        self.detailbutton.setFixedWidth(90)
        self.detailbutton.setFont(QFont("苏新诗柳楷繁", 12))
        self.detailbutton.clicked.connect(self.detailInfo)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.jumpToLabel)
        self.hbox.addWidget(self.pageEdit)
        self.hbox.addWidget(self.pageLabel)
        self.hbox.addWidget(self.jumpToButton)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.detailbutton)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.prevButton)
        self.hbox.addWidget(self.backButton)
        widget = QWidget()
        widget.setLayout(self.hbox)
        widget.setFixedWidth(600)
        self.h2box.addWidget(widget)

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('./db/myOCR.db')
        self.db.open()
        self.tableView = QTableView()
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setFont(QFont("苏新诗柳楷繁", 12))
        self.tableView.horizontalHeader().setFont(QFont("苏新诗柳楷繁", 12))
        self.queryModel = QSqlQueryModel()
        self.searchButtonClicked()
        self.tableView.setModel(self.queryModel)

        self.queryModel.setHeaderData(0, Qt.Horizontal, "识别编号")
        self.queryModel.setHeaderData(1, Qt.Horizontal, "识别时间")
        self.queryModel.setHeaderData(2, Qt.Horizontal, "识别类型")
        self.queryModel.setHeaderData(3, Qt.Horizontal, "识别文字")

        self.vbox.addLayout(self.h1box)
        self.vbox.addWidget(self.tableView)
        self.vbox.addLayout(self.h2box)
        self.setLayout(self.vbox)
        self.searchButton.clicked.connect(self.searchButtonClicked)
        self.prevButton.clicked.connect(self.prevButtonClicked)
        self.backButton.clicked.connect(self.backButtonClicked)
        self.jumpToButton.clicked.connect(self.jumpToButtonClicked)
        self.searchEdit.returnPressed.connect(self.searchButtonClicked)

    def setButtonStatus(self):
        if (self.currentPage == self.totalPage):
            self.prevButton.setEnabled(True)
            self.backButton.setEnabled(False)
        if (self.currentPage == 1):
            self.backButton.setEnabled(True)
            self.prevButton.setEnabled(False)
        if (self.currentPage < self.totalPage and self.currentPage > 1):
            self.prevButton.setEnabled(True)
            self.backButton.setEnabled(True)

    def getTotalRecordCount(self):
        self.queryModel.setQuery("select RecordId,RecordTime,RecordType,RecordText from records")
        self.totalRecord = self.queryModel.rowCount()
        return

    def getPageCount(self):
        self.getTotalRecordCount()
        self.totalPage = int((self.totalRecord + self.pageRecord - 1) / self.pageRecord)
        return

    def recordQuery(self, index):
        conditionChoice = self.condisionComboBox.currentText()
        if (conditionChoice == "按识别编号查询"):
            conditionChoice = 'RecordId'
        elif (conditionChoice == "按识别时间查询"):
            conditionChoice = 'RecordTime'
        elif (conditionChoice == "按识别类型查询"):
            conditionChoice = 'RecordType'
        else:
            conditionChoice = 'RecordText'


        if (self.searchEdit.text() == ""):
            queryCondition = "select RecordId,RecordTime,RecordType,RecordText from records order by RecordTime DESC"
            self.queryModel.setQuery(queryCondition)
            self.totalRecord = self.queryModel.rowCount()
            self.totalPage = int((self.totalRecord + self.pageRecord - 1) / self.pageRecord)
            label = "/" + str(int(self.totalPage)) + "页"
            self.pageLabel.setText(label)
            queryCondition = ("select RecordId,RecordTime,RecordType,RecordText from records order by %s desc limit %d,%d " % (
            conditionChoice, index, self.pageRecord))
            self.queryModel.setQuery(queryCondition)
            self.setButtonStatus()
            return

        temp = self.searchEdit.text()
        s = '%'
        for i in range(0, len(temp)):
            s = s + temp[i] + "%"
        queryCondition = ("select RecordId,RecordTime,RecordType,RecordText from records where %s like '%s' order by %s desc" % (
            conditionChoice, s, conditionChoice))
        self.queryModel.setQuery(queryCondition)
        self.totalRecord = self.queryModel.rowCount()
        if (self.totalRecord == 0):
            print(QMessageBox.information(self, "提醒", "查询无记录", QMessageBox.Yes, QMessageBox.Yes))
            queryCondition = "select RecordId,RecordTime,RecordType,RecordText from records order by RecordTime DESC"
            self.queryModel.setQuery(queryCondition)
            self.totalRecord = self.queryModel.rowCount()
            self.totalPage = int((self.totalRecord + self.pageRecord - 1) / self.pageRecord)
            label = "/" + str(int(self.totalPage)) + "页"
            self.pageLabel.setText(label)
            queryCondition = ("select RecordId,RecordTime,RecordType,RecordText from records order by %s desc limit %d,%d " % (
            conditionChoice, index, self.pageRecord))
            self.queryModel.setQuery(queryCondition)
            self.setButtonStatus()
            return
        self.totalPage = int((self.totalRecord + self.pageRecord - 1) / self.pageRecord)
        label = "/" + str(int(self.totalPage)) + "页"
        self.pageLabel.setText(label)
        queryCondition = ("select RecordId,RecordTime,RecordType,RecordText from records where %s like '%s' order by %s desc limit %d,%d " % (
            conditionChoice, s, conditionChoice, index, self.pageRecord))
        self.queryModel.setQuery(queryCondition)
        self.setButtonStatus()
        return

    def searchButtonClicked(self):
        self.currentPage = 1
        self.pageEdit.setText(str(self.currentPage))
        self.getPageCount()
        s = "/" + str(int(self.totalPage)) + "页"
        self.pageLabel.setText(s)
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)
        return

    def prevButtonClicked(self):
        self.currentPage -= 1
        if (self.currentPage <= 1):
            self.currentPage = 1
        self.pageEdit.setText(str(self.currentPage))
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)
        return

    def backButtonClicked(self):
        self.currentPage += 1
        if (self.currentPage >= int(self.totalPage)):
            self.currentPage = int(self.totalPage)
        self.pageEdit.setText(str(self.currentPage))
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)
        return

    def jumpToButtonClicked(self):
        if (self.pageEdit.text().isdigit()):
            self.currentPage = int(self.pageEdit.text())
            if (self.currentPage > self.totalPage):
                self.currentPage = self.totalPage
            if (self.currentPage <= 1):
                self.currentPage = 1
        else:
            self.currentPage = 1
        index = (self.currentPage - 1) * self.pageRecord
        self.pageEdit.setText(str(self.currentPage))
        self.recordQuery(index)
        return

    def detailInfo(self):
        index_ = self.tableView.currentIndex().row()
        if (index_ == -1):
            print(QMessageBox.warning(self, "警告", "您没有选中任何记录", QMessageBox.Yes, QMessageBox.Yes))
            return
        else:
            str = self.queryModel.data(self.queryModel.index(index_, 0))
            type = self.queryModel.data(self.queryModel.index(index_, 2))
            if(type == '身份证识别'):
                self.recordDetail_id(str)
            else:
                self.recordDetail(str)

    def recordDetail(self, RecordId):
        recorddetaildialog = RecordDetailDialog(RecordId)
        recorddetaildialog.show()
        recorddetaildialog.exec_()

    def recordDetail_id(self,RecordId):
        recorddetail_id = RecordDetailDialog_id(RecordId)
        recorddetail_id.show()
        recorddetail_id.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    recordsWindow = RecordsViewer()
    recordsWindow.show()
    sys.exit(app.exec_())