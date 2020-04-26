# -*- coding: utf-8 -*-
from .trendSplit import *
import numpy as np
import copy
import math


class MAPA(trendSplit):
    def __init__(self, x, y, bad=1):
        trendSplit.__init__(self, x, y, bad)

    def fit(self,trend='up',sby='woe'):
        '''
        :param num_split: 最大切割点数,不包含最大最小值
        :param minv: 最小分裂所需数值，woe/iv
        :param sby: 'woe','iv','woeiv'
        :param min_sample: 每个分箱最小样本数
        :return: numpy array -- 切割点数组
        '''
        self.set_init()
        self.everysplit()
        if trend == 'auto':
            self.candidateTrend()
        else:
            self.trend = trend
        self.test = {}
        candidate = []
        for r in self.range_dict:
            candidate.append(r[0])
            candidate.append(r[1])

        if self.trend == 'up':
            self.candidate = sorted(list(set(candidate)),reverse=False)
        else:
            self.candidate = sorted(list(set(candidate)), reverse=True)

        cut_list, v = self.find_cut(sby=sby)
        self.cut_range = [cut_list[-1]]
        self.cut_range.append(self.candidate[0])
        self.cut_range.append(self.candidate[-1])
        for d in cut_list:
            self.candidate.remove(d)

        while True:
            cut_list, v = self.find_cut(sby=sby)
            if len(cut_list)>0:
                self.cut_range.append(cut_list[-1])
                self.cut_range = sorted(list(set(self.cut_range)))
                for d in cut_list:
                    self.candidate.remove(d)
            else:
                break
        self.bins = np.array(sorted(list(set(self.cut_range))))
        print(self.test)

    def find_cut(self,trend='up',sby='woe'):
        '''
        :param minv: 最小分裂所需数值，woe/iv
        :param sby: 'woe','iv','woeiv'
        :param iv_base: 上一轮的iv值，sby='woe'时不用考虑
        :return:
        '''
        cut_list = []
        cut = None
        minv = 0 # bad rate
        for c in self.candidate:
            if c != self.candidate[0]:
                if trend == 'up':
                    v = self.value[(self.x<c) & (self.x>=self.candidate[0])]
                else:
                    v = self.value[(self.x >=c) & (self.x < self.candidate[0])]

                if len(v)>0:
                    if sby == 'woe':
                        badr = self._cal_woe(v)
                    elif badr == 'bad':
                        badr = len(v[v == self.bad]) / len(v)
                    else:
                        badr = 0
                else:
                    badr = 0
                self.test[c] = badr
                if badr>=minv:
                    minv = badr
                    cut_list.append(c)
                else:
                    break
        return cut_list, minv

    def candidateTrend(self):
        trend_up = 0
        trend_down = 0

        candidate_list = copy.deepcopy(self.candidate)
        for i in range(1, len(candidate_list) - 1):
            v_up = self.value[(self.x < candidate_list[i]) & (self.x >= candidate_list[i - 1])]
            v_down = self.value[(self.x < candidate_list[i + 1]) & (self.x >= candidate_list[i])]
            woe_up = self._cal_woe(v_up)
            woe_down = self._cal_woe(v_down)
            iv_up = self._cal_iv(v_up)
            iv_down = self._cal_iv(v_down)
            if woe_up > woe_down:
                trend_up += 1
            elif woe_up < woe_down:
                trend_down += 1
        if trend_up > trend_down:
            self.trend = 'up'
        else:
            self.trend = 'down'
