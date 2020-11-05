# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 11:46:12 2020

@author: Sam
"""

import subprocess
from PyQt5.QtCore import *

class StThread(QThread):
    """ This class works as an interface for the Stlink server.
    """
    # signals to communicare betwween other threads      
    msg = pyqtSignal(str)
    progress = pyqtSignal(int)

    def __init__(self):
        """ Initializes the object.
        """
        super(StThread, self).__init__()
        self.stlinkPath = r'C:\ST\STM32CubeIDE_1.4.0\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.externaltools.stlink-gdb-server.win32_1.4.0.202007081208\tools\bin'
        self.cubeProgPath = r'C:\ST\STM32CubeIDE_1.4.0\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.externaltools.cubeprogrammer.win32_1.4.0.202007081208\tools\bin'

    def getProcess(self):
        """ Returns the suprocess which holds the Stkink server.
        """
        return self.process
    
    def run(self):
        """ Starts the Stlink server.
        """
        self.msg.emit("Try to connect to stlink...")
        
        openStlink = self.stlinkPath + "\ST-LINK_gdbserver.exe"  
        openStlink += " " + "-v -p 61234 -d -cp" + " " + self.cubeProgPath 
                    
        x = subprocess.Popen(openStlink, stdout=subprocess.PIPE)
        self.process = x
        
        while True:
            # read consol output form Stlink server
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