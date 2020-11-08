# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 14:33:31 2020

@author: Sam
"""
from datetime import datetime
import textwrap
from CodeSize import CodeSize
from GdbData import GdbData

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
        """ Returns the projecttitel of the .elf file.
        """
        sep = "/"
        if("\\" in self._elfPath):
            sep = "\\"
        return self._elfPath.split(sep)[-1].split(".")[0]
    
    def getCsInfo(self):
        """ Returns formatted code size information.
        """
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
        """ Returns formatted meassurement data.
        """
        d = GdbData()
        data = d.getDict()
        
        label1 = "Time"
        label2 = "StackSize"
        label3 = "HeapSize"
        
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
        
        # calculate max data string length
        dL3 = list()
        for elem in data['s']:
            dL3.append(len(str(elem)))
        dL3 = max(dL3) + 5
        dL3 = max(dL3, len(label3))

        subTitle = "GDB Measurement:\n"
        s = subTitle
        s += f"{'':-<{len(subTitle)}}\n\n"
        
        s += f"{label1:<{dL1}}  | {label2:<{dL2}} | {label3:<{dL3}}\n"
        s += f"{'':-<{dL1 + dL2 + dL3 + 7}}\n"
        for time, sSize, hSize in zip(data['t'], data['s'], data['h']):
            s += f"{time:>{dL1}}  |{sSize:>{dL2}}  |{hSize:>{dL3}}\n" 
        return s
        

    def getProtocol(self):       
        """ Returns a measurement protocol.
        """
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
        
    def saveTxt(self, savePath):
        """ Saves protocol as .txt file.
        """
        fileName = self.getTitle()
        fileName += "_" + datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + ".txt"
        with open(savePath + "\\" + fileName,  mode="w") as f:
            f.write(self.getProtocol())
            
    def saveCsv(self, savePath):
        s = ""
        d = GdbData()
        cs = CodeSize(self._elfPath)
        data = cs.getDict()
        
        for k in data.keys():
            s += f"{k},{data[k]}\n"
        
        data = d.getDict()
        for k in data.keys():
            s += k + ','
            s += ','.join([str(i) for i in data[k]]) + "\n"
        
        fileName = self.getTitle()
        fileName += "_" + datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + ".csv"
        with open(savePath + "\\" + fileName,  mode="w") as f:
            f.write(s)

if __name__ == "__main__":           
    f = Format(r"C:\Users\samue\STM32CubeIDE\workspace_1.4.0\EHS\Debug\EHS.elf", "")
    print(f.getProtocol())
    f.saveCsv("../logFiles")