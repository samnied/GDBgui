# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 13:18:18 2020

@author: Sam
"""

import numpy as np

class Data():
    def __init__(self, fileName):
        self.fileName = fileName
        self.t = list()
        self.s = list 
        self.text = -1
        self.data = -1
        self.bss = -1
        self.dec = -1
        self.code = -1
        self.data = list()
        
    def run(self):
        with open(self.fileName) as f:
            self.data = [self.text, self.data, self.bss, self.dec, self.code, self.t, self.s]
            
            for i, line in enumerate(f.readlines()):
                d = line.strip('\n').split(',')
                d.pop(0)
                self.data[i] = [int(i) for i in d]
        

d = Data("test.csv")
d.run()
for i in d.data:
    print(i)