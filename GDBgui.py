# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 12:40:53 2020
generate code from Qt designer with following command
pyuic5 –x "filename".ui –o "filename".py
pyuic5 –x QTdesign.ui –o QTdesign.py

@author: Samuel Niederer
"""
import time
import sys
import subprocess
import threading
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import *

from QTdesign import Ui_MainWindow
from GDBinfo import GDBinfo
from Size import Size
from Data import Data
from StackInfo import StackInfo

#adjust for high dpi screen
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


class StThread(QThread):
    # class used to start stlink server from consol
       
    msg = pyqtSignal(str)
    progress = pyqtSignal(int)

    def __init__(self):
        super(StThread, self).__init__()

    def getProcess(self):
        return self.process
    
    def run(self):
        self.msg.emit("Try to connect to stlink...")
      
        x = subprocess.Popen(GDBinfo.openStlink, stdout=subprocess.PIPE)
        self.process = x
        
        while True:
            # read consol output form stlink server
            s = x.stdout.readline().decode('utf-8', errors="ignore")
            
            if "ST-LINK device initialization OK" in s:
                self.msg.emit(s)
                self.progress.emit(30)
            elif "Accepted connection" in s:
               self.msg.emit(s)
            elif "error" in s:
                self.msg.emit(s)
                break
            elif "stlink shut down\n" in s:
                self.msg.emit(s)
                break

class GDBThread(QThread):
    # class used to start stlink server from consol
       
    msg = pyqtSignal(str)
    finished = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self):
        super(GDBThread, self).__init__()
        self.elfPath = ""
        
    def getProcess(self):
        return self.process
    
    def setElfPath(self, path):
        self.elfPath = path
        
    def run(self):
        self.msg.emit("Run GDB-Server...")
        self.progress.emit(55)
        
        x = subprocess.Popen(GDBinfo.openGDB + " " + self.elfPath, stdout=subprocess.PIPE)
        self.process = x
        
        while True:
            # read consol output form stlink server
            s = x.stdout.readline().decode('utf-8', errors="ignore")
            
            if "gdb-script-finished" in s:
                self.msg.emit(s)
                self.progress.emit(75)
                self.finished.emit("ok")
                break
            elif "gdb.error" in s:
               self.msg.emit(s)
            elif "error" in s:
                self.msg.emit(s)
                break
            elif "gdb-script-error" in s:
                self.msg.emit(s)
                self.finished.emit("error")
                break
            self.msg.emit(s)
        
    
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
        savePath = "..\logFiles"
        self.savePathEdit.setText(savePath)
        
        self.threads = list()
        
        
        self.stThread = StThread()
        self.stThread.msg.connect(self.stlinkLog)
        self.stThread.progress.connect(self.progress)
        
        self.gdbThread = GDBThread()
        self.gdbThread.msg.connect(self.gdbLog)
        self.gdbThread.finished.connect(self.gdbFinished)
        self.gdbThread.progress.connect(self.progress)
        
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
            
    
    def gdbFinished(self, log):
        if log == "ok":
            d = Data()
            self.measureLog(d.getStr())
            self.saveFile(self.textOutput.toPlainText())
            self.progress(100)
        if log == "error":
            self.measureLog("an error occured, no measureoutput")
           
        
    def getSizeInfo(self):
        filePath = self.elfPathEdit.text()
        return Size.getStr(filePath)
    
    
    def closeEvent(self):
        self.stThread.getProcess().terminate()
        self.stThread.terminate()
         
        print("wait for wait for threads to be finished")
        for t in self.threads:
            t.join()
        print("shut down GDBgui ...")
    
    def stlinkLog(self, msg):
        if msg == "clear":
            self.stlinkOutput.clear()
        else:
            # print msg to console
            print(msg)
            # print msg to gui text element
            if(not "\n" in msg):
                msg += "\n"
            self.stlinkOutput.insertPlainText(msg)
    
    def gdbLog(self, msg):
        if msg == "clear":
            self.gdbOutput.clear()
        else:
            # print msg to console
            print(msg)
            # print msg to gui text element
            if(not "\n" in msg):
                msg += "\n"
            self.gdbOutput.insertPlainText(msg)
    
    def measureLog(self, msg):
        if msg == "clear":
            self.textOutput.clear()
        else:
            # print msg to console
            print(msg)
            # print msg to gui text element
            if(not "\n" in msg):
                msg += "\n"
            self.textOutput.insertPlainText(msg)
            

    def saveFile(self, data):
        savePath = self.savePathEdit.text()
        filePath = self.elfPathEdit.text()
        
        sep = "/"
        if("\\" in filePath):
            sep = "\\"
            
        fileName = filePath.split(sep)[-1].split(".")[0]
        fileName += "_" + datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + ".txt"
       
        with open(savePath + "\\" + fileName,  mode="w") as f:
            comment = self.commentEdit.text()
            data = comment + "\n\n" + data 
            f.write(data)
       
    def progress(self, percent):
        self.progressBar.setValue(percent)
        
    def runMeasurement(self):
        self.progress(0)
        
        self.stlinkLog("clear")
        self.gdbLog("clear")
        self.measureLog("clear")
        
        # run gdb objdump and save resut to .txt
        StackInfo.run(self.elfPathEdit.text())
        # print code size information
        self.measureLog(self.getSizeInfo())
          
    
        # check if there is allready an stlink sever running
        if self.stThread.isRunning():
            self.stThread.getProcess().terminate()
            self.stThread.terminate()
        self.stThread.start()
        
         # check if there is allready an GDB server running
        if self.gdbThread.isRunning():
            self.gdbThread.getProcess().terminate()
            self.gdbThread.terminate()
        self.gdbThread.setElfPath(self.elfPathEdit.text())
        self.gdbThread.start() 
        
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindowUser(MainWindow)
    
    MainWindow.show()
    sys.exit(app.exec_())