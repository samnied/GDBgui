# -*- coding: utf-8 -*-
"""
Created on Mon Nov 2 2020

@author: Samuel Niederer
"""

def connect():
    gdb.execute("target remote localhost:61234")
    
gdb.execute("set pagination off")
connect()
gdb.execute("load")
gdb.execute("break end")
gdb.execute("continue")

data = "t" + gdb.execute("p *this.tBuff@this.tIndex", to_string=True)
data += "s" + gdb.execute("p *this.sBuff@this.sIndex", to_string=True)

with open(r'log.txt', mode="w") as f:
    f.write(data)

print("gdb-script-finished")
    
# disconnect properly before quitting
gdb.execute("detach")   
gdb.execute("quit")  


    