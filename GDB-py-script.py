# -*- coding: utf-8 -*-
"""
Created on Mon Nov 2 2020

@author: Samuel Niederer
"""
from datetime import datetime

def connect():
    try:
        gdb.execute("target remote localhost:61234")
    except Exception as e:
        print("gdb-script-error, {s}")
        gdb.execute("quit")  

    
gdb.execute("set pagination off")
gdb.execute("set print repeats 0")
connect()

gdb.execute("load")
gdb.execute("monitor reset")

gdb.execute("break GDBlog::end")
gdb.execute("continue")

data = "t" + gdb.execute("p *this.tBuff@this.tIndex", to_string=True)
data += "s" + gdb.execute("p *this.sBuff@this.sIndex", to_string=True)
data += "h" + gdb.execute("p *this.hBuff@this.hIndex", to_string=True)

with open(r'log.txt', mode="w") as f:
    f.write(data)

print("gdb-script-finished")
    
# disconnect properly before quitting
gdb.execute("detach")   
gdb.execute("quit")  


    