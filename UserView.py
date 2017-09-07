#!/usr/bin/env python3
#

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGroupBox, QGridLayout, QLabel, 
        QHBoxLayout, QVBoxLayout, QSizePolicy, QWidget, QFrame)
import psutil
import datetime

class UserView(QWidget):
    def __init__(self, parent=None):
        super(UserView, self).__init__(parent)
        
#        self.setFixedSize(450, 280)
        self.mainLayout = QVBoxLayout() 
        self.createUserGroup()
        self.mainLayout.addWidget(self.userGroupBox)
        self.setLayout(self.mainLayout)

    def updateShow(self):
        self.userGroupBox.deleteLater()
        self.createUserGroup()
        self.mainLayout.addWidget(self.userGroupBox)
#        self.update()

    def createUserGroup(self):
        self.userGroupBox = QGroupBox("用户登录信息")
        self.userLayout = QGridLayout()
        self.userLayout.setRowStretch(100, 100)

        info = psutil.users()
#        print(len(psutil.users()))
        num = 1
        self.userLayout.addWidget(self.addLabel("登陆名"), 0, 0)
        self.userLayout.addWidget(self.addLabel("登陆终端"), 0, 1)
        self.userLayout.addWidget(self.addLabel("登陆主机"), 0, 2)
        self.userLayout.addWidget(self.addLabel("登陆时间"), 0, 3)
        for i in info:
            self.insertUser(i, num)
            num += 1
        self.userGroupBox.setLayout(self.userLayout)

    def addLabel(self, value):
        label = QLabel(value)
        label.setAlignment(Qt.AlignHCenter)
        return label

    def insertUser(self, user, num):
        self.userLayout.addWidget(self.addLine(user.name), num, 0)
        self.userLayout.addWidget(self.addLine(user.terminal), num, 1)
        self.userLayout.addWidget(self.addLine(user.host), num, 2)
        self.userLayout.addWidget(self.addLine(datetime.datetime.\
            fromtimestamp(user.started).strftime("%Y-%m-%d %H:%M:%S")), num, 3)

    def addLine(self, value):
        line = QLabel(value)
        line.setAlignment(Qt.AlignCenter)
        line.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))
        line.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        return line

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    user = UserView()
    user.show()
    sys.exit(app.exec_())

