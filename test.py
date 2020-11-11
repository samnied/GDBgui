# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 13:18:18 2020

@author: Sam
"""

import matplotlib.pyplot as plt
import numpy as np

class Data():
    def __init__(self, fileName):
        self.fileName = fileName
        self.t = list()
        self.s = list() 
        self.h = list()
        self.text = list()
        self.data = list()
        self.bss = list()
        self.dec = list()
        self.hex = list()
        self.arr = list()
        self.run()
        
    def run(self):
        with open(self.fileName) as f:
            self.arr = [self.text, self.data, self.bss, self.dec, self.hex, self.t, self.s, self.h]
            
            for i, line in enumerate(f.readlines()):
                d = line.strip('\n').split(',')
                d.pop(0)
                if i == 4:
                    # interpret as hex
                    self.arr[i].extend([int(i, 16) for i in d])
                else:
                    self.arr[i].extend([int(i) for i in d])
        

# d1 = Data("../logFiles/EHS_07-11-2020_20-22-28.csv")
d1 = Data("../logFiles/EHS_07-11-2020_20-22-28.csv")
d2 = Data("../logFiles/EHS_07-11-2020_20-23-26.csv")

t1 = np.asarray(d1.t)
t2 = np.asarray(d2.t)

# plt.plot(np.arange(len(t1)), t1)
# plt.plot(np.arange(len(t2)), t2)





labels = ['Text', 'Data', 'Bss', 'Dec']
data1 = [d1.text[0], d1.data[0], d1.bss[0], d1.dec[0]] 
data2 = [d2.text[0], d2.data[0], d2.bss[0], d2.dec[0]]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, data1, width, label='Without EH')
rects2 = ax.bar(x + width/2, data2, width, label='With EH')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('[Bytes]')
ax.set_title('Titel')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)

fig.tight_layout()

plt.savefig("meassurement.pdf")
