#!/usr/bin/env python3
#

from PyQt5.QtCore import (Qt, pyqtSignal, QStringListModel)
from PyQt5.QtWidgets import (QApplication, QGroupBox, QVBoxLayout, QHBoxLayout, QLabel,
        QLineEdit, QSizePolicy, QWidget, QGridLayout, QComboBox)
import psutil

class PartitionView(QWidget):
    def __init__(self, parent=None):
        super(PartitionView, self).__init__(parent)
        
#        self.setFixedSize(450, 330)
        self.createIOBox()
        self.createPartBox()
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addWidget(self.ioGroupBox)
        self.mainLayout.addWidget(self.partGroupBox)
        self.setLayout(self.mainLayout)

    def updateShow(self):
        self.ioGroupBox.deleteLater()
        self.partGroupBox.deleteLater()
        self.createIOBox()
        self.createPartBox()
        self.mainLayout.addWidget(self.ioGroupBox)
        self.mainLayout.addWidget(self.partGroupBox)

    def createIOBox(self):
        self.ioGroupBox = QGroupBox("IO总信息")
        self.ioGroupBox.setFixedHeight(90)
        io = psutil.disk_io_counters()
        self.ioLayout = QGridLayout()
        item = self.addLabel("IO读总个数：", 0, str(io.read_count))
        self.addItem(self.ioLayout, item, 0, 0, 1)
        item = self.addLabel("IO读总比特：", 0, str(io.read_bytes) + "bytes")
        self.addItem(self.ioLayout, item, 0, 2, 3)
        item = self.addLabel("IO写总个数：", 0, str(io.write_count))
        self.addItem(self.ioLayout, item, 1, 0, 1)
        item = self.addLabel("IO写总比特：", 0, str(io.write_bytes) + "bytes")
        self.addItem(self.ioLayout, item, 1, 2 , 3)
        self.ioGroupBox.setLayout(self.ioLayout)
    
    def createPartBox(self):
        self.partGroupBox = QGroupBox("分区信息")
        self.partGroupBox.setFixedHeight(250)
        self.partLayout = QVBoxLayout()
        self.partGridLayout = QGridLayout()
        partLabel = QLabel("选择分区：")
        partCombo = QComboBox()
        self.showPart()
        partCombo.addItems(sorted(self.getPartMount()[1].keys()))
        partCombo.activated[str].connect(self.showPart)

        labelLayout = QHBoxLayout()
        labelLayout.addWidget(partLabel)
        labelLayout.addWidget(partCombo)

        self.partLayout.addLayout(labelLayout)
        self.partLayout.addLayout(self.partGridLayout)
        self.partGroupBox.setLayout(self.partLayout)

    def showPart(self, part="/"):
        dev, fs = self.getPartMount()
        info = psutil.disk_usage(part)
        item = self.addLabel("文件系统类型：", 1, dev[part])
        self.addAloneItem(self.partGridLayout, item, 0, 0, 1)
        item = self.addLabel("系统硬件：", 1, fs[part])
        self.addAloneItem(self.partGridLayout, item, 1, 0, 1)
        item = self.addLabel("分区大小：", 1, str(info.total))
        self.addAloneItem(self.partGridLayout, item, 2, 0, 1)
        item = self.addLabel("分区已使用：", 1, str(info.used))
        self.addAloneItem(self.partGridLayout, item, 3, 0, 1)
        item = self.addLabel("分区剩余：", 1, str(info.free))
        self.addAloneItem(self.partGridLayout, item, 4, 0, 1)
        item = self.addLabel("分区使用占比：", 1, str(info.percent) + " %")
        self.addAloneItem(self.partGridLayout, item, 5, 0, 1)

    def getPartMount(self):
        flag = psutil.disk_partitions()
        tp = {}
        dv = {}
        for i in flag:
            tp[i.mountpoint] = i.fstype
            dv[i.mountpoint] = i.device
        return (tp, dv)
    
    def addItem(self, layout, item, num1, num2, num3):
        layout.addWidget(item[0], num1, num2)
        layout.addWidget(item[1], num1, num3)
    
    def addAloneItem(self, layout, item, num1, num2, num3):
        layout.addWidget(item[0], num1, num2)
        layout.addWidget(item[1], num1, num3, 1, 128)
    
    def addLabel(self, label, num, value):
        if not num:
            itemLine = QLabel()
        else:
            itemLine = QLineEdit()
            itemLine.setReadOnly(True)
        itemLine.setText(value)
#        itemLine.setReadOnly(True)
        itemLine.setAlignment(Qt.AlignCenter)
        itemLine.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))
        itemLabel = QLabel(label)
        itemLabel.setBuddy(itemLine)
        return (itemLabel, itemLine)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    part = PartitionView()
    part.show()
    sys.exit(app.exec_())
