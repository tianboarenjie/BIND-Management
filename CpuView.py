#!/usr/bin/env python3

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGroupBox, QVBoxLayout, QGridLayout,
        QLabel, QLineEdit, QSizePolicy, QWidget, QLineEdit)
import platform

class CpuView(QWidget):
    def __init__(self, parent=None):
        super(CpuView, self).__init__(parent)

#        self.setFixedSize(450, 330)
        self.createCpuInfo()
        mainLayout = QVBoxLayout()
        mainLayout.setAlignment(Qt.AlignTop)
        mainLayout.addWidget(self.cpuGroupBox)
        self.setLayout(mainLayout)

    def updateShow(self):
        pass
    def createCpuInfo(self):
        self.cpuGroupBox = QGroupBox("CPU信息")
        self.cpuGroupBox.setFixedHeight(350)
        self.cpuLayout = QGridLayout()
        self.getCpuInfo()
        item = self.addLabel("CPU线程数：", self.info["threads"])
        self.addItem(item, 0)
        item = self.addLabel("CPU核心数：", self.info["cores"])
        self.addItem(item, 1)
        item = self.addLabel("CPU供应商：", self.info["vendor"])
        self.addItem(item, 2)
        item = self.addLabel("CPU规格：", self.info["stand"])
        self.addItem(item, 3)
        item = self.addLabel("CPU核心速度：", self.info["cpu"])
        self.addItem(item, 4)
        item = self.addLabel("命令指令集：", self.info["order"])
        self.addItem(item, 5)
        item = self.addLabel("一级数据缓存：", self.info["l1d"])
        self.addItem(item, 6)
        item = self.addLabel("一级指令缓存：", self.info["l1i"])
        self.addItem(item, 7)
        item = self.addLabel("二级缓存：", self.info["l2"])
        self.addItem(item, 8)
        item = self.addLabel("三级缓存：", self.info["l3"])
        self.addItem(item, 9)
        self.cpuGroupBox.setLayout(self.cpuLayout)

    def getCpuInfo(self):
        self.info = {}
        self.info["threads"] = self.getValueByCommand("lscpu | awk -F: '/^CPU\(s\)/{print $2}'")
        self.info["cores"] = self.getValueByCommand("awk -F: '/cpu cores/{print $2}' /proc/cpuinfo | tail -1")
        self.info["order"] = self.getValueByCommand("lscpu | awk -F: '/Byte/{print $2}'")
        self.info["vendor"] = self.getValueByCommand("lscpu | awk -F: '/Vendor/{print $2}'")
        self.info["stand"] = self.getValueByCommand("lscpu | awk -F: '/Model name/{print $2}'")
        self.info["cpu"] = self.getValueByCommand("lscpu | awk -F : '/CPU MHz/{print $2}'") + "  MHz"
        self.info["l1d"] = self.getValueByCommand("lscpu | awk -F: '/L1d/{print $2}'")
        self.info["l1i"] = self.getValueByCommand("lscpu | awk -F: '/L1i/{print $2}'")
        self.info["l2"] = self.getValueByCommand("lscpu | awk -F: '/L2/{print $2}'")
        self.info["l3"] = self.getValueByCommand("lscpu | awk -F: '/L3/{print $2}'")

    def getValueByCommand(self, command):
        value = platform.popen(command).read().strip()
        return value

    def addItem(self, item, num):
        self.cpuLayout.addWidget(item[0], num, 0)
        self.cpuLayout.addWidget(item[1], num, 1, 1, 128)

    def addLabel(self, label, value):
        itemLine = QLineEdit()
        itemLine.setText(value)
        itemLine.setReadOnly(True)
        itemLine.setAlignment(Qt.AlignCenter)
        itemLine.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))
        itemLabel = QLabel(label)
        itemLabel.setBuddy(itemLine)
        return (itemLabel, itemLine)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    cpuview = CpuView()
    cpuview.show()
    sys.exit(app.exec_())
