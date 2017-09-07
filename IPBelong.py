#!/usr/bin/env python3
#

from PyQt5.QtCore import (Qt, pyqtSignal)
from PyQt5.QtWidgets import (QApplication, QGroupBox, QLineEdit, QLabel, 
        QGridLayout, QHBoxLayout, QVBoxLayout, QSizePolicy, QWidget, QPushButton,
        QMessageBox)
import re
import urllib
import urllib.request
import json

class IPBelong(QWidget):
    def __init__(self, parent=None):
        super(IPBelong, self).__init__(parent)
        
#        self.setFixedSize(440, 280)
        self.createBox()
        mainLayout = QVBoxLayout()
        mainLayout.setAlignment(Qt.AlignTop)
        mainLayout.addLayout(self.ipHLayout)
        mainLayout.addWidget(self.ipGroupBox)
        self.setLayout(mainLayout)

    def updateShow(self):
        pass
    def createBox(self):
        self.ipGroupBox = QGroupBox("IP归属地信息")
        self.ipGroupBox.setFixedHeight(200)
        self.ipLayout = QGridLayout()
        self.ipEdit = LineEdit()
        self.ipEdit.setText("202.101.224.69")
        self.ipEdit.setAlignment(Qt.AlignCenter)
        self.ipEdit.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))
        self.searchButton = QPushButton("查询")
        self.searchButton.clicked.connect(self.checkIP)
        self.ipHLayout = QHBoxLayout()
        self.ipHLayout.addWidget(self.ipEdit)
        self.ipHLayout.addWidget(self.searchButton)
        self.ipLayout.addWidget(self.addLabel("所属国家："), 1, 0)
        self.country = QLineEdit()
        self.country.setReadOnly(True)
        self.ipLayout.addWidget(self.country, 1, 1, 1, 28)
        self.ipLayout.addWidget(self.addLabel("所属地区:"), 2, 0)
        self.area = QLineEdit()
        self.area.setReadOnly(True)
        self.ipLayout.addWidget(self.area, 2, 1, 1, 28)
        self.ipLayout.addWidget(self.addLabel("所属省:"), 3, 0)
        self.region = QLineEdit()
        self.region.setReadOnly(True)
        self.ipLayout.addWidget(self.region, 3, 1, 1, 28)
        self.ipLayout.addWidget(self.addLabel("所属市："), 4, 0)
        self.city = QLineEdit()
        self.city.setReadOnly(True)
        self.ipLayout.addWidget(self.city, 4, 1, 1, 28)
        self.ipLayout.addWidget(self.addLabel("运营商："), 5, 0)
        self.isp = QLineEdit()
        self.isp.setReadOnly(True)
        self.ipLayout.addWidget(self.isp, 5, 1, 1, 28)
        self.ipGroupBox.setLayout(self.ipLayout)

    def addLabel(self, value):
        label = QLabel(value)
        label.setAlignment(Qt.AlignCenter)
        label.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))
        return label

    def checkIP(self):
        ip = self.ipEdit.text()
#        ipRex = '((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))'
        ipRex = "(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])"
        tmp = re.findall(re.compile(ipRex), ip)
        if not tmp:
            QMessageBox.about(self, "IP Error","IP格式错误，请重新输入需要查询的IP并确认正确！！！")
        else:
            self.getInfo(ip)

    def getInfo(self, ip):
        reponseData = self.searchIP(ip)
        if isinstance(reponseData, bytes) or isinstance(reponseData, bool):
            QMessageBox.about(self, "Network Error", "当前网络有问题，请检查网络后再查询！！！")
        else:
            data = json.loads(reponseData)
            if data['code'] == 0:
                self.showInfo(data['data'])
            else:
                QMessageBox.about(self, "Other Error", "找不到相关信息！！！")

    def searchIP(self, ip):
        url = "http://ip.taobao.com/service/getIpInfo.php?ip="
        headers = ('User-Agent','Mozilla/5.0 (Windows NT 5.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
#        data = opener.open(url+ip).read()
        try:
            data = opener.open(url+ip).read()
            data = data.decode('UTF-8')
        except (UnicodeDecodeError, urllib.error.URLError):
            return True
        return data
    
    def showInfo(self, info):
        self.country.setText(info["country"])
        self.area.setText(info["area"])
        self.region.setText(info["region"])
        self.city.setText(info["city"])
        self.isp.setText(info["isp"])

class LineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)

#    def mouseDoubleClickEvent(self, e):
#        self.clear()
    def focusInEvent(self, e):
        self.clear()
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ip = IPBelong()
    ip.show()
    sys.exit(app.exec_())

