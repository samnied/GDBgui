# -*- coding: utf-8 -*-
"""
Created on Mon Nov 2 2020

@author: Samuel Niederer
"""
from datetime import datetime

def connect():
    gdb.execute("target remote localhost:61234")
    
gdb.execute("set pagination off")
connect()

addr = None
with open("stackB.txt") as f:
    addr = str(int(f.read(), 16))
    

gdb.execute("load")
gdb.execute("break StackTrace")
gdb.execute("break main.cpp:73")
gdb.execute("continue")

gdb.execute("set variable this.stackB =" + addr)
gdb.execute("continue")

s = gdb.execute("p *0x20001000")

# with open(r'log.txt', mode="w") as f:
#     f.write(data)

# print("gdb-script-finished")
    
# # disconnect properly before quitting
# gdb.execute("detach")   
# gdb.execute("quit")  


    