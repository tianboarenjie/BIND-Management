#!/usr/bin/env python3

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGroupBox, QButtonGroup,
        QVBoxLayout, QLabel, QSizePolicy, QWidget, QGridLayout, 
        QLineEdit)
import platform
import psutil
import datetime

class SysView(QWidget):
    def __init__(self, parent=None):
        super(SysView, self).__init__(parent)
        
#        self.resize(500, 250)
#        self.setFixedSize(450, 250)
        self.createSysInfo()        
        mainLayout = QVBoxLayout()
        mainLayout.setAlignment(Qt.AlignTop)
        mainLayout.addWidget(self.sysGroupBox)
        self.setLayout(mainLayout)
    
    def updateShow(self):
        pass

    def createSysInfo(self):
        uname = platform.uname()
        self.sysGroupBox = QGroupBox("电脑信息")
        self.sysGroupBox.setFixedHeight(260)
        self.sysGroupBox.setFixedWidth(435)
        self.sysLayout = QGridLayout()
        uname = platform.uname()
        item = self.addLabel("平台:", platform.platform())
        self.addItem(item, 0)
        item = self.addLabel("操作系统:", uname.system)
        self.addItem(item, 1)
        item = self.addLabel("系统版本:", uname.version)
        self.addItem(item, 2)
        item = self.addLabel("系统位数:", platform.architecture()[0] + "  " + \
            platform.architecture()[1])
        self.addItem(item, 3)
        item = self.addLabel("计算机类型:", uname.machine)
        self.addItem(item, 4)
        item = self.addLabel("主机名:", uname.node)
        self.addItem(item, 5)
        item = self.addLabel("系统开机时间：", \
            datetime.datetime.fromtimestamp(psutil.boot_time()).\
            strftime("%Y-%m-%d %H: %M: %S"))
        self.addItem(item, 6)
        self.sysGroupBox.setLayout(self.sysLayout)

    def addItem(self, item, num):
        self.sysLayout.addWidget(item[0], num, 0)
        self.sysLayout.addWidget(item[1], num, 1, 1, 128)

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
    sysview = SysView()
    sysview.show()
    sys.exit(app.exec_())
