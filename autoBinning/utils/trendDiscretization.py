# -*- coding: utf-8 -*-
from .simpleMethods import *
import numpy as np
import copy 

class trendDisMethod(simpleMethods):
    def __init__(self,x,y):
        simpleMethods.__init__(self,x) 
        self.y = y
        self.cut_range = []
        
    def __stat(self,bad=1):
        '''
        统计数据集各个区间的坏样本比例
        :param bad:
        :return:
        '''
        n = 20 if len(self.x)>=10 else len(self.x)
        self.equalSize(n)
        self.value = np.array(self.y)
        #self.x_array = np.array(self.x)
        self.range_table = {}
        self.down = []
        self.bad_list = []
        self.count_list = []
        #print(self.range_dict)
        #print('for')
        for r in self.range_dict:
            range_value = self.value[(self.x<r[1]) & (self.x>=r[0])]
            bad_num = len(range_value[range_value==bad])
            count_num = len(range_value)
            if count_num == 0:
                rate = 0
            else:
                rate = bad_num/count_num
            
            self.range_table[r[1]] = {'bad_rate':rate,'count':count_num,'down':r[1],'range':r,
                                      'bad_num':bad_num,'count_num':count_num}
            self.down.append(r[1])
            self.bad_list.append(bad_num)
            self.count_list.append(count_num)
        print(self.range_table)

            
    def fit(self, bad=1, trend='up'):
        self.__stat(bad=bad)
        self.down = np.array(self.down)              # 各分区区间下限
        self.bad_list = np.array(self.bad_list)      # 各分区坏样本比例
        self.count_list = np.array(self.count_list)  # 各分区总样本比例
        
        self.cut_range = self.find_cut(trend=trend)  # 第一个切割点

        while True:
            cut_list = self.find_cut(self.cut_range,trend=trend)

            if len(cut_list)>0:
                for c in cut_list:
                    self.cut_range.append(c)
                    self.cut_range = sorted(list(set(self.cut_range)))
            else:
                break

        self.bins = np.array(sorted(list(set(self.cut_range))))
        
    
    def find_cut(self,cut_list=[],trend='up'):
        cuts = []
        if cut_list == []:
            candidate = sorted(copy.deepcopy(self.down))
            cut, rate = self.__find_cut(list(candidate),start='',end='',trend=trend)
            if rate:
                cuts.append(cut)
        else:
            for i in range(len(cut_list)):
                if i == 0:
                    candidate = list(self.down[self.down<cut_list[i]])
                    cut, rate = self.__find_cut(list(candidate),start='',end=cut_list[i],trend=trend)

                else:
                    candidate = list(self.down[(self.down<cut_list[i]) & (self.down>cut_list[i-1])])
                    cut, rate = self.__find_cut(list(candidate),start=cut_list[i-1],end=cut_list[i],trend=trend)

                if rate and cut not in self.cut_range:
                    cuts.append(cut)
                if i == len(cut_list)-1:
                    candidate = list(self.down[self.down>cut_list[i]])
                    cut, rate = self.__find_cut(list(candidate),start=cut_list[i],end='',trend=trend)

                    if rate and cut not in self.cut_range:
                        cuts.append(cut)   
        return cuts                       
        
    def __find_cut(self,candidate,start='',end='',trend='up'):
        result_cut = None
        result_rate = None

        for i in range(len(candidate)):
            if start=='' and end=='':
                bad_up = sum(self.bad_list[(self.down<=candidate[i])])
                count_up = sum(self.count_list[(self.down<=candidate[i])])                                                    
                bad_down = sum(self.bad_list[(self.down>candidate[i])])
                count_down = sum(self.count_list[(self.down>candidate[i])])    
            elif start == '' and end != '':   
                bad_up = sum(self.bad_list[(self.down<=candidate[i])])
                count_up = sum(self.count_list[(self.down<=candidate[i])])                                                    
                bad_down = sum(self.bad_list[(self.down>candidate[i]) & (self.down<=end)])
                count_down = sum(self.count_list[(self.down>candidate[i]) & (self.down<=end)])
            elif start != '' and end == '':
                bad_up = sum(self.bad_list[(self.down<=candidate[i]) & (self.down>start)])
                count_up = sum(self.count_list[(self.down<=candidate[i]) & (self.down>start)])                                                    
                bad_down = sum(self.bad_list[(self.down>candidate[i])])
                count_down = sum(self.count_list[(self.down>candidate[i])])    
            elif start != '' and end != '':
                bad_up = sum(self.bad_list[(self.down<=candidate[i]) & (self.down>start)])
                count_up = sum(self.count_list[(self.down<=candidate[i]) & (self.down>start)])                                                    
                bad_down = sum(self.bad_list[(self.down>candidate[i]) & (self.down<=end)])
                count_down = sum(self.count_list[(self.down>candidate[i]) & (self.down<=end)])   
                
            if count_down == 0:
                rate_down = 0
            else:
                rate_down = bad_down/count_down
            if count_up == 0:
                rate_up = 0
            else:
                rate_up = bad_up/count_up    
                
            rate = rate_down - rate_up
            
            if trend=='up':
                if rate >=0:
                    if not result_rate:
                        result_rate = rate
                        result_cut = candidate[i] 
                    if rate > result_rate and candidate[i] not in self.cut_range:
                        result_rate = rate
                        result_cut = candidate[i] 
            elif trend=='down':
                if rate <=0:
                    if not result_rate:
                        result_rate = rate
                        result_cut = candidate[i] 
                    if rate < result_rate and candidate[i] not in self.cut_range:
                        result_rate = rate
                        result_cut = candidate[i]                 
        #print(result_cut, result_rate)                                               
        return result_cut, result_rate
