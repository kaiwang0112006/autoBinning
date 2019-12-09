# -*- coding: utf-8 -*-
from .trendSplit import *
import numpy as np
import copy
import math


class forwardSplit(trendSplit):
    def __init__(self, x, y, bad=1):
        trendSplit.__init__(self, x, y, bad)

    def fit(self, init_split=0, num_split=None, minv=None, sby='woe'):
        '''
        :param num_split: 最大切割点数,不包含最大最小值
        :param minv: 最小分裂所需数值，woe/iv
        :param sby: 'woe','iv','woeiv'
        :return: numpy array -- 切割点数组
        '''
        self.set_init()

        if init_split == 0 or len(self.x) <= init_split:
            self.everysplit()
        else:
            self.equalSize(init_split)

        candidate = []
        for r in self.range_dict:
            candidate.append(r[0])
            candidate.append(r[1])
        self.candidate = sorted(list(set(candidate)))

        param = {'minv': minv, 'sby': sby}
        cut, iv = self.find_cut(**param)
        param['iv_base'] = iv
        self.cut_range = [cut]
        self.candidate.remove(cut)
        if cut:
            while True:
                cut, iv = self.find_cut(**param)
                param['iv_base'] = iv
                if cut:
                    self.cut_range.append(cut)
                    self.cut_range = sorted(list(set(self.cut_range)))
                    self.candidate.remove(cut)
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


    def find_cut(self,minv=None, sby='iv',iv_base=None):
        '''
        寻找最优切点
        :param parms:参数字典
                      minv: 最小分裂所需数值，woe/iv
                      sby: 'woe','iv','woeiv'
                      iv_base: 上一轮的iv值，sby='woe'时不用考虑
        :return:
        '''
        if not minv:
            minv = 0
        if ((sby== 'woe') or (sby == 'woeiv')) and (not self.trend):
            self.trend = self.candidateTrend()

        iv = 0
        if not iv_base:
            iv_base = 0
        cut = None
        result = {}
        for i in range(1, len(self.candidate) - 1):
            if len(self.cut_range) == 0:
                woe_range = (self.candidate[0], self.candidate[i], self.candidate[-1]+1)
                iv_range = (self.candidate[0], self.candidate[i], self.candidate[-1]+1)
            else:
                range_list = sorted([self.candidate[0], self.candidate[i], self.candidate[-1]+1]+list(self.cut_range))
                canidx = range_list.index(self.candidate[i])
                #woe_range = (self.candidate[0], self.candidate[i], self.candidate[-1]+1)
                woe_range = (range_list[canidx-1], range_list[canidx], range_list[canidx+1])
                iv_range = tuple(range_list)

            if sby == 'woe':
                woe = self.cal_woe_by_range(woe_range)
                if woe > minv:
                    minv = woe
                    cut = self.candidate[i]
            elif sby == 'iv':
                iv = self.cal_iv_by_range(iv_range)
                result[self.candidate[i]] = iv
                if iv > minv and iv > iv_base:
                    minv = iv
                    cut = self.candidate[i]
            else:
                woe = self.cal_woe_by_range(woe_range)
                iv = self.cal_iv_by_range(iv_range)
                if ((woe>=0 and self.trend=='up') or (woe<=0 and self.trend=='down') \
                    or self.trend not in ('up','down')) and iv > minv:
                    minv = iv
                    cut = self.candidate[i]

        return cut, iv
