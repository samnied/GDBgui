# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 14:58:44 2020

@author: Sam
"""

class GDBinfo():
    
    stlinkPath = r'C:\ST\STM32CubeIDE_1.4.0\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.externaltools.stlink-gdb-server.win32_1.4.0.202007081208\tools\bin'
    cubeProgPath = r'C:\ST\STM32CubeIDE_1.4.0\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.externaltools.cubeprogrammer.win32_1.4.0.202007081208\tools\bin'
    openStlink = stlinkPath + "\ST-LINK_gdbserver.exe" + " " + "-v -p 61234 -d -cp" + " " + cubeProgPath 
    
    gdbPath = r'C:\ST\STM32CubeIDE_1.4.0\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.externaltools.gnu-arm-embedded.7-2018-q2-update.win32_1.4.0.202007081208\tools\bin\arm-none-eabi-gdb-py.exe'
    gdbScript = r'-x GDB-gdb-script.gdb'
    openGDB = " ".join([gdbPath, gdbScript])
    