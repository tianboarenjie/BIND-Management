#!/usr/bin/env python3

from PyQt5.QtWidgets import (QApplication, QDialog, QDialog,
        QDialogButtonBox, QFrame, QLabel, QTabWidget, QTextEdit,
        QScrollArea, QVBoxLayout, QHBoxLayout, QWidget)

class DialogMe(QDialog):
    def __init__(self, parent=None):
        super(DialogMe, self).__init__(parent)
        
        me = Me()
        pro = Project()
        bind = Bind()
        tabWidget = QTabWidget()
        tabWidget.addTab(me, "基本信息")
        tabWidget.addTab(pro, "课题简介")
        tabWidget.addTab(bind, "关于BIND")

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)

        buttonBox.accepted.connect(self.accept)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("About Me")

class Me(QWidget):
    def __init__(self, parent=None):
        super(Me, self).__init__(parent)

        nameLabel = QLabel("姓名：")
        nameValueLabel = QLabel("刘文杰")
        nameValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        stuNumLabel = QLabel("学号：")
        stuNumValueLabel = QLabel("201208066043")
        stuNumValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        classLabel = QLabel("班级：")
        classValueLabel = QLabel("12级网络工程（一）班")
        classValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        
        thesisLabel = QLabel("课题：")
        thesisValueLabel = QLabel("")
        thesisValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(nameLabel)
        mainLayout.addWidget(nameValueLabel)
        mainLayout.addWidget(stuNumLabel)
        mainLayout.addWidget(stuNumValueLabel)
        mainLayout.addWidget(classLabel)
        mainLayout.addWidget(classValueLabel)
        mainLayout.addWidget(thesisLabel)
        mainLayout.addWidget(thesisValueLabel)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

class Project(QWidget):
    def __init__(self, parent=None):
        super(Project, self).__init__(parent)
        
        textEdit = QTextEdit()

        textEdit.setPlainText("设计说明")
        textEdit.setReadOnly(True)
        textEdit.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        mainLayout = QHBoxLayout()
        #mainLayout.setContentSMargins(5, 5, 5, 5)
        mainLayout.addWidget(textEdit)
        self.setLayout(mainLayout)

class Bind(QWidget):
    def __init__(self, parent=None):
        super(Bind, self).__init__(parent)
        
        textEdit = QTextEdit()

        textEdit.setPlainText("BIND是一款开放源码的DNS服务器软件，"
        "BIND由美国加州大学Berkeley分校开发和维护的，全名为Berkeley Internet Name Domain它是"
        "目前世界上使用最为广泛的DNS服务器软件，支持各种unix平台和windows平台")
        textEdit.setReadOnly(True)
        textEdit.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        mainLayout = QHBoxLayout()
        #mainLayout.setContentSMargins(5, 5, 5, 5)
        mainLayout.addWidget(textEdit)
        self.setLayout(mainLayout)

if __name__ == "__main__":
    
    import sys
    
    app = QApplication(sys.argv)
    dialogme = DialogMe()
    dialogme.show()
    sys.exit(app.exec_())
