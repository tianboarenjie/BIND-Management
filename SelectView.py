#!/usr/bin/env python3

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QButtonGroup, QVBoxLayout, QLabel,
        QListWidget, QListWidgetItem, QSizePolicy, QStackedWidget, QToolBox, 
        QToolButton, QWidget)

class SelectView(QWidget):
    def __init__(self, parent=None):
        super(SelectView, self).__init__(parent)
        
        self.leftWidget = self.createLeft()
        self.leftWidget.setMinimumHeight(256)
        self.leftWidget.setMaximumWidth(128)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.leftWidget)
        self.setLayout(mainLayout)

    def createLeft(self):
        leftBox = QToolBox()
        leftSys = self.createLeftSys()
        leftBind = self.createLeftBind()
        leftBox.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))
        leftBox.addItem(leftSys, "系统信息")
        leftBox.addItem(leftBind, "BIND调整")
        
        return leftBox

    def createLeftSys(self):
        sysWidget = QListWidget()

        sysWidget.setSpacing(5)
        sysButton = QListWidgetItem(sysWidget)
        sysButton.setText("系统平台")
        sysButton.setTextAlignment(Qt.AlignHCenter)
        sysButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  

        sysButton = QListWidgetItem(sysWidget)
        sysButton.setText("CPU信息")
        sysButton.setTextAlignment(Qt.AlignHCenter)
        sysButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        memButton = QListWidgetItem(sysWidget)
        memButton.setText("内存信息")
        memButton.setTextAlignment(Qt.AlignHCenter)
        memButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
#        if memButton.isSelected():
#            print(memButton.text())

        partButton = QListWidgetItem(sysWidget)
        partButton.setText("分区详情")
        partButton.setTextAlignment(Qt.AlignHCenter)
        partButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        netButton = QListWidgetItem(sysWidget)
        netButton.setText("网络信息")
        netButton.setTextAlignment(Qt.AlignHCenter)
        netButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        
        loginButton = QListWidgetItem(sysWidget)
        loginButton.setText("登陆用户")
        loginButton.setTextAlignment(Qt.AlignHCenter)
        loginButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        
        return sysWidget
#        self.contentsWidgetItemChanged.connect(self.changeView)
    def createLeftBind(self):
        bindWidget = QListWidget()
        bindWidget.setSpacing(5)
        
        azoneButton = QListWidgetItem(bindWidget)
        azoneButton.setText("添加域")
        azoneButton.setTextAlignment(Qt.AlignHCenter)
        azoneButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        
        zoneButton = QListWidgetItem(bindWidget)
        zoneButton.setText("域管理")
        zoneButton.setTextAlignment(Qt.AlignHCenter)
        zoneButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled) 

        aviewButton = QListWidgetItem(bindWidget)
        aviewButton.setText("添加视图")
        aviewButton.setTextAlignment(Qt.AlignHCenter)
        aviewButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  
        
        viewButton = QListWidgetItem(bindWidget)
        viewButton.setText("视图管理")
        viewButton.setTextAlignment(Qt.AlignHCenter)
        viewButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
 
        ipbeButton = QListWidgetItem(bindWidget)
        ipbeButton.setText("IP归属地")
        ipbeButton.setTextAlignment(Qt.AlignHCenter)
        ipbeButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        return bindWidget
    

if __name__ == "__main__":

    import sys
    app = QApplication(sys.argv)
    select = SelectView()
    select.show()
    sys.exit(app.exec_())
