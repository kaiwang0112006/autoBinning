# -*- coding: utf-8 -*-

from utils.simpleMethods import *
from utils.trendDiscretization import *
from utils.trendSplit import *
from utils.splitBywoe import *
from utils.splitByiv import *
import numpy as np
import pandas as pd

def sampleTest():
    #my_list = [1,1,2,2,2,2,3,3,4,5,6,7,8,9]
    my_list = [1,1,2,2,2,2,3,3,4,5,6,7,8,9,10,10,20,20,20,20,30,30,40,50,60,70,80,90,100]
    my_list_y = [1,1,2,2,2,2,1,1,1,2,2,2,1,1]
    t = simpleMethods(my_list)
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
 
def woe_test_by_data():
    df = pd.read_csv('credit_old.csv')
    df = df[['Age','target']]
    df = df.dropna()

    t = splitBywoe(df['Age'], df['target'])
    t.fit(trend='up',init_split=20,minwoe=0.01)
    #print(df['Age'].describe())
    print(t.bins)
    t = trendSplit(df['Age'], df['target'])
    t.fit(sby='woe',minv=0.01,init_split=20,trend='up')
    print(t.bins)
    t = trendSplit(df['Age'], df['target'])
    t.fit(sby='woe',num_split=4,init_split=20,trend='up')
    print(t.bins)
    #trans = np.digitize(df['Age'], t.bins)
    #print(list(trans))
    #print(df['Age'])

def iv_test_by_data():
    df = pd.read_csv('credit_old.csv')
    df = df[['Age','target']]
    df = df.dropna()

    t = splitByiv(df['Age'], df['target'])
    t.fit(miniv=0.1)
    print(t.bins) # [16.  18.5 82.5 83.5 84.5 85.5 86.5 95. ]
    t = trendSplit(df['Age'], df['target'])
    t.fit(sby='iv',minv=0.1)
    print(t.bins) # [16.  18.5 82.5 83.5 84.5 85.5 86.5 95. ]
    t = trendSplit(df['Age'], df['target'])
    t.fit(sby='iv',minv=0.1,init_split=20)
    print(t.bins) # [16. 25. 29. 33. 36. 38. 40. 42. 46. 48. 50. 94.]
    t = trendSplit(df['Age'], df['target'])
    t.fit(sby='iv',num_split=4,init_split=20)
    print(t.bins) # [16. 25. 29. 33. 42. 94.]

def main():
    #woe_test_by_data()
    #sampleTest()
    iv_test_by_data()

if __name__ == "__main__":
    main()