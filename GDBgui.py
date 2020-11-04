# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 12:40:53 2020
generate code from Qt designer with following command
pyuic5 –x "filename".ui –o "filename".py
pyuic5 –x QTdesign.ui –o QTdesign.py

@author: Samuel Niederer
"""
import sys
import subprocess
import threading
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog

from QTdesign import Ui_MainWindow
from GDBinfo import GDBinfo
from Size import Size
from Data import Data
from StackInfo import StackInfo

#adjust for high dpi screen
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

class Ui_MainWindowUser(Ui_MainWindow):
    def __init__(self, MainWindow):
        self.setupUi(MainWindow)
        
        # connect signals and slots
        app.aboutToQuit.connect(self.closeEvent)
        self.btnRun.clicked.connect(self.runMeasurement)
        self.btnSearchElfPath.clicked.connect(self.selectElf)
        self.btnSearchSavePath.clicked.connect(self.selectLog)
        
        # set default value
        elfPath = r"C:\Users\samue\STM32CubeIDE\workspace_1.4.0\EHS\Debug\EHS.elf"
        self.elfPathEdit.setText(elfPath)
        savePath = "../logFiles"
        self.savePathEdit.setText(savePath)
        
        self.threads = list()
        
        self.progressBar.setValue(0)
        
        
    def selectElf(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName()[0]
        if fileName:
            self.elfPathEdit.setText(fileName)
    
    
    def selectLog(self):
        fileName = QFileDialog.getExistingDirectory(None, 
                                                  'Select directory', 
                                                  "", 
                                                  QFileDialog.ShowDirsOnly)
        if fileName:
            self.savePathEdit.setText(fileName)
        
        
    def openStlink(self):
        print("Try to connect to stlink...")
        # self.errorOutput.insertPlainText("Try to connect to stlink... \n")
        x = subprocess.Popen(GDBinfo.openStlink, stdout=subprocess.PIPE)
        
        while True:
            s = x.stdout.readline().decode('utf-8', errors="ignore")
            if s == '' and x.poll() is not None:
                break
            elif "ST-LINK device initialization OK" in s:
                out = s + "\n"
                print(out)
                # self.errorOutput.insertPlainText(out)
            elif "Accepted connection" in s:
                out = s + "\n"
                print(out)
            elif "error" in s:
                out = "stlink failed to connect... unplug usb cable and try again\n"
                # self.errorOutput.insertPlainText(out)
                print(out)
                break
            elif " stlink shut down\n" in s:
                out = "Shut down Stlink server \n"
                print(out)
                # self.errorOutput.insertPlainText("Shut down Stlink server\n")
                break
        print("end of function openStlink")
    
    
    def runGDB(self, stThread):
        print("Try to run GDB...")
        
        x = subprocess.Popen(GDBinfo.openGDB + " " + self.elfPathEdit.text(), stdout=subprocess.PIPE)
        
        while True:
            s = x.stdout.readline().decode('utf-8', errors="ignore")
            if s == '' and x.poll() is not None:
                break
            if "gdb-script-finished" in s:
                print("Successfully run gdb...")
                # self.errorOutput.insertPlainText("Successfully run gdb...")
                # self.progressBar.setValue(100)
                break
            elif "gdb-script-error" in s:
                print("an error occured while running gdb, stop execution")
                break
           
            
    def getSizeInfo(self):
        filePath = self.elfPathEdit.text()
        return Size.getStr(filePath)
    
    
    def closeEvent(self):
        # wait for the threads to be finished 
        for t in self.threads:
            t.join()
        print("shut down GDBgui ...")
    
    def infoLog(self, msg):
        if msg == "clear":
            self.errorOutput.clear()
        else:
            self.errorOutput.insertPlainText(msg + "\n")
    
    def saveFile(self, data):
        filePath = self.savePathEdit.text()
        fileName = self.elfPathEdit.text()
        fileName =  fileName.split("\\")[-1].split(".")[0]
        fileName += "_" + datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + ".txt"
        
        with open(filePath + "\\" + fileName,  mode="w") as f:
            f.write(data)
            
        
    def runMeasurement(self):
        self.infoLog("clear")
        self.textOutput.clear()
        self.progressBar.setValue(0)
        
        # run gdb objdump and save resut to .txt
        StackInfo.run(self.elfPathEdit.text())
        
        # print code size information
        self.textOutput.insertPlainText(self.getSizeInfo() + "\n")
        
        
        #start Stlink server
        self.infoLog("Start Stlink server...")
        t1 = threading.Thread(target=self.openStlink)
        self.threads.append(t1)
        t1.start()
        
        self.progressBar.setValue(50)
        
        #start GDB and run script
        t2 = threading.Thread(target=self.runGDB(t1))
        self.threads.append(t2)
        t2.start()
        
        # wait for thread to finish
        t2.join()
        self.progressBar.setValue(100)
        self.infoLog("Successfully run GDB...")
        
        d = Data()
        self.textOutput.insertPlainText(d.getStr())
        
        self.saveFile(self.textOutput.toPlainText())

        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindowUser(MainWindow)
    
    MainWindow.show()
    sys.exit(app.exec_())