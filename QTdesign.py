# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QTdesign.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(887, 567)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnRun = QtWidgets.QPushButton(self.centralwidget)
        self.btnRun.setGeometry(QtCore.QRect(10, 160, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnRun.setFont(font)
        self.btnRun.setObjectName("btnRun")
        self.elfPathEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.elfPathEdit.setGeometry(QtCore.QRect(130, 10, 371, 22))
        self.elfPathEdit.setObjectName("elfPathEdit")
        self.savePathEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.savePathEdit.setGeometry(QtCore.QRect(130, 50, 371, 22))
        self.savePathEdit.setObjectName("savePathEdit")
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(10, 10, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label1.setFont(font)
        self.label1.setObjectName("label1")
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(10, 60, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label2.setFont(font)
        self.label2.setObjectName("label2")
        self.btnSearchElfPath = QtWidgets.QPushButton(self.centralwidget)
        self.btnSearchElfPath.setGeometry(QtCore.QRect(510, 10, 93, 28))
        self.btnSearchElfPath.setObjectName("btnSearchElfPath")
        self.btnSearchSavePath = QtWidgets.QPushButton(self.centralwidget)
        self.btnSearchSavePath.setGeometry(QtCore.QRect(510, 50, 93, 28))
        self.btnSearchSavePath.setObjectName("btnSearchSavePath")
        self.textOutput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textOutput.setGeometry(QtCore.QRect(10, 220, 411, 301))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.textOutput.setFont(font)
        self.textOutput.setObjectName("textOutput")
        self.stlinkOutput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.stlinkOutput.setGeometry(QtCore.QRect(440, 220, 431, 87))
        self.stlinkOutput.setObjectName("stlinkOutput")
        self.label3 = QtWidgets.QLabel(self.centralwidget)
        self.label3.setGeometry(QtCore.QRect(440, 180, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label3.setFont(font)
        self.label3.setObjectName("label3")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(130, 160, 161, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label4 = QtWidgets.QLabel(self.centralwidget)
        self.label4.setGeometry(QtCore.QRect(440, 330, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label4.setFont(font)
        self.label4.setObjectName("label4")
        self.gdbOutput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.gdbOutput.setGeometry(QtCore.QRect(440, 370, 431, 151))
        self.gdbOutput.setObjectName("gdbOutput")
        self.label5 = QtWidgets.QLabel(self.centralwidget)
        self.label5.setGeometry(QtCore.QRect(10, 100, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label5.setFont(font)
        self.label5.setObjectName("label5")
        self.commentEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.commentEdit.setGeometry(QtCore.QRect(130, 90, 371, 51))
        self.commentEdit.setObjectName("commentEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 887, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GDBgui"))
        self.btnRun.setText(_translate("MainWindow", "RUN"))
        self.label1.setText(_translate("MainWindow", "Elf File"))
        self.label2.setText(_translate("MainWindow", "Path"))
        self.btnSearchElfPath.setText(_translate("MainWindow", "Search"))
        self.btnSearchSavePath.setText(_translate("MainWindow", "Search"))
        self.label3.setText(_translate("MainWindow", "Stlink Response"))
        self.label4.setText(_translate("MainWindow", "GDB Response"))
        self.label5.setText(_translate("MainWindow", "Comment"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

