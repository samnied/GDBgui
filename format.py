# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 14:33:31 2020

@author: Sam
"""
from datetime import datetime
import textwrap
from CodeSize import CodeSize
from GdbData import GdbData

# todo read this info from csv
# todo adjust gdb-py-script to directly creat csv file

class Format():
    
    """ This class formats the data.
    """
    def __init__(self, elfPath, comment):
        #pageWidth
        self._pw = 50
        
        self._elfPath = elfPath
        self._title = self.getTitle()
        self.comment = comment
        
    @property
    def comment(self):
        return self._comment
    
    @comment.setter
    def comment(self, val):
        subTitle = "Comment:\n"
        s = subTitle
        s += f"{'':-<{len(subTitle)}}\n"
        # fit comment to page widht
        s += textwrap.fill(val, self._pw) + "\n" 
        s += f"{'':=^{self._pw}}\n"
        
        self._comment = s   
        
    def getTitle(self):
        sep = "/"
        if("\\" in self._elfPath):
            sep = "\\"
        return self._elfPath.split(sep)[-1].split(".")[0]
        
    def saveTxt(self, savePath):
        fileName = self.getTitle()
        fileName += "_" + datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + ".txt"
        with open(savePath + "\\" + fileName,  mode="w") as f:
            f.write(self.getStr())
    
    def getCsInfo(self):
        cs = CodeSize(self._elfPath)
        data = cs.getDict()
      
        # calculate max data string length
        dL = list()
        for elem in data.values():
            dL.append(len(str(elem)))
        dL = max(dL) + 5
        
        subTitle = "Code size information:\n"
        s = subTitle
        s += f"{'':-<{len(subTitle)}}\n"
        
        for k, v in data.items():
            s += f"{k:<5}{v:>{dL}} [bytes]\n"
        s += f"{'':=^{self._pw}}\n"
        return s
    
    def getMeasurement(self):
        d = GdbData()
        data = d.getDict()
        
        label1 = "Time"
        label2 = "StackSize"
        
        # calculate max data string length
        dL1 = list()
        for elem in data['t']:
            dL1.append(len(str(elem)))
        dL1 = max(dL1) + 3
        dL1 = max(dL1, len(label1) + 3)

        # calculate max data string length
        dL2 = list()
        for elem in data['s']:
            dL2.append(len(str(elem)))
        dL2 = max(dL2) + 5
        dL2 = max(dL2, len(label2))


        subTitle = "GDB Measurement:\n"
        s = subTitle
        s += f"{'':-<{len(subTitle)}}\n\n"
        
        s += f"{label1:<{dL1}}  | {label2:<{dL2}}\n"
        s += f"{'':-<{dL1 + dL2 + 4}}\n"
        for time, size in zip(data['t'], data['s']):
            s += f"{time:>{dL1}}  |{size:>{dL2}}\n"
            
        return s
        

    def getStr(self):       
        #header
        s = ""
        s += f"{'':=^{self._pw}}\n"
        s += f"Project:     {self._title}\n"
        s += f"{'':=^{self._pw}}\n"
        
        #comment
        s += self.comment
        
        # code size info
        s += self.getCsInfo()
        
        # measurement
        s += self.getMeasurement()
        
        return s