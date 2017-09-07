#!/usr/bin/env python3

from PyQt5.QtCore import (Qt, pyqtSignal)
from PyQt5.QtWidgets import (QApplication, QGridLayout, QGroupBox, QListWidget,
        QVBoxLayout, QHBoxLayout, QListWidgetItem, QWidget, QLabel, QComboBox,
        QPushButton, QMessageBox)
from Notepad import *
import os
import psutil
import os.path

class ViewMan(QWidget):
    def __init__(self, parent=None):
        super(ViewMan, self).__init__(parent)
        
        self.getView()
        delete = self.createDele()
        self.createInfo()
        #button = self.createOperate()
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(delete, 0, Qt.AlignTop)
        mainLayout.addWidget(self.infoBox, 1, Qt.AlignTop)
        self.setLayout(mainLayout)
        

    def createDele(self):
        deleBox = QGroupBox("删除视图")
        deleBox.setFixedSize(440, 60)
        dele = QHBoxLayout()
        dele.addWidget(QLabel("请选择视图："))
        self.delview = QComboBox()
        self.delview.addItems(sorted(self.view))
        self.valueview = self.delview.itemText(0)
#        print(self.valueview)
        self.delview.activated[str].connect(self.getDelView)
        dele.addWidget(self.delview, 0, Qt.AlignCenter)
        self.delete = QPushButton("删除")
        dele.addWidget(self.delete)
        self.delete.clicked.connect(self.delView)
        deleBox.setLayout(dele)
        return deleBox
    
    def getDelView(self, value):
        self.valueview = value
 #       print(self.valueview)

    def delView(self):
        if QMessageBox.information(self, "警告", "你确定要删除吗？", \
            QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
            return
        view = self.valueview
        files = os.listdir("/var/cache/bind/" + view)
        for fil in files:
            os.popen("rm -rvf /var/cache/bind/" + i)
        os.popen("rm -rvf /var/cache/bind/" + view)
        os.popen("sed -i '/.*" + view + "-views/d' " + "/etc/bind/named.conf")
        os.popen("rm -f /etc/bind/*" + view + "-views")
#        print(self.view)
        self.updateShow()

    def updateShow(self):
        self.view = [i for i in os.listdir("/var/cache/bind/") if os.path.isdir("/var/cache/bind/" + i)]
        self.viewCombo.clear()
        self.viewCombo.addItems(self.view)
        self.delview.clear()
        self.delview.addItems(self.view)
        self.info.update()
        self.valueview = self.delview.itemText(0)
        if not self.valueview:
            self.delete.setEnabled(False)

    def createInfo(self):
        self.infoBox = QGroupBox("修改视图内域文件")
        self.infoBox.setFixedSize(440, 195)
        top = QHBoxLayout()
        self.info = QVBoxLayout()
        self.listWidget = QListWidget()
        self.label = QLabel("请选择视图：")
        self.viewCombo = QComboBox()
        self.viewCombo.addItems(self.view)
        self.chanview = self.viewCombo.itemText(0)
        self.viewCombo.activated[str].connect(self.upDirList)
        top.addWidget(self.label)
        top.addWidget(self.viewCombo)
        self.info.addLayout(top)
        self.info.addWidget(self.listWidget)
        self.info.addLayout(self.createOperate())
        self.infoBox.setLayout(self.info) 
        self.getDirList(self.viewCombo.itemText(0))
        self.checkDelete()

    def createOperate(self):
        layout = QHBoxLayout()
        self.change = QPushButton("修改")
        self.delete = QPushButton("删除")
        self.change.clicked.connect(self.viewfileChange)
        self.delete.clicked.connect(self.viewfileDelete)
        layout.addWidget(self.change)
        layout.addWidget(self.delete)
        return layout

    def viewfileChange(self):
        fil = self.selected
        path = "/var/cache/bind/" + self.chanview + "/" + fil
        self.changnotpad = Notepad()
        self.changnotpad.openFile(path)
#        self.changnotpad.show()

    def viewfileDelete(self):
        if QMessageBox.information(self, "警告", "你确定要删除吗？", \
            QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
            return
        fil = self.selected
        name = fil.split("-")
        path = "/var/cache/bind/" + self.chanview + "/" + fil
        psutil.os.popen("rm " + path).read()
        psutil.os.popen("rm -f /var/cache/bind/" + fil)
        psutil.os.popen("sed -i '/zone \"" + name[1] + "\"/,/; };/d' /etc/bind/named.conf." + name[0] + "-views")
        flag = psutil.os.popen("echo $?").read().strip()
        if flag:
            QMessageBox.about(self, "Success", "删除" + path + "文件成功！！！")
        else:
            QMessageBox.about(self, "Failed", "删除" + path + "文件时权限受限!!!")
        self.upDirList(self.chanview)
        
    def checkDelete(self):
        if self.filelist:
            self.selected = self.listWidget.item(0).text()
            self.change.setDisabled(False)
            self.delete.setDisabled(False)
        else:
            self.change.setDisabled(True)
            self.delete.setDisabled(True)

    def getView(self):
        self.view = [i for i in os.listdir("/var/cache/bind/") if os.path.isdir("/var/cache/bind/" + i)]   
    
    def upDirList(self, value):
        self.chanview = value
        self.listWidget.clear()
        self.getDirList(value)
        self.listWidget.update()
        self.checkDelete()

    def getDirList(self, value=""):
        path = "/var/cache/bind/" + value
        self.filelist = os.listdir(path)
       # print(self.filelist)
        self.addListItem(self.filelist)
        #self.checkDelete()
        self.listWidget.currentItemChanged.connect(self.getSelected)

    def getSelected(self, current, previous):
        if not current:
            current = previous
        self.selected = self.listWidget.item(self.listWidget.row(current)).text()
        #print(self.selected)

    def addListItem(self, flist):
        for i in flist:
            item = QListWidgetItem(self.listWidget)
            item.setText(i)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    vman = ViewMan()
    vman.show()
    sys.exit(app.exec_())
