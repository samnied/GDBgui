# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 12:40:53 2020
generate code from Qt designer with following command
pyuic5 –x "filename".ui –o "filename".py
pyuic5 –x design.ui –o design.py

@author: Sam
"""
import sys
import subprocess
import threading
from PyQt5 import QtCore, QtGui, QtWidgets

from design import Ui_MainWindow
from FileDialog import FileDialog
from GDBinfo import GDBinfo
from Size import Size

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

class Ui_MainWindowUser(Ui_MainWindow):
    def __init__(self, MainWindow):
        self.setupUi(MainWindow)
        
        self.btnRun.clicked.connect(self.runMeasurement)
        self.btnSearch1.clicked.connect(self.selectElf)
        self.btnSearch2.clicked.connect(self.selectLog)
        
        app.aboutToQuit.connect(self.closeEvent)
        self.progressBar.setValue(0)
        
        # set default value
        elfPath = r"C:\Users\samue\STM32CubeIDE\workspace_1.4.0\EHS\Debug\EHS.elf"
        self.pathEdit1.setText(elfPath)
        
        self.threads = list()
        
        
    def selectElf(self):
        fd = FileDialog()
        fileName = fd.openFileNameDialog()
        if fileName:
            self.pathEdit1.setText(fileName)
    
    
    def selectLog(self):
        fd = FileDialog()
        fileName = fd.saveFileDialog()
        if fileName:
            self.pathEdit2.setText(fileName)
        
        
    def openSt(self):
        print("Try to connect to stlink...")
        # self.errorOutput.insertPlainText("Try to connect to stlink... \n")
        x = subprocess.Popen(GDBinfo.openStlink, stdout=subprocess.PIPE)
        
        while True:
            s = x.stdout.readline().decode('utf-8', errors="ignore")
            if s == '' and x.poll() is not None:
                break
            elif "ST-LINK device initialization OK" in s:
                out = "stlink succsessfully connected\n"
                print(out)
                # self.errorOutput.insertPlainText(out)
            elif "error" in s:
                out = "stlink failed to connect... unplug usb cable and try again\n"
                # self.errorOutput.insertPlainText(out)
                print(out)
                break
            elif " stlink shut down\n" in s:
                print(out)
                # self.errorOutput.insertPlainText("Shut down Stlink server\n")
                break
    
    
    def runGDB(self):
        print("Try to run GDB...")
        # self.errorOutput.insertPlainText("Try to run GDB... \n")
        x = subprocess.Popen(GDBinfo.openGDB + " " + self.pathEdit1.text(), stdout=subprocess.PIPE)
        
        while True:
            s = x.stdout.readline().decode('utf-8', errors="ignore")
            if s == '' and x.poll() is not None:
                break
            if "gdb-script-finished" in s:
                print("Successfully run gdb...")
                # self.errorOutput.insertPlainText("Successfully run gdb...")
                # self.progressBar.setValue(100)
                break
           
            
    def getSizeInfo(self):
        filePath = self.pathEdit1.text()
        return Size.getStr(filePath)
    
    
    def closeEvent(self):
        # wait for the threads to be finished 
        for t in self.threads:
            t.join()
        print("shut down GDBgui ...")
      
        
    def runMeasurement(self):
        self.errorOutput.clear()
        self.textOutput.clear()
        self.progressBar.setValue(0)
        
        self.textOutput.insertPlainText(self.getSizeInfo())
        
        #start Stlink server
        t1 = threading.Thread(target=self.openSt)
        self.threads.append(t1)
        t1.start()
        
        self.progressBar.setValue(50)
        
        #start GDB and run script
        t2 = threading.Thread(target=self.runGDB)
        self.threads.append(t2)
        t2.start()
        
        t2.join()
        self.progressBar.setValue(100)
        

        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindowUser(MainWindow)
    
    MainWindow.show()
    sys.exit(app.exec_())