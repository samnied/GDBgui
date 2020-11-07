# -*- coding: utf-8 -*-
"""
Created on Sat Nov 7 2020

@author: Samuel Niederer
"""
import subprocess

class CodeSize():
    """ This class collects information about the code size of an .elf file.
    """
    def __init__(self, elfPath):
        self._progPath = r"C:\ST\STM32CubeIDE_1.4.0\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.externaltools.gnu-arm-embedded.7-2018-q2-update.win32_1.4.0.202007081208\tools\bin\arm-none-eabi-size.exe"
        self._flags = "--radix=10"
        self._elfPath = elfPath
        
    def getDict(self):
        """ Returns a dictionary wiht all meassurands.
        """
        command = " ".join([self._progPath, self._flags, self._elfPath])
        sb = subprocess.Popen(command, stdout=subprocess.PIPE)
       
        s = list()
        for line in sb.stdout.readlines():
            x = line.decode('utf-8', errors="ignore").split()
            x.pop(-1)
            s.append(x)
            
        x = {key:value for key, value in zip(s[0], s[1])}
        return x