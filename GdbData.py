# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 19:13:18 2020

@author: Samuel Niederer
"""

class GdbData():
    """ This class collects data from a GDB output file.
    """
    def __init__(self, filePath = "log.txt"):
        self._t = None
        self._s = None
        self._h = None
        self.d = dict()
        
        with open(filePath) as f:
            for line in f.readlines():
                start = line.find("{") + 1
                end = line.find("}")
                data = line[start:end].split(", ")
                data = [int(i) for i in data]
                
                self.d.update({line[0]:data})
    
    def getDict(self):
        """ Returns a dictionary with all meassurands.
        """
        return self.d