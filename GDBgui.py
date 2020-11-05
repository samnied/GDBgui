# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 12:40:53 2020
generate code from Qt designer with following command
pyuic5 –x "filename".ui –o "filename".py
pyuic5 –x QTdesign.ui –o QTdesign.py

@author: Samuel Niederer
"""
import sys
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import *

from QTdesign import Ui_MainWindow
from Size import Size
from Data import Data
from StackInfo import StackInfo
from GDB import GDBThread
from Stlink import StThread

#adjust for high dpi screen
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
     
    
class Ui_MainWindowUser(Ui_MainWindow):
    """ This class holds all GUI elements.
    """
    def __init__(self, MainWindow):
        """ Initializes the main window.
        """
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
        """ Cleans up everything when the main window gets closed.
        """
        self.stThread.getProcess().terminate()
        self.stThread.terminate()
        
        self.gdbThread.getProcess().terminate()
        self.gdbThread.terminate()
    
    
    def stlinkLog(self, msg):
        """ Updates the stlink output window.
        """
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
        """ Updates the gdb output window.
        """
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
        """ Updates the measurement output windwow.
        """
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
        """ Saves data to a text file.
        """
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
        """ Updates the progress bar.
        """
        self.progressBar.setValue(percent)
        
        
    def runMeasurement(self):
        """ Runs a measurement.
        """
        
        self.progress(0)
        
        # clear all text ouputs
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