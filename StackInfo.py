# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 13:18:18 2020

@author: Samuel Niederer
"""

import subprocess

class StackInfo():
    """ This calss works as an interface to the objdump application.
    """
    def run(elfPath):
        """ Runs the objdump application.
        """
        progPath = r"C:\ST\STM32CubeIDE_1.4.0\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.externaltools.gnu-arm-embedded.7-2018-q2-update.win32_1.4.0.202007081208\tools\bin\arm-none-eabi-objdump.exe"
        flags = "-t"
        cmdStr = " ".join([progPath, flags, elfPath])
        stackBpath = "stackB.txt"
        
        sb = subprocess.Popen(cmdStr, stdout=subprocess.PIPE)
        
        found = False
        for line in sb.stdout.readlines():
            line = line.decode('utf-8', errors="ignore")
            if "_user_heap_stack" in line:
                with open(stackBpath, mode="w") as f:
                    f.write(line.split()[0])
                found = True
            if found:
                break