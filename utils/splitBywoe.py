# -*- coding: utf-8 -*-
from .simpleMethods import *
import numpy as np
import copy
import math

class splitBywoe(simpleMethods):
    def __init__(self,x,y):
        simpleMethods.__init__(self,x) 
        self.y = y
        self.cut_range = []
            
    def fit(self, bad=1,init_split=0,trend='up',num_split=None, minwoe=None):
        '''
        :param bad: 坏样本标记，默认label=1为坏样本
        :param trend: 趋势参数，up为woe递增，down为woe递减，默认为None，不考虑趋势，取woe最大的切分点
        :param num_split: 最大切割点数,不包含最大最小值
        :param minwoe: 最小分裂所需woe
        :return: numpy array -- 切割点数组
        '''
        self.value = np.array(self.y)
        self.allbad = len(self.value[self.value==bad])  # 好样本总数
        self.allgood = len(self.value)-self.allbad      # 坏样本总数

        if init_split == 0 or len(self.x) <= init_split:
            self.everysplit()
        else:
            self.equalSize(init_split)

        candidate = []
        for r in self.range_dict:
            candidate.append(r[0])
            candidate.append(r[1])
        self.candidate = sorted(list(set(candidate)))
        cut = self.find_cut(bad=bad, trend=trend, minwoe=minwoe)
        self.cut_range = [cut]

        if cut:
            while True:
                cut = self.find_cut(bad=bad,trend=trend,minwoe=minwoe)
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

    def find_cut(self,bad=1,trend='up',minwoe=None):
        '''
        基于最大woe分裂切割
        :param cut_list: 已分裂的结点
        :param bad: 坏样本标记，默认label=1为坏样本
        :param trend: 趋势参数，up为woe递增，down为woe递减，默认为None，不考虑趋势，取woe最大的切分点
        :param minwoe: 最小分裂所需woe
        :return: 新的一个最大切割点
        '''
        result_cut = None
        result_woe = None
        if not minwoe:
            minwoe=0
        cut_find = None
        # 先计算所有的范围：(start, point, end)
        candidate_pair = []
        if len(self.cut_range) == 0:
            for i in range(1, len(self.candidate)-1):
                candidate_pair.append((self.candidate[0],self.candidate[i],self.candidate[-1]+1))
        else:
            pidx = 0
            cut_range = sorted(self.cut_range)
            for i in range(1, len(self.candidate)-1):
                if self.candidate[i] not in cut_range:
                    if pidx<=len(cut_range)-1:
                        if self.candidate[i]>cut_range[pidx]:
                            pidx+=1
                    start = self.candidate[0] if pidx==0 else cut_range[pidx-1]
                    end = self.candidate[-1] if pidx==len(cut_range) else cut_range[pidx]
                    candidate_pair.append((start, self.candidate[i], end))

        # 计算woe最大的point
        #print(candidate_pair)
        compare_woe = {}
        for i in range(len(candidate_pair)):
            v_up = self.value[(self.x<candidate_pair[i][1]) & (self.x>=candidate_pair[i][0])]
            v_down = self.value[(self.x<candidate_pair[i][2]) & (self.x>=candidate_pair[i][1])]

            woe_up = self._cal_woe(v_up,bad=bad)
            woe_down = self._cal_woe(v_down, bad=bad)
            if trend == 'up':
                woe_sub = woe_up - woe_down
            elif trend == 'down':
                woe_sub = woe_down - woe_up
            else:
                woe_sub = abs(woe_down - woe_up)

            if woe_sub-minwoe>0:
                compare_woe[candidate_pair[i][1]] = woe_sub
                if not result_woe:
                    result_woe = woe_sub
                    result_cut = candidate_pair[i][1]
                elif woe_sub > result_woe and candidate_pair[i][1] not in self.cut_range:
                    result_woe = woe_sub
                    result_cut = candidate_pair[i][1]

        return result_cut

