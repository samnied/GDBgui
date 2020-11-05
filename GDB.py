# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 11:38:46 2020

@author: Samuel Niederer
"""
import subprocess
from PyQt5.QtCore import *

class GDBThread(QThread):
    """ This class works as an interface for the GDB server.
    """
    # signals to communicare betwween other threads   
    msg = pyqtSignal(str)
    finished = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self):
        """ Initializes the object.
        """
        super(GDBThread, self).__init__()
        self.gdbPath = r'C:\ST\STM32CubeIDE_1.4.0\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.externaltools.gnu-arm-embedded.7-2018-q2-update.win32_1.4.0.202007081208\tools\bin\arm-none-eabi-gdb-py.exe'
        self.gdbScript = r'-x GDB-gdb-script.gdb'
        self.elfPath = ""
        
    def getProcess(self):
        """ Returns the suprocess which holds the GDB server.
        """
        return self.process
    
    def setElfPath(self, path):
        """ Set the path where the .elf file is stored.
        """
        self.elfPath = path
        
    def run(self):
        """ Starts the GDB-server.
        """
        self.msg.emit("Run GDB-Server...")
        self.progress.emit(55)
        
        openGDB = " ".join([self.gdbPath, self.gdbScript])
        x = subprocess.Popen(openGDB + " " + self.elfPath, stdout=subprocess.PIPE)
        self.process = x
        
        while True:
            # read consol output form GDB server
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