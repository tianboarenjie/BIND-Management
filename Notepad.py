#!/usr/bin/env python3
#
import sys
import os
import configparser as parser
from PyQt5.QtCore import (QFile, QTextStream, Qt, QFileInfo, QTextCodec, QSize,
        QPoint)
from PyQt5.QtGui import (QTextCursor, QFont, QKeySequence)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPlainTextEdit, QMenu,
        QDesktopWidget, QMessageBox, QAction, QDialog, QLabel, QPushButton, 
        QDialogButtonBox, QHBoxLayout, QVBoxLayout, QGridLayout, QLayout,
        QLineEdit, QFontDialog)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter

QTextCodec.setCodecForLocale(QTextCodec.codecForName("UTF-8"))
CONFIG_FILE_PATH = "notepad.ini"


class Notepad(QMainWindow):
    def __init__(self):
        self.judgeConfigFile()
        self.clipboard = QApplication.clipboard()
        self.lastSearchText = ""
        self.lastReplaceSearchText = ""
        self.reset = False
        self.config = parser.ConfigParser()
        self.config.read(CONFIG_FILE_PATH)

        QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("无标题 - 记事本")

        self.initEditText()

        self.createActions()
        self.createStatusBar()
        self.createMenubars()

        self.readSettings()

        self.text.document().contentsChanged.connect(self.documentWasModified)

        self.setCurrentFile('')

    def initEditText(self):
        self.text = QPlainTextEdit()
        self.text.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text.customContextMenuRequested.connect(self.customContextMenu)
        self.setCentralWidget(self.text)

    def customContextMenu(self):
        menu = QMenu(self)
        menu.addAction(self.undoAction)
        menu.addSeparator()
        menu.addAction(self.cutAction)
        menu.addAction(self.copyAction)
        menu.addAction(self.pasteAction)
        menu.addAction(self.deleteAction)
        menu.addSeparator()
        menu.addAction(self.selectAllAction)
        menu.exec_(QCursor.pos())

        return menu

    def documentWasModified(self):
        self.setWindowModified(self.text.document().isModified())
        if "" != self.text.toPlainText():
            self.findAction.setEnabled(True)
            self.findNextAction.setEnabled(True)
        else:
            self.findAction.setEnabled(False)
            self.findNextAction.setEnabled(False)

    def readSettings(self):
        width = getConfig(self.config, "Display", "width", "1000")
        height = getConfig(self.config, "Display", "height", "600")
        size = QSize(int(width), int(height))

        screen = QDesktopWidget().screenGeometry()
        pos_x = getConfig(self.config, "Display", "x", (screen.width() - 1000) // 2)
        pos_y = getConfig(self.config, "Display", "y", (screen.height() - 600) // 2)
        pos = QPoint(int(pos_x), int(pos_y))

        toolbar = getConfig(self.config, "Display", "toolbar", "True")

        wrapMode = getConfig(self.config, "TextEdit", "wrapmode", "True")

        fontFamile = getConfig(self.config, "TextEdit", "font", "Consolas")
        fontSize = getConfig(self.config, "TextEdit", "size", 14)
        fonts = QFont(fontFamile, int(fontSize))

        if "True" == wrapMode:
            wrapMode = QPlainTextEdit.WidgetWidth
        else:
            wrapMode = QPlainTextEdit.NoWrap

        self.resize(size)
        self.move(pos)
        self.text.setLineWrapMode(wrapMode)
        self.text.setFont(fonts)

    def resetSettings(self):
        writeConfig(self.config, "Display", "width", "1000")
        writeConfig(self.config, "Display", "height", "600")
        screen = QDesktopWidget().screenGeometry()
        writeConfig(self.config, "Display", "x", str((screen.width() - 1000) // 2))
        writeConfig(self.config, "Display", "y", str((screen.height() - 600) // 2))
        writeConfig(self.config, "Display", "toolbar", "True")
        writeConfig(self.config, "TextEdit", "wrapmode", "True")
        writeConfig(self.config, "TextEdit", "font", "Consolas")
        writeConfig(self.config, "TextEdit", "size", "14")

        self.config.write(open(CONFIG_FILE_PATH, "w"))

        QMessageBox.information(self, "记事本", "重置成功，请重启记事本！")
        self.reset = True
        self.close()

    def writeSettings(self):
        writeConfig(self.config, "Display", "height", str(self.size().height()))
        writeConfig(self.config, "Display", "width", str(self.size().width()))
        writeConfig(self.config, "Display", "x", str(self.pos().x()))
        writeConfig(self.config, "Display", "y", str(self.pos().y()))
        writeConfig(self.config, "TextEdit", "wrapmode",
                    str(self.text.lineWrapMode() == QPlainTextEdit.WidgetWidth))
        writeConfig(self.config, "TextEdit", "font", self.text.font().family())
        writeConfig(self.config, "TextEdit", "size", str(self.text.font().pointSize()))

        self.config.write(open(CONFIG_FILE_PATH, "w"))

    def judgeConfigFile(self):
        if not os.path.exists(CONFIG_FILE_PATH):
            f = open(CONFIG_FILE_PATH, mode="w", encoding="UTF-8")
            f.close()

    def createActions(self):

        self.saveAction = QAction("&保存", self,
                                            shortcut=QKeySequence.Save,
                                            statusTip="保存文件", triggered=self.save)

        self.exitAction = QAction("退出", self, shortcut="Ctrl+Q",
                                            statusTip="退出程序", triggered=self.close)

        self.undoAction = QAction("撤销", self,
                                            shortcut=QKeySequence.Undo,
                                            statusTip="撤销编辑",
                                            triggered=self.text.undo)

        self.cutAction = QAction("剪切", self,
                                           shortcut=QKeySequence.Cut,
                                           statusTip="剪切选中的文本",
                                           triggered=self.text.cut)

        self.copyAction = QAction("复制", self,
                                            shortcut=QKeySequence.Copy,
                                            statusTip="复制选中的文本",
                                            triggered=self.text.copy)

        self.pasteAction = QAction("粘贴", self,
                                             shortcut=QKeySequence.Paste,
                                             statusTip="粘贴剪切板的文本",
                                             triggered=self.text.paste)

        self.clearAction = QAction("清空剪切板", self,
                                             statusTip="清空剪切板",
                                             triggered=self.clearClipboard)

        self.deleteAction = QAction("删除", self,
                                              statusTip="删除选中的文本",
                                              triggered=self.delete)

        self.findAction = QAction("查找", self,
                                            statusTip="查找文本", triggered=self.findText, shortcut=QKeySequence.Find)

        self.findNextAction = QAction("查找下一个", self,
                                                statusTip="查找文本", triggered=self.findNextText,
                                                shortcut=QKeySequence.FindNext)

        self.replaceAction = QAction("替换", self,
                                               statusTip="替换文本", triggered=self.replaceText,
                                               shortcut=QKeySequence.Replace)

        self.selectAllAction = QAction("全选", self,
                                                 shortcut=QKeySequence.SelectAll,
                                                 statusTip="全选",
                                                 triggered=self.text.selectAll)

        self.autoWrapAction = QAction("自动换行", self,
                                                statusTip="设置自动换行",
                                                triggered=self.setWrap)

        self.fontAction = QAction("字体", self,
                                            statusTip="设置字体", triggered=self.setFont_)


        self.aboutQtAction = QAction("关于Qt", self,
                                               triggered=QApplication.instance().aboutQt)

        self.undoAction.setEnabled(False)
        self.cutAction.setEnabled(False)
        self.copyAction.setEnabled(False)
        self.deleteAction.setEnabled(False)
        if "" == self.clipboard.text():
            self.pasteAction.setEnabled(False)
            self.clearAction.setEnabled(False)
        if "" == self.text.toPlainText():
            self.findAction.setEnabled(False)
            self.findNextAction.setEnabled(False)

        self.text.undoAvailable.connect(self.undoAction.setEnabled)
        self.text.copyAvailable.connect(self.cutAction.setEnabled)
        self.text.copyAvailable.connect(self.copyAction.setEnabled)
        self.text.copyAvailable.connect(self.deleteAction.setEnabled)

        self.clipboard.dataChanged.connect(self.enabledSomeActionByClipboard)

    def enabledSomeActionByClipboard(self):
        if ("" != self.clipboard.text()):
            self.pasteAction.setEnabled(True)
            self.clearAction.setEnabled(True)

    def clearClipboard(self):
        self.clipboard.clear()
        self.pasteAction.setEnabled(False)
        self.clearAction.setEnabled(False)

    def createStatusBar(self):
        self.statusBar().showMessage("准备就绪")

    def createMenubars(self):
        file = self.menuBar().addMenu("文件")
        file.addAction(self.saveAction)
        file.addSeparator()
        file.addSeparator()
        file.addAction(self.exitAction)

        edit = self.menuBar().addMenu("编辑")
        edit.addAction(self.undoAction)
        edit.addSeparator()
        edit.addAction(self.cutAction)
        edit.addAction(self.copyAction)
        edit.addAction(self.pasteAction)
        edit.addAction(self.clearAction)
        edit.addAction(self.deleteAction)
        edit.addSeparator()
        edit.addAction(self.findAction)
        edit.addAction(self.findNextAction)
        edit.addAction(self.replaceAction)
        edit.addSeparator()
        edit.addAction(self.selectAllAction)

        style = self.menuBar().addMenu("格式")
        style.addAction(self.autoWrapAction)
        style.addAction(self.fontAction)

        help = self.menuBar().addMenu("帮助")
        help.addAction(self.aboutQtAction)

    def maybeSave(self):
        if self.text.document().isModified():
            ret = self.tip()

            if 0 == ret:
                return self.save()

            if 2 == ret:
                return False

        return True

    def openFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "记事本",
                                          "文件%s不能被读取:\n%s." % (fileName, file.errorString()))
            return

        inf = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.text.setPlainText(inf.readAll())
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.show()
        self.statusBar().showMessage("文件读取成功", 2000)

    def setCurrentFile(self, fileName):
        self.curFile = fileName
        self.text.document().setModified(False)
        self.setWindowModified(False)

        if self.curFile:
            shownName = self.strippedName(self.curFile)
        else:
            shownName = '未命名.txt'

        self.setWindowTitle("%s[*] - 记事本" % shownName)

    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()

    def save(self):
        if self.curFile:
            return self.saveFile(self.curFile)
        else:
            return self.saveAs()

    def saveFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "记事本",
                                          "文件%s不能被写入:\n%s." % (fileName, file.errorString()))
            return False

        outf = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outf << self.text.toPlainText()
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("写入文件成功", 2000)
        return True

    def closeEvent(self, event):
        if not self.maybeSave():
            event.ignore()
        else:
            if not self.reset:
                self.writeSettings()
            event.accept()

    def tip(self, title="记事本", content="文件已被修改，是否保存？"):
        alertBox = QMessageBox(self)
        saveButton = alertBox.addButton("保存", QMessageBox.ActionRole)
        unSaveButton = alertBox.addButton("不保存", QMessageBox.ActionRole)
        cancelButton = alertBox.addButton("取消", QMessageBox.ActionRole)

        alertBox.setWindowTitle(title)
        alertBox.setText(content)
        alertBox.exec_()
        button = alertBox.clickedButton()

        if saveButton == button:
            return 0
        elif unSaveButton == button:
            return 1
        elif cancelButton == button:
            return 2
        else:
            return -1;

    def delete(self):
        cursor = self.text.textCursor()
        if not cursor.isNull():
            cursor.removeSelectedText()
            self.statusBar().showMessage("删除成功", 2000)

    def findText(self):
        self.displayFindDialog()

    def findNextText(self):
        if "" == self.lastSearchText:
            self.displayFindDialog()
        else:
            self.searchText()

    def displayFindDialog(self):
        self.findDialog = QDialog(self)

        label = QLabel("查找内容:")
        self.lineEdit = QLineEdit()
        self.lineEdit.setText(self.lastSearchText)
        label.setBuddy(self.lineEdit)

        self.findButton = QPushButton("查找下一个")
        self.findButton.setDefault(True)
        self.findButton.clicked.connect(self.searchText)

        buttonBox = QDialogButtonBox(Qt.Vertical)
        buttonBox.addButton(self.findButton, QDialogButtonBox.ActionRole)

        topLeftLayout = QHBoxLayout()
        topLeftLayout.addWidget(label)
        topLeftLayout.addWidget(self.lineEdit)

        leftLayout = QVBoxLayout()
        leftLayout.addLayout(topLeftLayout)

        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addLayout(leftLayout, 0, 0)
        mainLayout.addWidget(buttonBox, 0, 1)
        mainLayout.setRowStretch(2, 1)
        self.findDialog.setLayout(mainLayout)

        self.findDialog.setWindowTitle("查找")
        self.findDialog.show()

    def searchText(self):
        cursor = self.text.textCursor()
        findIndex = cursor.anchor()
        text = self.lineEdit.text()
        content = self.text.toPlainText()
        length = len(text)

        self.lastSearchText = text
        index = content.find(text, findIndex)

        if -1 == index:
            errorDialog = QMessageBox(self)
            errorDialog.addButton("取消", QMessageBox.ActionRole)

            errorDialog.setWindowTitle("记事本")
            errorDialog.setText("找不到\"%s\"." % text)
            errorDialog.setIcon(QMessageBox.Critical)
            errorDialog.exec_()
        else:
            start = index

            cursor = self.text.textCursor()
            cursor.clearSelection()
            cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, start + length)
            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, length)
            cursor.selectedText()
            self.text.setTextCursor(cursor)

    def replaceText(self):
        replaceDialog = QDialog(self)

        replaceLabel = QLabel("替换内容:")
        self.replaceText = QLineEdit()
        self.replaceText.setText(self.lastReplaceSearchText)
        replaceLabel.setBuddy(self.replaceText)

        replaceToLabel = QLabel("替换为  :")
        self.replaceToText = QLineEdit()
        replaceToLabel.setBuddy(self.replaceToText)

        findNextButton = QPushButton("查找下一个")
        findNextButton.setDefault(True)
        replaceButton = QPushButton("替换")
        replaceAllButton = QPushButton("全部替换")
        cancelAllButton = QPushButton("取消")

        findNextButton.clicked.connect(lambda: self.replaceOrSearch(False))
        cancelAllButton.clicked.connect(replaceDialog.close)
        replaceButton.clicked.connect(lambda: self.replaceOrSearch(True))
        replaceAllButton.clicked.connect(self.replaceAllText)

        buttonBox = QDialogButtonBox(Qt.Vertical)
        buttonBox.addButton(findNextButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(replaceButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(replaceAllButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(cancelAllButton, QDialogButtonBox.ActionRole)

        topLeftLayout = QHBoxLayout()

        topLeftLayout.addWidget(replaceLabel)
        topLeftLayout.addWidget(self.replaceText)

        topLeftLayout2 = QHBoxLayout()
        topLeftLayout2.addWidget(replaceToLabel)
        topLeftLayout2.addWidget(self.replaceToText)

        leftLayout = QVBoxLayout()
        leftLayout.addLayout(topLeftLayout)
        leftLayout.addLayout(topLeftLayout2)

        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addLayout(leftLayout, 0, 0)
        mainLayout.addWidget(buttonBox, 0, 1)
        mainLayout.setRowStretch(2, 1)
        replaceDialog.setLayout(mainLayout)

        replaceDialog.setWindowTitle("替换")
        replaceDialog.show()

    def replaceOrSearch(self, isReplace):
        cursor = self.text.textCursor()
        findIndex = cursor.anchor()
        text = self.replaceText.text()
        content = self.text.toPlainText()
        length = len(text)
        index = content.find(text, findIndex)
        self.lastReplaceSearchText = text
        if -1 == index:
            errorDialog = QMessageBox(self)
            errorDialog.addButton("取消", QMessageBox.ActionRole)

            errorDialog.setWindowTitle("记事本")
            errorDialog.setText("找不到\"%s\"." % text)
            errorDialog.setIcon(QMessageBox.Critical)
            errorDialog.exec_()
        else:
            start = index
            if isReplace:
                toReplaceText = self.replaceToText.text()
                prefix = content[0:start]
                postfix = content[start + length:]
                newText = prefix + toReplaceText + postfix
                self.text.setPlainText(newText)
                length = len(toReplaceText)
                self.text.document().setModified(True)

            cursor = self.text.textCursor()
            cursor.clearSelection()
            cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, start + length)
            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, length)
            cursor.selectedText()
            self.text.setTextCursor(cursor)

    def replaceAllText(self):
        text = self.replaceText.text()
        content = self.text.toPlainText()
        toReplaceText = self.replaceToText.text()
        content = content.replace(text, toReplaceText)
        self.text.setPlainText(content)
        self.text.document().setModified(True)

    def setWrap(self):
        mode = self.text.lineWrapMode()
        if 1 == mode:
            self.text.setLineWrapMode(QPlainTextEdit.NoWrap)
        else:
            self.text.setLineWrapMode(QPlainTextEdit.WidgetWidth)

    def toggleToolBar(self):
        if self.toolBar.isHidden():
            self.toolBar.show()
        else:
            self.toolBar.hide()

    def preferences(self):
        print("")

    def setFont_(self):
        font, ok = QFontDialog.getFont(QFont(self.text.toPlainText()), self)
        if ok:
            self.text.setFont(font)


def getConfig(config, selection, option, default=""):
    if config is None:
        return default
    else:
        try:
            return config.get(selection, option)
        except:
            return default


def writeConfig(config, selection, option, value):
    if not config.has_section(selection):
        config.add_section(selection)

    config.set(selection, option, value)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    notepad = Notepad()
    notepad.openFile("/home/tianming/notepad-pyqt5/Notepad.py")
#    notepad.show()
    app.exec_()
