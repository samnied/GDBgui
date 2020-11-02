# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnRun = QtWidgets.QPushButton(self.centralwidget)
        self.btnRun.setGeometry(QtCore.QRect(40, 160, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnRun.setFont(font)
        self.btnRun.setObjectName("btnRun")
        self.pathEdit1 = QtWidgets.QLineEdit(self.centralwidget)
        self.pathEdit1.setGeometry(QtCore.QRect(140, 50, 371, 22))
        self.pathEdit1.setObjectName("pathEdit1")
        self.pathEdit2 = QtWidgets.QLineEdit(self.centralwidget)
        self.pathEdit2.setGeometry(QtCore.QRect(140, 90, 371, 22))
        self.pathEdit2.setObjectName("pathEdit2")
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(50, 50, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label1.setFont(font)
        self.label1.setObjectName("label1")
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(50, 100, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label2.setFont(font)
        self.label2.setObjectName("label2")
        self.btnSearch1 = QtWidgets.QPushButton(self.centralwidget)
        self.btnSearch1.setGeometry(QtCore.QRect(520, 50, 93, 28))
        self.btnSearch1.setObjectName("btnSearch1")
        self.btnSearch2 = QtWidgets.QPushButton(self.centralwidget)
        self.btnSearch2.setGeometry(QtCore.QRect(520, 90, 93, 28))
        self.btnSearch2.setObjectName("btnSearch2")
        self.textOutput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textOutput.setGeometry(QtCore.QRect(40, 220, 411, 301))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.textOutput.setFont(font)
        self.textOutput.setObjectName("textOutput")
        self.errorOutput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.errorOutput.setGeometry(QtCore.QRect(520, 240, 241, 87))
        self.errorOutput.setObjectName("errorOutput")
        self.label3 = QtWidgets.QLabel(self.centralwidget)
        self.label3.setGeometry(QtCore.QRect(520, 200, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label3.setFont(font)
        self.label3.setObjectName("label3")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(160, 160, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnRun.setText(_translate("MainWindow", "RUN"))
        self.label1.setText(_translate("MainWindow", "Elf File"))
        self.label2.setText(_translate("MainWindow", "Path"))
        self.btnSearch1.setText(_translate("MainWindow", "Search"))
        self.btnSearch2.setText(_translate("MainWindow", "Search"))
        self.label3.setText(_translate("MainWindow", "Status information"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

