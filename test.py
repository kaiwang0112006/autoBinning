# -*- coding: utf-8 -*-
from autoBinning.utils.forwardSplit import *
from autoBinning.utils.trendSplit import *
from autoBinning.utils.simpleMethods import *
from autoBinning.utils.trendDiscretization import *
from autoBinning.utils.mapa import *

import numpy as np
import pandas as pd


def sampleTest():
    #my_list = [1,1,2,2,2,2,3,3,4,5,6,7,8,9]
    my_list = [1,1,2,2,2,2,3,3,4,5,6,7,8,9,10,10,20,20,20,20,30,30,40,50,60,70,80,90,100]
    my_list_y = [1,1,2,2,2,2,1,1,1,2,2,2,1,1]
    t = simpleMethods(my_list) # [  1.           5.33333333  20.         100.        ]
    t.equalSize(3)
    trans = np.digitize(my_list, t.bins)
    print(t.bins)
    print(trans)
    t.equalValue(4)
    trans = np.digitize(my_list, t.bins)
    print(t.bins)
    print(trans)
    t.equalHist(4)
    trans = np.digitize(my_list, t.bins)
    print(t.bins)
    print(trans)

    
def distest():
    my_list = [1,1,2,2,2,2,3,3,4,5,6,7,8,9,10,10,20,20,20,20,30,30,40,50,60,70,80,90,100]
    my_list_y = [1,1,0,0,0,1,0,0,1,1,1,0,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1]
    t = trendDisMethod(my_list, my_list_y)
    t.fit()
    trans = np.digitize(my_list, t.bins)
    print(t.bins)
    print(trans)   
    
def trend_test_by_data():
    df = pd.read_csv('credit_old.csv')
    df = df[['Age','target']]
    df = df.dropna()

    t = trendDisMethod(df['Age'], df['target'])
    t.fit(trend='down')
    print(df['Age'].describe())
    print(t.bins)
    #print(df['Age'].describe())
 
def forward_woe_test():
    df = pd.read_csv('credit_old.csv')
    df = df[['Age','target']]
    df = df.dropna()

    t = forwardSplit(df['Age'], df['target'])
    t.fit(sby='woe',minv=0.01,init_split=20)
    print(t.bins) # [16. 25. 29. 33. 36. 38. 40. 42. 44. 46. 48. 50. 52. 54. 55. 58. 60. 63. 72. 94.]
    t = forwardSplit(df['Age'], df['target'],missing=16)
    t.fit(sby='woe',num_split=4,init_split=20)
    print(t.bins)
    t = forwardSplit(df['Age'], df['target'])
    t.fit(sby='woe',num_split=4,init_split=20)
    print(t.bins) # [16. 42. 44. 48. 50. 94.]
    print("bin\twoe")
    for i in range(len(t.bins)-1):
        v = t.value[(t.x < t.bins[i+1]) & (t.x >= t.bins[i])]
        woe = t._cal_woe(v)
        print((t.bins[i], t.bins[i+1]),woe)
    # {(16.0, 25.0): 0.11373232830301286, (25.0, 42.0): 0.07217546872710079, (42.0, 50.0): 0.04972042405868509, (50.0, 72.0): -0.07172614369435065, (72.0, 94.0): -0.13778318584223453}

def forward_iv_test():
    df = pd.read_csv('credit_old.csv')
    df = df[['Age','target']]
    df = df.dropna()

    t = forwardSplit(df['Age'], df['target'])
    t.fit(sby='iv',minv=0.1,init_split=20)
    print(t.bins) # [16. 25. 29. 33. 36. 38. 40. 42. 44. 46. 48. 50. 58. 60. 63. 94.]
    t = forwardSplit(df['Age'], df['target'])
    t.fit(sby='iv',num_split=4,init_split=20,min_sample=len(df)*0.2)
    print(t.bins) # [16. 38. 50. 94.]
    t.fit(sby='woeiv',num_split=4,init_split=20)
    print(t.bins) # [16. 25. 33. 36. 38. 94.]
    print("bin\twoe")
    for i in range(len(t.bins)-1):
        v = t.value[(t.x < t.bins[i+1]) & (t.x >= t.bins[i])]
        woe = t._cal_woe(v)
        print((t.bins[i], t.bins[i+1]),woe)

def backward_iv_test():
    df = pd.read_csv('credit_old.csv')
    df = df[['Age','target']]
    df = df.dropna()

    t = backwardSplit(df['Age'], df['target'])
    t.fit(sby='iv',num_split=5)
    print(t.bins) # [16.  17.5 18.5 85.5 95. ]
    woe_dict = {}
    for i in range(len(t.bins)-1):
        v = t.value[(t.x < t.bins[i+1]) & (t.x >= t.bins[i])]
        woe = t._cal_woe(v)
        woe_dict[(t.bins[i], t.bins[i+1])] = woe
    print(woe_dict)

def backward_chi_test():
    df = pd.read_csv('credit_old.csv')
    df = df[['Age','target']]
    df = df.dropna()

    t = backwardSplit(df['Age'], df['target'])
    t.fit(sby='chi',num_split=7)
    print(t.bins) # [16.  72.5 73.5 87.5 89.5 90.5 95. ]
    print("bin\twoe")
    for i in range(len(t.bins)-1):
        v = t.value[(t.x < t.bins[i+1]) & (t.x >= t.bins[i])]
        woe = t._cal_woe(v)
        print((t.bins[i], t.bins[i+1]),woe)
        #woe_dict[(t.bins[i], t.bins[i+1])] = woe

def forward_iv_test2():
    df = pd.read_csv('resolution.csv')
    df = df.dropna()

    t = forwardSplit(df['x'], df['y'],missing=-1)
    t.fit(sby='woeiv',minv=0.1,init_split=0,num_split=4)
    print(t.bins)
    print("bin\twoe")
    for i in range(len(t.bins)-1):
        v = t.value[(t.x < t.bins[i+1]) & (t.x >= t.bins[i])]
        woe = t._cal_woe(v)
        print((t.bins[i], t.bins[i+1]),woe)

def MAPA_test():
    df = pd.read_csv('credit_old.csv')
    df = df[['Age','target']]
    df = df.dropna()

    t = MAPA(df['Age'], df['target'])
    t.fit(trend='up',sby='woe')
    print(t.bins)
    print("bin\twoe")
    for i in range(len(t.bins)-1):
        v = t.value[(t.x < t.bins[i+1]) & (t.x >= t.bins[i])]
        woe = t._cal_woe(v)
        print((t.bins[i], t.bins[i+1]),woe)

def spearman_test():
    df = pd.read_csv('credit_old.csv')
    df = df[['Age','target']]
    df = df.dropna()

    t = backwardSplit(df['Age'], df['target'])
    t.fit_by_spearman(min_v=5, init_split=20)
    print(t.bins)
    print("bin\twoe")
    for i in range(len(t.bins)-1):
        v = t.value[(t.x < t.bins[i+1]) & (t.x >= t.bins[i])]
        woe = t._cal_woe(v)
        print((t.bins[i], t.bins[i+1]),woe)

def main():
    #forward_woe_test()
    #forward_iv_test2()
    #sampleTest()
    #forward_iv_test()
    #backward_chi_test()
    #MAPA_test()
    spearman_test()

if __name__ == "__main__":
    main()