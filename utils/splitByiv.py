# -*- coding: utf-8 -*-
from .simpleMethods import *
import numpy as np
import copy
import math

class splitByiv(simpleMethods):
    def __init__(self,x,y):
        simpleMethods.__init__(self,x) 
        self.y = y
        self.cut_range = []
            
    def fit(self, bad=1,init_split=20,num_split=None, miniv=None):
        '''
        :param bad: 坏样本标记，默认label=1为坏样本
        :param init_split: 基于等频分箱确认初始分裂点, init_split=0时使用最细粒度
        :param num_split: 最大切割点数,不包含最大最小值
        :param miniv: 最小分裂所需iv
        :return: numpy array -- 切割点数组
        '''
        self.value = np.array(self.y)
        self.allbad = len(self.value[self.value==bad])  # 好样本总数
        self.allgood = len(self.value)-self.allbad      # 坏样本总数
        self.iv_base = 0
        if init_split == 0 or len(self.x) <= init_split:
            self.everysplit()
        else:
            self.equalSize(init_split)

        candidate = []
        for r in self.range_dict:
            candidate.append(r[0])
            candidate.append(r[1])
        self.candidate = sorted(list(set(candidate)))
        cut = self.find_cut(bad=bad, miniv=miniv)

        if cut:
            self.cut_range = [cut]  # 第一个切割点

            while True:
                cut = self.find_cut(bad=bad,miniv=miniv)
                if cut:
                    self.cut_range.append(cut)
                    self.cut_range = sorted(list(set(self.cut_range)))
                else:
                    break

                if num_split:
                    if len(set(self.cut_range)) >= num_split:
                        break

            self.cut_range.append(self.candidate[0])
            self.cut_range.append(self.candidate[-1])
            self.bins = np.array(sorted(list(set(self.cut_range))))
        else:
            self.cut_range = None
            self.bins = None
    
    def find_cut(self,bad=1,miniv=None):
        '''
        基于最大iv分裂切割
        :param bad: 坏样本标记，默认label=1为坏样本
        :param miniv: 最小分裂所需miniv
        :return: 新的一个最大切割点
        '''
        if not miniv:
            miniv=0

        cut_find = None
        iv = 0
        if len(self.cut_range) == 0:
            for i in range(1,len(self.candidate)-1):
                v_up = self.value[(self.x < self.candidate[i])]
                v_down = self.value[(self.x >= self.candidate[i])]

                iv_up = self._cal_iv(v_up,bad=bad)
                iv_down = self._cal_iv(v_down, bad=bad)
                iv_split = iv_down + iv_up
                if iv_split>=miniv and iv_split>iv:
                    iv = iv_split
                    cut_find = self.candidate[i]
        else:
            for i in range(1, len(self.candidate) - 1):
                if self.candidate[i] not in self.cut_range:
                    cut_points = copy.deepcopy(self.cut_range)
                    cut_points.append(self.candidate[i])
                    cut_points = sorted(list(set(cut_points)))
                    iv_split = 0
                    for j in range(len(cut_points)):
                        if j == 0:
                            vvalue = self.value[(self.x < cut_points[j])]
                        elif j == len(cut_points)-1:
                            vvalue = self.value[(self.x >= cut_points[j])]
                        else:
                            vvalue = self.value[(self.x < cut_points[j+1]) & (self.x >= cut_points[j])]
                        iv_up = self._cal_iv(vvalue,bad=bad)
                        iv_split += iv_up
                        if iv_split>=miniv and iv_split>iv and iv_split>self.iv_base:
                            iv = iv_split
                            cut_find = self.candidate[i]
        self.iv_base = iv
        print(self.iv_base)
        return cut_find