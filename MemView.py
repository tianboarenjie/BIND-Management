#!/usr/bin/env python3

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGroupBox, QVBoxLayout, 
        QLabel, QLineEdit, QSizePolicy, QWidget, QGridLayout, 
        QListWidget)
import psutil

class MemView(QWidget):
    def __init__(self, parent=None):
        super(MemView, self).__init__(parent)
        
        self.createVirt()
        self.createSwap()
#        self.setFixedSize(450, 400)
        group = QListWidget()
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.virtGroupBox)
        self.mainLayout.addWidget(self.swapGroupBox)
        self.setLayout(self.mainLayout)

    def updateShow(self):
        self.virtGroupBox.deleteLater()
        self.swapGroupBox.deleteLater()
        self.createVirt()
        self.createSwap()
        self.mainLayout.addWidget(self.virtGroupBox)
        self.mainLayout.addWidget(self.swapGroupBox)

    
    def createVirt(self):
        mem = psutil.virtual_memory()
        self.virtGroupBox = QGroupBox("内存信息")
        self.virtLayout = QGridLayout()
        item = self.addLabel("内存总数：", str(mem.total))
        self.addVirtItem(item, 0)
        item = self.addLabel("已使用内存数：", str(mem.total - mem.available))
        self.addVirtItem(item, 1)
        item = self.addLabel("空闲内存数：", str(mem.available))
        self.addVirtItem(item, 2)
        item = self.addLabel("已使用的内存占比：", str(mem.percent) + " %")
        self.addVirtItem(item, 3)
        item = self.addLabel("缓冲使用数：", str(mem.buffers))
        self.addVirtItem(item, 4)
        item = self.addLabel("缓存使用数：", str(mem.cached))
        self.addVirtItem(item, 5)
        self.virtGroupBox.setLayout(self.virtLayout)

    def createSwap(self):
        swap = psutil.swap_memory()
        self.swapGroupBox = QGroupBox("SWAP缓冲区信息")
        self.swapLayout = QGridLayout()
        item = self.addLabel("交换内存字节总数：", str(swap.total))
        self.addSwapItem(item, 0)
        item = self.addLabel("交换内存已使用字节数：", str(swap.used))
        self.addSwapItem(item, 1)
        item = self.addLabel("交换内存剩余字节数：", str(swap.free))
        self.addSwapItem(item, 2)
        item = self.addLabel("交换内存使用占比：", str(swap.percent) + " %")
        self.addSwapItem(item, 3)
        item = self.addLabel("从磁盘交换字节数：", str(swap.sin))
        self.addSwapItem(item, 4)
        item = self.addLabel("交换进磁盘字节数：", str(swap.sout))
        self.addSwapItem(item, 5)
        self.swapGroupBox.setLayout(self.swapLayout)

    def addVirtItem(self, item, num):
        self.virtLayout.addWidget(item[0], num, 0)
        self.virtLayout.addWidget(item[1], num, 1, 1, 128)

    def addSwapItem(self, item, num):
        self.swapLayout.addWidget(item[0], num, 0)
        self.swapLayout.addWidget(item[1], num, 1, 1, 128)
    
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
    memview = MemView()
    memview.show()
    sys.exit(app.exec_())
