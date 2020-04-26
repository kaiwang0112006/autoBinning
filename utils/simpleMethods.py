# -*- coding: utf-8 -*-
import numpy as np 
import pandas as pd
import math
import copy

class simpleMethods:
    def __init__(self,x, missing=None,force=False):
        self.x_org = x
        self.range_dict = {}
        self.missing=missing
        if self.missing == None:
            self.x = copy.deepcopy(self.x_org)
            self.x_miss = None
        else:
            self.x = self.x_org[self.x_org!=self.missing]
            self.x_miss = self.x_org[self.x_org==self.missing]
        self.force=force
        
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
            end = self.bins[i+1]

            self.range_dict[(start, end)] = i       

        return self
    
    def equalSize(self,size):
        '''
        每个分箱样本数平均
        :param size:
        :return:
        '''
        self.range_dict = {}
        # use pandas qcut
        #_, self.bins = pd.qcut(self.x,size,retbins='True',duplicates='drop')
        #self.bins = sorted(list(self.bins))
        # use numpy instead
        breakpoints = np.arange(0, size + 1) / (size) * 100
        self.bins = [np.percentile(self.x, b) for b in breakpoints]

        for i in range(len(self.bins)-1):
            start = self.bins[i]
            end = self.bins[i+1]

            self.range_dict[(start, end)] = i       

        self.bins = np.array(self.bins)
        return self

    def everysplit(self):
        '''
        最细粒度切分
        :return:
        '''
        if len(set(self.x))<=10 and not self.force:
            self.bins = np.array(list(self.x))
        else:
            x_sort = sorted(list(set(self.x)),reverse=False)
            bins = [x_sort[0]]
            for i in range(len(x_sort)-1):
                bins.append((x_sort[i]+x_sort[i+1])/2)
            bins.append(x_sort[-1]+1)
            self.bins = np.array(bins)

        self.range_dict = {}
        for i in range(len(self.bins)-1):
            start = self.bins[i]
            end = self.bins[i+1]

            self.range_dict[(start, end)] = i