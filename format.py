# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 14:33:31 2020

@author: Sam
"""

# todo read this info from csv
# todo adjust gdb-py-script to directly creat csv file

titel = "EHS Measurement Time Date"
comment = "Test comment\nWith several\nlines blablabla c++program with exception handling"
stackData = ""

x = 10
y = 200
z = 3000

l = 50
l1 = max(10, max(len(x), len(y), len(z)))

s = f"{titel:^{l}}\n"
s += f"{'':=^{l}}\n"
s += comment + "\n"
s += f"{'':=^{l}}\n"

for i in [x, y, z]:
    s += f"Text{i:>{l1}} [bytes]\n"
s += f"{'':=^{l}}\n"


print(s)