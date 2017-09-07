#!/usr/bin/env python3
#

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGroupBox, QGridLayout, QVBoxLayout, QHBoxLayout,
        QLabel, QLineEdit, QSizePolicy, QWidget, QFrame)
import psutil

class NetView(QWidget):
    def __init__(self, parent=None):
        super(NetView, self).__init__(parent)

#        self.setFixedSize(455, 280)
        self.createAllBox()
        self.createAloneBox()
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addWidget(self.netAllGroupBox)
        self.mainLayout.addWidget(self.netAloneGroupBox)
        self.setLayout(self.mainLayout)

    def updateShow(self):
        self.netAllGroupBox.deleteLater()
        self.netAloneGroupBox.deleteLater()
        self.createAllBox()
        self.createAloneBox()
        self.mainLayout.addWidget(self.netAllGroupBox)
        self.mainLayout.addWidget(self.netAloneGroupBox)

    def createAllBox(self):
        self.netAllGroupBox = QGroupBox("网络信息")
        self.netAllGroupBox.setFixedHeight(80)
        self.netAllLayout = QGridLayout()
        info = psutil.net_io_counters()
        item = self.addLabel("发送字节数：", str(info.bytes_sent) + "bytes")
        self.addItem(item, 0, 0, 1)
        item = self.addLabel("发送数据包：", str(info.packets_sent))
        self.addItem(item, 0, 2, 3)
        item = self.addLabel("发送出错包：", str(info.errout))
        self.addItem(item, 0, 4, 5)
        item = self.addLabel("接受字节数：", str(info.bytes_recv) + "bytes")
        self.addItem(item, 1, 0, 1)
        item = self.addLabel("接受数据包：", str(info.packets_recv))
        self.addItem(item, 1, 2, 3)
        item = self.addLabel("接收出错包：", str(info.errin))
        self.addItem(item, 1, 4, 5)
        self.netAllGroupBox.setLayout(self.netAllLayout)

    def createAloneBox(self):
        self.netAloneGroupBox = QGroupBox("网卡信息")
        self.netAloneLayout = QGridLayout()
        netper = psutil.net_io_counters(pernic=True)
        nline = 1
        self.netAloneLayout.addWidget(self.addNetLabel(""), 0, 0)
        self.netAloneLayout.addWidget(self.addNetLabel("发送字节数"), 1, 0)
        self.netAloneLayout.addWidget(self.addNetLabel("发送数据包"), 2, 0)
        self.netAloneLayout.addWidget(self.addNetLabel("发送出错包"), 3, 0)
        self.netAloneLayout.addWidget(self.addNetLabel("接收字节数"), 4, 0)
        self.netAloneLayout.addWidget(self.addNetLabel("接收数据包"), 5, 0)
        self.netAloneLayout.addWidget(self.addNetLabel("接收出错包"), 6, 0)
        for i in sorted(netper):
            self.insertItem(i, netper[i], nline)
            nline += 1
        self.netAloneGroupBox.setLayout(self.netAloneLayout)

    def insertItem(self, net, netinfo, num):
        self.netAloneLayout.addWidget(self.addNetLabel(net), 0, num)
        self.netAloneLayout.addWidget(self.addLine(str(netinfo.bytes_sent) + "byes"), 1, num)
        self.netAloneLayout.addWidget(self.addLine(str(netinfo.packets_sent)), 2, num)
        self.netAloneLayout.addWidget(self.addLine(str(netinfo.errout)), 3, num)
        self.netAloneLayout.addWidget(self.addLine(str(netinfo.bytes_recv) + "bytes"), 4, num)
        self.netAloneLayout.addWidget(self.addLine(str(netinfo.packets_recv)), 5, num)
        self.netAloneLayout.addWidget(self.addLine(str(netinfo.errin)), 6, num)
    
    def addLine(self, value):
        line = QLabel()
        line.setText(value)
        line.setAlignment(Qt.AlignCenter)
        line.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))
        line.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        return line

    def addItem(self, item, num1, num2, num3):
        self.netAllLayout.addWidget(item[0], num1, num2)
        self.netAllLayout.addWidget(item[1], num1, num3)
         

    def addNetLabel(self, value):
        label = QLabel(value)
        label.setAlignment(Qt.AlignCenter)
        return label

    def addLabel(self, label, value):
        itemLine = QLabel()
        itemLine.setText(value)
        itemLine.setAlignment(Qt.AlignCenter)
        itemLine.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))
        itemLine.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        itemLabel = QLabel(label)
        itemLabel.setBuddy(itemLine)
        return (itemLabel, itemLine)
        

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    net = NetView()
    net.show()
    sys.exit(app.exec_())

