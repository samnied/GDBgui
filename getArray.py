# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 18:34:12 2020

@author: Samuel Niederer
"""
from datetime import datetime

# Header
progName = "Nested Functions"
dateStr = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

print(dateStr)
print("GDB Measuremnt of program: " + progName)
print()

# data = "$1 = {26, 52, 78, 104, 130, 156, 234, 208, 234, 260, 286, 312, 338, 364, 442, 416, 442, 468, 494, 520}"
data = ""
with open("log.txt") as f:
    data = f.read()
    
start = data.find("{") + 1
end = data.find("}")
data = data[start:end].split(", ")
data = [int(i) for i in data]


data_2 = [i for i in range(len(data))]

label1 = "time"
label2 = "size"

l1 = len(str(max(data))) + 1
l2 = len(str(max(data_2))) + 1
print(f"{'time':>{l1}} {'size':>{l2}}")

for x, y in zip(data, data_2):
    print(f"{x:>{l1}} {y:>{l2}}")

 
