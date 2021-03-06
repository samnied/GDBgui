# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 12:40:53 2020

Generate code from Qt designer with following commands
pyuic5 –x "filename".ui –o "filename".py
pyuic5 –x QTdesign.ui –o QTdesign.py

@author: Samuel Niederer
"""
import sys
import os
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import *

from QTdesign import Ui_MainWindow
from StackInfo import StackInfo
from GDB import GDBThread
from Stlink import StThread
from Format import Format

#adjust for high dpi screen
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
     
class Ui_MainWindowUser(Ui_MainWindow):
    """ This class holds all GUI elements.
    """
    def __init__(self, MainWindow):
        """ Initializes the main window.
        """
        self.setupUi(MainWindow)
        
        self.gdbOutput.ensureCursorVisible()
        self.gdbOutput.centerOnScroll()
        
        # connect signals and slots
        app.aboutToQuit.connect(self.closeEvent)
        self.btnRun.clicked.connect(self.runMeasurement)
        self.btnSearchElfPath.clicked.connect(self.selectElf)
        self.btnSearchSavePath.clicked.connect(self.selectLog)
        
        # set default value for path
        settings = QSettings("OST-HSR", "GDBgui")
        elfPath = settings.value("LAST_ELF_PATH", "")
        self.elfPathEdit.setText(elfPath)
        savePath = settings.value("LAST_LOG_PATH", "")
        self.savePathEdit.setText(savePath)
        
        self.stThread = StThread()
        self.stThread.msg.connect(self.stlinkLog)
        self.stThread.progress.connect(self.progress)
        
        self.gdbThread = GDBThread()
        self.gdbThread.msg.connect(self.gdbLog)
        self.gdbThread.finished.connect(self.gdbFinished)
        self.gdbThread.progress.connect(self.progress)
        
        self.progressBar.setValue(0)
        
    def selectElf(self):
        settings = QSettings("OST-HSR", "GDBgui")
        lastPath = settings.value("LAST_ELF_PATH", "")
        
        if not os.path.exists(lastPath):
            lastPath = ""
        
        fileName = QtWidgets.QFileDialog.getOpenFileName(None, "Select file", lastPath)[0]
        if fileName:
            self.elfPathEdit.setText(fileName)
            # save path to settings, as raw string
            settings.setValue("LAST_ELF_PATH", fr"{fileName}")
    
    def selectLog(self):
        settings = QSettings("OST-HSR", "GDBgui")
        lastPath = settings.value("LAST_LOG_PATH", "")
        
        if not os.path.exists(lastPath):
            lastPath = ""
        fileName = QFileDialog.getExistingDirectory(None, 
                                                  'Select directory', 
                                                  lastPath, 
                                                  QFileDialog.ShowDirsOnly)
        if fileName:
            self.savePathEdit.setText(fileName)
             # save path to settings, as raw string
            settings.setValue("LAST_LOG_PATH", fr"{fileName}")
    
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
            self.gdbOutput.appendPlainText(msg)
    
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
        
    def progress(self, percent):
        """ Updates the progress bar.
        """
        self.progressBar.setValue(percent)
        
    def gdbFinished(self, log):
        """ Saves data to file.
        """
        if log == "ok":
            d = Format(self.elfPathEdit.text(), self.commentEdit.toPlainText())
            self.measureLog(d.getProtocol())
            d.saveTxt(self.savePathEdit.text())
            d.saveCsv(self.savePathEdit.text())
            
            self.progress(100)
        if log == "error":
            self.measureLog("an error occured, no measureoutput")
        
    def runMeasurement(self):
        """ Runs a measurement.
        """
        self.progress(0)
        
        # clear all text ouputs
        self.stlinkLog("clear")
        self.gdbLog("clear")
        self.measureLog("clear")
        
        # run gdb objdump and save resut to .txt
        # StackInfo.run(self.elfPathEdit.text())         
    
        # check if there is allready an stlink sever running
        if self.stThread.isRunning():
            self.stThread.getProcess().terminate()
            self.stThread.terminate()
        self.stThread.start()
        
        # check if there is allready a GDB server running
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