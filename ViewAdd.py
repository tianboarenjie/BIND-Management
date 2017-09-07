#!/usr/bin/env python3

from PyQt5.QtCore import (Qt, pyqtSignal)
from PyQt5.QtWidgets import (QApplication, QGridLayout, QGroupBox, QLabel,
        QVBoxLayout, QSizePolicy, QWidget, QPushButton, QMessageBox, QLineEdit,
        QHBoxLayout)
from IPy import IP
import os

class ViewAdd(QWidget):
    def __init__(self, parent=None):
        super(ViewAdd, self).__init__(parent)

        self.createBox()
        self.createConfirm()
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.addBox)
        mainLayout.addLayout(self.confirm)
        self.setLayout(mainLayout)
        self.setFixedHeight(150)

    def createBox(self):
        self.addBox = QGroupBox()
        self.addBox.setFixedSize(440, 100)
#        self.addBox.setFixedWidth(400)
        box = QGridLayout()
        viewLabel = QLabel("请输入需要添加的视图名：")
        self.view = QLineEdit("default")
        self.view.setAlignment(Qt.AlignCenter)
        viewLabel.setBuddy(self.view)
        ipLabel = QLabel("请输入匹配该视图的IP段：")
        self.ip = QLineEdit("any;192.168.0.0/16;172.16.0.0/16")
        self.ip.setAlignment(Qt.AlignCenter)
        box.addWidget(viewLabel, 0, 0)
        box.addWidget(self.view, 0, 1, 1,128)
        box.addWidget(ipLabel, 1, 0)
        box.addWidget(self.ip, 1, 1, 1, 128)
        self.addBox.setLayout(box)
    
    def updateShow(self):
        pass
        
    def createConfirm(self):
        self.concel = QPushButton("取消")
        self.concel.setFixedWidth(220)
        self.add = QPushButton("添加")
        self.add.setFixedWidth(220)
        self.confirm = QHBoxLayout()
        self.confirm.addWidget(self.concel)
        self.confirm.addWidget(self.add)
        self.concel.clicked.connect(self.concelView)
        self.add.clicked.connect(self.check)

    def concelView(self):
        self.view.clear()
        self.ip.clear()

    def check(self):
        ip = self.ip.text()
        ip = ip.strip(";")
        ip = ip.split(";") 
        view = self.view.text()
        re_ip = []
        if not view:
            QMessageBox.about(self, "View Error", "视图名称不能为空！！！")
            return
        for i in ip:
            try:
                if i == "any":
                    re_ip.append(i)
                else:
                    re_ip.append(IP(i).strNormal())
            except ValueError:
                QMessageBox.about(self, "Network Error", "IP网段出错，请重新输入！！")
                return
        self.addView(";".join(re_ip), view)

    def addView(self, ip, view):
        db = "/var/cache/bind/" + view
        conf = "/etc/bind/named.conf"
        fil = "/etc/bind/named.conf." + view + "-views"
        if len(os.popen("awk '/" + fil.split('/')[-1] + "/' " + conf).read()):
            QMessageBox.about(self, "Error", "视图" + view + "已经存在！！！")
            self.concelView()
            return
#        os.popen("echo " + fil + ">>" + conf)
        os.popen("echo 'include \"" + fil + "\";' >> " + conf)
        os.popen("mkdir " + db + ";chmod 644 " + db + ";chown root:bind " + db)
        self.createAcl(fil, view, ip)
        QMessageBox.about(self, "Success","添加视图" + view + "成功！！！")

    def createAcl(self, fil, view, ip):
        sep = os.linesep
        os.popen("echo 'acl " + view + " {" +sep + "\t" + ip + ";" + sep +"};" + sep *2 + "' >" + fil)
        os.popen("echo 'view " + "\"" + view + "\" {" + sep + "\tmatch-clients {" + view + ";};"\
            + sep + "\trecursion yes;" + sep + "\tallow-transfer { none;};" + sep*4 + "};" + sep *2 +\
            "' >> " + fil)
        os.popen("chmod 640 " + fil + ";chown root:bind " + fil)



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ins = ViewAdd()
    ins.show()
    sys.exit(app.exec_())

