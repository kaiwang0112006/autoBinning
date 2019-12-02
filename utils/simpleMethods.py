# -*- coding: utf-8 -*-
import numpy as np 
import pandas as pd
import math

class simpleMethods:
    def __init__(self,x):
        self.x = x
        self.range_dict = {}
        
    def equalValue(self,size):
        '''
        x 等间距划分分箱  -> (0-0.1,0.1-0.2...)
        :param size:
        :return:
        '''
        self.range_dict = {}
        self.bins = np.linspace(min(self.x), max(self.x), size+1)

        for i in range(len(self.bins)-1):
            self.range_dict[(self.bins[i],self.bins[i+1])] = i

        return self

    def equalHist(self,size):
        '''
        基于np.histogram分箱
        :param size: bin数目
        :return:
        '''
        self.down = {}
        self.hist, self.bins = np.histogram(self.x, bins=size)


        for i in range(len(self.bins)-1):
            start = self.bins[i]
            end = self.bins[i+1]+1 if i+1==len(self.bins) else self.bins[i+1]

            self.range_dict[(start, end)] = i       

        return self
    
    def equalSize(self,size):
        '''
        每个分箱样本数平均
        self.bins:
        :param size:
        :return:
        '''
        self.range_dict = {}
        _, self.bins = pd.qcut(self.x,size,retbins='True',duplicates='drop')

        self.bins = sorted(list(self.bins))

        for i in range(len(self.bins)-1):
            start = self.bins[i]
            end = self.bins[i+1]+1 if i+1==len(self.bins) else self.bins[i+1]

            self.range_dict[(start, end)] = i       

        self.bins = np.array(self.bins)
        return self

    def everysplit(self):
        '''
        最细粒度切分
        :return:
        '''
        if type(list(self.x)[0]) == type(1):
            self.bins = np.array(list(self.x))
        else:
            bins = []
            x_sort = sorted(self.x,reverse=False)
            bins = [x_sort[0]]
            for i in range(len(x_sort)-1):
                bins.append((x_sort[i]+x_sort[i+1])/2)
            bins.append(x_sort[-1]+1)
            self.bins = np.array(bins)

        self.range_dict = {}
        for i in range(len(self.bins)-1):
            start = self.bins[i]
            end = self.bins[i+1]+1 if i+1==len(self.bins) else self.bins[i+1]

            self.range_dict[(start, end)] = i


    def _cal_woe(self,v,bad=1):
        '''
        计算woe
        :param v:
        :param bad:
        :return:
        '''
        bad_num = len(v[v == bad])
        count_num = len(v)

        if count_num-bad_num == 0 or self.allgood==0:
            woe = 0
        else:
            woe = math.log((bad_num / (count_num - bad_num)) / (self.allbad / self.allgood))
        return woe

    def _cal_iv(self, v, bad=1):
        '''
        计算iv
        :param v:
        :param bad:
        :return:
        '''
        bad_num = len(v[v == bad])
        count_num = len(v)

        if count_num-bad_num == 0 or self.allgood==0:
            iv = 0
        else:
            iv = (bad_num / (count_num - bad_num))*math.log((bad_num / (count_num - bad_num)) / (self.allbad / self.allgood))
        return iv