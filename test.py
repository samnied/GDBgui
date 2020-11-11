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
        

if __name__ == "__main__":
    # read data from cs file
    logFolderPath = r"C:/Users/Sam/OneDrive/SA_pers"
    d1 = Data(logFolderPath + "/logFiles/EHS_07-11-2020_20-22-28.csv")
    d2 = Data(logFolderPath + "/logFiles/EHS_07-11-2020_20-23-26.csv")
    
    # coinvert exectuion time to kilo cycles
    t1 = np.asarray(d1.t)/1000
    t2 = np.asarray(d2.t)/1000
    
    fig, ax = plt.subplots(3)
    fig.suptitle('Title')
    
    ax[0].plot(np.arange(len(t1)), t1, 'r', label="Without Exception Handling")
    ax[1].plot(np.arange(len(t1)), t2, 'g', label="With Exception Handling")
    
    ax[2].plot(np.arange(len(t1)), t1, 'r', label="Without Exception Handling")
    ax[2].plot(np.arange(len(t1)), t2, 'g', label="With Exception Handling")
    
#    # visualize start and stop of toggled signal s1
#    ax[1].plot([t[t1], t[t1]], [0, 2], "k:")
#    ax[1].plot([t[t2], t[t2]], [0, 2], "k:")
#    # ax[1].text(0.2,1.6,'$n_1$', fontsize=12)
#    # ax[1].text(t[t2]-0.7, 1.6,'$n_2$', fontsize=12)
#    ax[1].annotate(s='', xy=(0,1.2), xytext=(t[t2],1.2), arrowprops=dict(arrowstyle='<->'))
#    ax[1].text(2.9, 1.3,'$n_{offset} = 35 cycles$', fontsize=12)
#    
#    print(t[t2])
#    
#    ax[0].annotate(s='', xy=(0, 0.4), xytext=(t[t2], 0.4), arrowprops=dict(arrowstyle='<->'))
#    ax[0].text(3, 0.5,'$t_{offset} = 8.72 \mu s$', fontsize=12)
#    # ax[0].text(0, 1.1,'$t_1$', fontsize=15)
#    # ax[0].text(t[t2]-0.5, 1.1, '$t_2$', fontsize=15)
    
    ax[0].legend(loc="upper center")
    ax[1].legend(loc="upper center")
    
    ax[1].set_xlabel(r'Number of nested calls')
    ax[0].set_ylabel('Execution time [kilo cycles]')
    ax[1].set_ylabel('Execution time [kilo cycles]')
    
    plt.savefig("timeComparison.pdf")
    
   
    # plt.plot(np.arange(len(t1)), t1)
    # plt.plot(np.arange(len(t2)), t2)
    
    
#    # make code size plot
#    labels = ['Text', 'Data', 'Bss', 'Dec']
#    data1 = [d1.text[0], d1.data[0], d1.bss[0], d1.dec[0]] 
#    data2 = [d2.text[0], d2.data[0], d2.bss[0], d2.dec[0]]
#    
#    x = np.arange(len(labels))  # the label locations
#    width = 0.35  # the width of the bars
#    
#    fig, ax = plt.subplots()
#    rects1 = ax.bar(x - width/2, data1, width, label='Without EH')
#    rects2 = ax.bar(x + width/2, data2, width, label='With EH')
#    
#    # Add some text for labels, title and custom x-axis tick labels, etc.
#    ax.set_ylabel('[Bytes]')
#    ax.set_title('Titel')
#    ax.set_xticks(x)
#    ax.set_xticklabels(labels)
#    ax.legend()
#    
#    
#    def autolabel(rects):
#        """Attach a text label above each bar in *rects*, displaying its height."""
#        for rect in rects:
#            height = rect.get_height()
#            ax.annotate('{}'.format(height),
#                        xy=(rect.get_x() + rect.get_width() / 2, height),
#                        xytext=(0, 3),  # 3 points vertical offset
#                        textcoords="offset points",
#                        ha='center', va='bottom')
#    
#    
#    autolabel(rects1)
#    autolabel(rects2)
#    
#    fig.tight_layout()
#    
#    plt.savefig("meassurement.pdf")
