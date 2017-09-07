#!/usr/bin/env python3
#
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QListWidget,
        QListWidgetItem, QWidget, QLabel, QPushButton, QMessageBox, QLineEdit, QGroupBox)

from Notepad import *
import os
import psutil
import os.path

class NameMan(QWidget):
    def __init__(self, parent=None):
        super(NameMan, self).__init__(parent)

        self.createTop()
        self.createInfo()
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(self.searchLayout)
        mainLayout.addWidget(self.infoBox)
        self.setFixedSize(440, 260)
        self.setLayout(mainLayout)

    def createTop(self):
        self.searchLayout = QHBoxLayout()
        self.searchLine = QLineEdit()
        search = QPushButton("搜索")
        search.clicked.connect(self.updateInfoList)
        self.searchLayout.addWidget(self.searchLine)
        self.searchLayout.addWidget(search)
    
    def updateShow(self):
        pass
    
    def createInfo(self):
        self.infoBox = QGroupBox("匹配到的域文件")
        self.infoBox.setFixedSize(430, 200)
        self.listWidget = QListWidget()
        layout = QVBoxLayout()
        self.ok = QPushButton("修改")
        self.cancel = QPushButton("删除")
        self.ok.setEnabled(False)
        self.cancel.setEnabled(False)
        self.ok.clicked.connect(self.modifi)
        self.cancel.clicked.connect(self.delete)
        button = QHBoxLayout()
        button.addWidget(self.ok)
        button.addWidget(self.cancel)
        layout.addWidget(self.listWidget)
        layout.addLayout(button)
        self.infoBox.setLayout(layout)

    def updateInfoList(self):
        self.listWidget.clear()
        par = self.searchLine.text()
        if not par:
            QMessageBox.about(self, "Error", "没有检索内容！！！")
            return
        view = [i for i in os.listdir("/var/cache/bind/") if os.path.isdir("/var/cache/bind/" + i)]
        self.result = []
        for i in view:
            lis = os.listdir("/var/cache/bind/" + i)
            ret = ["%s-->%s" % (i,a) for a in lis if par in a]
            self.result.extend(ret)
        if not self.result:
            QMessageBox.about(self, "Warn", "没有你想要检索的内容!!!")
            self.checkButton()
            return
        self.addListItem()
        self.selected = self.listWidget.item(0).text()
        self.listWidget.currentItemChanged.connect(self.getSelected)
        #print(self.selected)
        self.checkButton()

    def checkButton(self):
        if not self.result:
            self.ok.setEnabled(False)
            self.cancel.setEnabled(False)
        else:
            self.ok.setEnabled(True)
            self.cancel.setEnabled(True)

    def addListItem(self):
        lis = self.result
        for i in lis:
            item = QListWidgetItem(self.listWidget)
            item.setText(i)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    
    def getSelected(self, current, previous):
        if not current:
            current = previous
        self.selected = self.listWidget.item(self.listWidget.row(current)).text()
        print(self.selected)

    def modifi(self):
        flag = self.selected.split("-->")
        path = "/var/cache/bind/" + flag[0] + "/" + flag[1]
        self.notepad = Notepad()
        self.notepad.openFile(path)
#        self.notepad.show()

    def delete(self):
        flag = self.selected.split("-->")
        conf = "/etc/bind/named.conf." + flag[0] + "-views"
        path1 = "/var/cache/bind/" + flag[0] + "/" + flag[1]
        path2 = "/var/cache/bind/" + flag[1]
        print(conf)
        psutil.os.popen("rm -f " + path1)
        psutil.os.popen("rm -f " + path2)
        psutil.os.popen('sed -i "/' + self.searchLine.text() + '\"/,/\b;};/d" '  + conf)
        n1 = self.result
        self.updateInfoList()
        n2 = self.result
        if n1 != n2:
            QMessageBox.about(self, "Succree", "删除文件成功!!!")
        else:
            QMessageBox.about(self, "Fail", "发生未知错误导致删除文件失败!!!") 

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    name = NameMan()
    name.show()
    sys.exit(app.exec_())
