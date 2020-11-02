# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 13:54:17 2020

@author: Samuel Niederer
"""
import os
class Size():
    progPath = r"C:\ST\STM32CubeIDE_1.4.0\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.externaltools.gnu-arm-embedded.7-2018-q2-update.win32_1.4.0.202007081208\tools\bin\arm-none-eabi-size.exe"
    flags = "--radix=10"
    
    def getDict(filePath):
        command = " ".join([Size.progPath, Size.flags, filePath])
        stream = os.popen(command)
        
        s = list()
        for line in stream.readlines():
            x = line.split()
            x.pop(-1)
            s.append(x)
            
        x = {key:value for key, value in zip(s[0], s[1])}
        return x

    def getStr(filePath):
        x = Size.getDict(filePath)
        length = 8

        for i in x.values():
            if(len(i) > length):
                length = len(i) + 3
        
        s = "".join(f"{k:>{length}}" for k in x.keys()) + "\n"
        s += "".join(f"{v:>{length}}" for v in x.values()) + "\n"
        
        return s
