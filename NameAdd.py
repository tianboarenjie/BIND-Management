#!/usr/bin/env python3

from PyQt5.QtCore import (Qt, pyqtSignal)
from PyQt5.QtWidgets import (QApplication, QTextEdit, QVBoxLayout, QHBoxLayout, QLabel,
        QLineEdit, QSizePolicy, QGroupBox, QWidget, QGridLayout, QComboBox, QPushButton,
        QMessageBox)
import os
import re
import psutil

class NameAdd(QWidget):
    def __init__(self, parent=None):
        super(NameAdd, self).__init__(parent)

        self.createInfo()
        self.setFixedSize(440, 300)
        self.setLayout(self.mainLayout)

    def createInfo(self):
        #self.func = {"master": "self.masterBox", "slave": "self.slaveBox", "forward": "self.forward"}
        self.mainLayout = QVBoxLayout()
        self.topLayout = QGridLayout()
        domain = QLabel("需要添加的域名：")
        self.domain = QLineEdit("")
        typ = QLabel("选择类型")
        self.typeCombo = QComboBox()
        view = QLabel("选择域")
        self.viewCombo = QComboBox()
        self.typeCombo.addItems(["master","slave","forward"])
        self.typeCombo.activated[str].connect(self.upDetialLayout) 
        self.updateShow()
        self.viewCombo.activated[str].connect(self.changeView)
        ok = QPushButton("添加")
        ok.setFixedWidth(180)
        cancel = QPushButton("取消")
        cancel.setFixedWidth(180)
        ok.clicked.connect(self.addDomain)
        cancel.clicked.connect(self.cancelDomain)
        button = QHBoxLayout()
        button.addWidget(ok)
        button.addWidget(cancel)
        self.topLayout.addWidget(domain, 0, 0)
        self.topLayout.addWidget(self.domain, 0, 1, 1, 128)
        self.topLayout.addWidget(view, 1, 0)
        self.topLayout.addWidget(self.viewCombo, 1, 1, 1, 128)
        self.topLayout.addWidget(typ, 2, 0)
        self.topLayout.addWidget(self.typeCombo, 2, 1, 1, 128)
        self.mainLayout.addLayout(self.topLayout, 0)
        self.createBox()
        self.func = {"master": self.mdetail, "slave": self.sdetail, "forward": self.fdetail}
        self.mainLayout.addWidget(self.masterBox)
        self.mainLayout.addWidget(self.slaveBox)
        self.mainLayout.addWidget(self.forwardBox)
        self.mainLayout.addLayout(button)
        self.slaveBox.setHidden(True)
        self.forwardBox.setHidden(True)
        self.selected = self.typeCombo.itemText(0)
        self.selectedview = self.viewCombo.itemText(0)
        #print(self.selectedview)
        #print(self.selected)
        #print(self.func[self.selected])

    def changeView(self, value):
        self.selectedview = value
        
    def updateShow(self):
        self.view = [i for i in os.listdir("/var/cache/bind/") if os.path.isdir("/var/cache/bind/" + i)]
        self.viewCombo.clear()
        self.viewCombo.addItems(self.view)
    
    def createBox(self):
        self.masterBox = QGroupBox("master")
        self.masterBox.setFixedHeight(150)
        self.master = QVBoxLayout()
        mpre = QLabel("请输入资源记录")
        self.mdetail = QTextEdit("@  IN  NS  ns." + self.domain.text())
        self.mdetail.setFixedHeight(95)
        self.master.addWidget(mpre)
        self.master.addWidget(self.mdetail)
        self.masterBox.setLayout(self.master)
        
        self.slaveBox = QGroupBox("slave")
        self.slaveBox.setFixedHeight(100)
        self.slave = QVBoxLayout()
        spre = QLabel("主DNS服务器IP")
        self.sdetail = QLineEdit()
        self.slave.addWidget(spre, 0, Qt.AlignTop)
        self.slave.addWidget(self.sdetail, 1, Qt.AlignTop)
        self.slaveBox.setLayout(self.slave)
        
        self.forwardBox = QGroupBox("forward")
        self.forwardBox.setFixedHeight(100)
        self.forward = QVBoxLayout()
        fpre = QLabel("转发DNS服务IP")
        self.fdetail = QLineEdit()
        self.forward.addWidget(fpre, 0, Qt.AlignTop)
        self.forward.addWidget(self.fdetail, 1, Qt.AlignTop)
        self.forwardBox.setLayout(self.forward)

    def upDetialLayout(self, value):
        if value == "master":
            self.masterBox.setHidden(False)
            self.slaveBox.setHidden(True)
            self.forwardBox.setHidden(True)
        elif value == "slave":
            self.masterBox.setHidden(True)
            self.slaveBox.setHidden(False)
            self.forwardBox.setHidden(True)
        else:
            self.masterBox.setHidden(True)
            self.slaveBox.setHidden(True)
            self.forwardBox.setHidden(False)
        self.selected = self.typeCombo.currentText()
        #print(self.selected)
    def checkDomain(self):
        name = self.domain.text().split(".")
        domains = ["com", "cn", "jp", "uk", "edu", "tv", "info", "ac", "ag",\
            "am", "at", "be", "biz", "bz", "cc", "es", "eu", "fm", "gs", "hk", \
            "in", "io", "it", "la", "md", "ms", "name", "tw", "us", "co", "uk",\
            "vc", "vg", "vs", "ws", "il", "li", "nz"]
        if len(name) <= 1:
            QMessageBox.about(self, "Error",  self.domain.text() + "不是合格域!!!")
            return False
        
        if self.domain.text().endswith(".in-addr.arpa"):
            return True
        if name[-1] in domains:
            return True
        else:
            QMessageBox.about(self, "Error",  self.domain.text() + "不是合格域!!!")
            return False


    def addDomain(self):
        if not self.checkDomain():
            return
        if QMessageBox.information(self, "确认", "你确定要添加" + self.domain.text() + "域吗？", \
            QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
            return
        fil = "/etc/bind/named.conf." + self.selectedview + "-views"
        if len(psutil.os.popen("awk '/zone.*\"" + self.domain.text() + "\"/' " + fil).read()):
            QMessageBox.about(self, "Error", "域" + self.domain.text() + "已经在" + \
            self.selected + "视图中，不能重复添加！！！")
            return
        if self.selected == "master":
            self.addMaster(fil)
        elif self.selected == "slave":
            if not self.checkNotIP(self.func[self.selected].text()):
                return
            self.addSlave(fil)
        else:
            if self.checkNotIP(self.func[self.selected].text()):
                return
            self.addForward(fil)

    def checkNotIP(self, ip):
            ip = ip.strip()
            ip = ip.split(";")
            ipRed = "(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])"
            result = []
            tmp = False
            for i in ip:
                result.append(re.findall(re.compile(ipRex), i))
            tmp = tmp in result
            #tmp = re.findall(re.compile(ipRex), ip)
            if tmp:
                QMessageBox.about(self, "IP Error","IP格式错误，请重新输入需要查询的IP并确认正确！！！")
                return False
            else:
                return True

    def addMaster(self, fil):
        sep = os.linesep
        name = self.domain.text()
        view = self.selectedview
        fname = "/var/cache/bind/" + view + "-" + name
        psutil.os.popen("sed -i '10a\zone \"" + name + "\" {" + sep + "' " + fil)
        psutil.os.popen("sed -i '11a\ \ttype master;" + sep + "' " + fil)
        psutil.os.popen("sed -i '12a\ \tfile \"" + fname +"\"; };"\
            + sep*2 + "' " + fil)
        #psutil.os.popen("sed -i '11a\ " + add + "'" + fil)
        text = self.func[self.selected].toPlainText()
        #psutil.os.popen("echo '$TTL 86400" + sep + "@   IN  SOA dns." + name + ".   admin." + name + ".(" + sep\
        psutil.os.popen("echo '$TTL 86400" + sep + "@   IN  SOA dns." + name + ".   admin." + name + ".\t ( " + sep\
            + "\t\t01" + sep + "\t\t3H" + sep + "\t\t15M" + sep + "\t\t1W" + sep + "\t\t1D)" + sep*2 + text + "' >" + \
            fname)
        psutil.os.popen("ln -sv " + fname + " /var/cache/bind/" + view + "/" + view + "-" + name)

    def addSlave(self, fil):
        sep = os.linesep
        name = self.domain.text()
        psutil.os.popen("sed -i '10a\zone \"" + name + "\" {" + sep\
            + "\ttype slave;" + sep + "\t\tfile \"/var/cache/bind/" + self.selectedview +\
            + "/slaves." + self.selectedview + "-" + name + "\";" + sep + "\t\tmaster {" + \
            self.func[self.selected].text() + " ;} \b; };" + sep*2 + "' " + fil)
    
    def addForward(self, fil):
        sep = os.linesep
        psutil.os.popen("sed -i '10a\zone \"" + name + "\" {" + sep\
             + "\ttype forward;" + sep + "forwards {" + self.func[self.selected].text() + "\b; };" \
             + sep*2 + "' " + fil)

    def cancelDomain(self):
        self.domain.clear()
        self.func[self.selected].clear()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    name = NameAdd()
    name.show()
    sys.exit(app.exec_())
