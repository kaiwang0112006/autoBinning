# -*- coding: utf-8 -*-
from .trendSplit import *
import numpy as np
import copy
import math


class forwardSplit(trendSplit):
    def __init__(self, x, y, bad=1,missing=None, force=False):
        trendSplit.__init__(self, x, y, bad, missing, force)

    def fit(self, init_split=0, num_split=0, minv=0, sby='woe', min_sample=0):
        '''
        :param num_split: 最大切割点数,不包含最大最小值
        :param minv: 最小分裂所需数值，woe/iv
        :param sby: 'woe','iv','woeiv'
        :param min_sample: 每个分箱最小样本数
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

        param = {'minv': minv, 'sby': sby, 'min_sample':min_sample}
        cut, iv = self.find_cut(**param)
        param['iv_base'] = iv
        self.cut_range = [cut]
        if cut!=None:
            self.candidate.remove(cut)
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


    def find_cut(self,minv=None, sby='iv',iv_base=0, min_sample=0):
        '''
        :param minv: 最小分裂所需数值，woe/iv
        :param sby: 'woe','iv','woeiv'
        :param iv_base: 上一轮的iv值，sby='woe'时不用考虑
        :return:
        '''
        if not minv:
            minv = 0
        if ((sby== 'woe') or (sby == 'woeiv')) and (not self.trend) and len(self.cut_range)>0:
            self.candidateTrend(self.cut_range)

        iv = 0

        cut = None
        result = {}
        for i in range(1, len(self.candidate) - 1):
            if len(self.cut_range) == 0:
                woe_range = (self.candidate[0]-0.1, self.candidate[i], self.candidate[-1])
                iv_range = (self.candidate[0]-0.1, self.candidate[i], self.candidate[-1])
            else:
                range_list = sorted([self.candidate[0]-0.1, self.candidate[i], self.candidate[-1]]+list(self.cut_range))
                canidx = range_list.index(self.candidate[i])
                #woe_range = (self.candidate[0], self.candidate[i], self.candidate[-1]+1)
                woe_range = (range_list[canidx-1], range_list[canidx], range_list[canidx+1])
                iv_range = tuple(range_list)

            if len(self.value[(self.x < woe_range[1]) & (self.x >= woe_range[0])]) > min_sample and \
                    len(self.value[(self.x < woe_range[2]) & (self.x >= woe_range[1])]) > min_sample:
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
                    is_trend_tag = False
                    if self.trend in ('up','down'):
                        up_count, down_count = self.candidateTrend(list(iv_range)[1:-1])
                        if (self.trend == 'up' and down_count==0 and up_count>0) or \
                           (self.trend == 'down' and down_count > 0 and up_count == 0):
                            is_trend_tag = True

                    iv = self.cal_iv_by_range(iv_range)
                    #print(is_trend_tag, self.trend not in ('up','down'), self.trend)
                    #print((is_trend_tag or self.trend not in ('up','down')))
                    if (is_trend_tag or self.trend not in ('up','down')) and iv > minv:
                        minv = iv
                        cut = self.candidate[i]

        return cut, iv
