#!/usr/bin/env python3

#################################################################
##
## graduation project
##
#################################################################

from PyQt5.QtCore import (pyqtSignal, QSize, Qt)
from PyQt5.QtGui import (QColor, QFont, QIcon)
from PyQt5.QtWidgets import (QAction, QApplication, QButtonGroup, QComboBox,
        QDialog, QFontComboBox, QGridLayout, QStyleFactory, QHBoxLayout, QLabel, QMenu, 
        QMainWindow, QMessageBox, QToolBox, QToolButton, QWidget, QStackedWidget,
        QScrollArea, QDesktopWidget) 
import os, time

from DialogMe import *
from SelectView import *
from  SysView import *
from CpuView import *
from MemView  import *
from PartitionView import *
from NetView import *
from UserView import *
from IPBelong import *
from SysView import *
from ViewAdd import *
from ViewMan import *
from NameAdd import *
from NameMan import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.createActions()
        self.createMenus()
        self.createToolBox()
        self.createToolbars()
        self.createRightScreen()
        self.resize(640, 370)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())/2, \
            (screen.height() - size.height())/2)

        layout = QHBoxLayout()
        layout.addWidget(self.leftWidget, 10, Qt.AlignTop)
        layout.addWidget(self.rightArea, 10, Qt.AlignTop)

        self.widget = QWidget()
        self.widget.setLayout(layout)
        
        self.setCentralWidget(self.widget)
        self.setWindowTitle("BIND GUI MANAGER")        

    def createRightScreen(self):
        self.rightArea = QScrollArea()
        self.rightScreen = QStackedWidget()
        self.rightScreen.addWidget(SysView())
        self.rightScreen.addWidget(CpuView())
        self.rightScreen.addWidget(MemView())
        self.rightScreen.addWidget(PartitionView())
        self.rightScreen.addWidget(NetView())
        self.rightScreen.addWidget(UserView())
        self.rightScreen.addWidget(NameAdd())
        self.rightScreen.addWidget(NameMan())
        self.rightScreen.addWidget(ViewAdd())
        self.rightScreen.addWidget(ViewMan())
        self.rightScreen.addWidget(IPBelong())
        self.rightArea.setWidget(self.rightScreen)

    def createActions(self):
        self.toWinStyleAction = QAction(
                QIcon('images/Windows.png'),"Change to &Windows Style",
                self, shortcut="Ctrl+W", statusTip="Change Windows Style",
                triggered=self.changeStyleW) 
        
        self.toGTKStyleAction = QAction(
                QIcon('images/GTK.png'), "Change to &GTK+ Style",
                self, shortcut="Ctrl+G", statusTip="Change GTK+ Style",
                triggered=self.changeStyleG)

        self.toFusStyleAction = QAction(
                QIcon('images/Fusion.png'), "Change to &Fusion Style",
                self, shortcut="Ctrl+F", statusTip="Change Fusion Style",
                triggered=self.changeStyleF)

        self.startAction = QAction(
                QIcon('images/start.png'), "Start BIND Service", self,
                statusTip="Start BIND Service", triggered=self.startBIND)

        self.restartAction = QAction(
                QIcon('images/restart.png'), "Restart BIND Service", self,
                statusTip="Restart BIND Service", triggered=self.restartBIND)

        self.stopAction = QAction(
                QIcon('images/stop.png'), "Stop BIND Service", self,
                statusTip="Stop BIND Service", triggered=self.stopBIND)
        
        self.reloadAction = QAction(
                QIcon('images/reload.png'), "Reload BIND Service", self,
                statusTip="Reload BIND Service", triggered=self.reloadBIND)

        self.exitAction = QAction(
                QIcon('images/exit.png'), "&Exit", self, shortcut="Ctrl+E",
                statusTip="Quit the manager GUI", triggered=self.close)

        self.aboutAction = QAction("About Qt", self, shortcut="Ctrl+B",
                triggered=QApplication.instance().aboutQt)
        self.aboutMeAction = QAction("About Me", self, shortcut="Ctrl+M",
                triggered=self.aboutMe)
        

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.startAction)
        self.fileMenu.addAction(self.stopAction)
        self.fileMenu.addAction(self.reloadAction)
        self.fileMenu.addAction(self.restartAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)

        self.styleMenu = self.menuBar().addMenu("&Style")
        self.styleMenu.addAction(self.toWinStyleAction)
        self.styleMenu.addAction(self.toGTKStyleAction)
        self.styleMenu.addAction(self.toFusStyleAction)
        
        self.aboutMenu = self.menuBar().addMenu("&Help")
        self.aboutMenu.addAction(self.aboutAction)
        self.aboutMenu.addSeparator()
        self.aboutMenu.addAction(self.aboutMeAction)
    
    def createToolBox(self):
        flag = SelectView(self)
        self.leftWidget = flag.leftWidget
        self.leftWidget.widget(0).currentItemChanged.connect(self.changeSysScreen)
        self.leftWidget.widget(1).currentItemChanged.connect(self.changeBindScreen)

    def changeSysScreen(self, current, previous):
        if not current:
            current = previous
        self.rightScreen.setCurrentIndex(self.leftWidget.widget(0).row(current))
        self.rightScreen.widget(self.leftWidget.widget(0).row(current)).updateShow()
    
    def changeBindScreen(self, current, previous):
        if not current:
            current = previous
        self.rightScreen.setCurrentIndex(self.leftWidget.widget(1).row(current) + 6)
        self.rightScreen.widget(self.leftWidget.widget(1).row(current)+6).updateShow()

    def createToolbars(self):
        self.serviceToolBar = self.addToolBar("Service")
        self.serviceToolBar.addAction(self.startAction)
        self.serviceToolBar.addAction(self.stopAction)
        self.serviceToolBar.addAction(self.reloadAction)
        self.serviceToolBar.addAction(self.restartAction)
        self.serviceToolBar.addAction(self.exitAction)

        self.styleToolBar = self.addToolBar("Style")
        self.styleToolBar.addAction(self.toWinStyleAction)
        self.styleToolBar.addAction(self.toGTKStyleAction)
        self.styleToolBar.addAction(self.toFusStyleAction)

    def getStatus(self):
        return os.popen("service bind9 status | grep Active | grep -o '(.*)'").read().strip()
    
    def startBIND(self):
        status = self.getStatus()
        if status == "(running)":
            QMessageBox.about(self, "Warn", "BIND已经启动！！！")
            return
        os.popen("service bind9 start") 
        time.sleep(1)
        if self.getStatus() == "(running)":
            QMessageBox.about(self, "Success", "BIND启动成功！！！")
        else:
            QMessageBox.about(self, "Failure", "BIND发生未知错误不能启动!!!")

    def restartBIND(self):
        os.popen("service bind9 restart")
        time.sleep(1)
        if self.getStatus() == "(running)":
            QMessageBox.about(self, "Success", "BIND重启成功！！！")
        else:
            QMessageBox.about(self, "Failure", "BIND发生未知错误不能启动!!!")
        
    def reloadBIND(self):
        os.popen("service bind9 reload")
        status = self.getStatus()
        time.sleep(1)
        if status == "(running)":
            QMessageBox.about(self, "Success", "BIND重加载成功！！！")
        else:
            QMessageBox.about(self, "Failure", "BIND发生未知错误不能重加载!!!")
        

    def stopBIND(self):
        status = self.getStatus()
        if self.getStatus() == "(dead)":
            QMessageBox.about(self, "Warn", "BIND原本就关闭")
            return
        os.popen("service bind9 stop")
        time.sleep(1)
        if self.getStatus() == "(dead)":
            QMessageBox.about(self, "Success", "BIND关闭成功！！！")
        else:
            QMessageBox.about(self, "Failure", "BIND发生未知错误不能关闭!!!")
        

    def changeStyleW(self):
        self.changeStyle("Windows")

    def changeStyleG(self):
        self.changeStyle("GTK+")

    def changeStyleF(self):
        self.changeStyle("Fusion")

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        #QApplication.setStyle(QStyleFactory.create(styleName))
    
    def aboutMe(self):
        DialogMe(self).show()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
