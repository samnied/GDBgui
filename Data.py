# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 19:13:18 2020

@author: Samuel Niederer
"""

class Data():
    def __init__(self, filePath = "log.txt"):
        self.t = None
        self.s = None
        
        with open(filePath) as f:
            for line in f.readlines():
                start = line.find("{") + 1
                end = line.find("}")
                data = line[start:end].split(", ")
                data = [int(i) for i in data]
                
                if line.startswith("t"):
                    self.t = data
                elif line.startswith("s"):
                    self.s = data
                    
    def getStr(self):     
        out = ""
        label1 = "time"
        label2 = "stack"

        l1 = len(str(max(self.t))) + 2
        l2 = len(str(max(self.s))) + 1
        out += f"{label1:>{l1}} {label2:>{l2}}\n"
        out += f'{"":_<{l1 + l2 + 3}}\n'

        for x, y in zip(self.t, self.s):
            out += f"{x:>{l1}} {y:>{l2}}\n"
        
        return out