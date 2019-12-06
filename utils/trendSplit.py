# -*- coding: utf-8 -*-
from .simpleMethods import *
import numpy as np
import copy
import math


class trendSplit(simpleMethods):
    def __init__(self, x, y):
        simpleMethods.__init__(self, x)
        self.y = y
        self.cut_range = []

    def fit(self, bad=1, init_split=0, trend='up', num_split=None, minv=None, sby='woe'):
        '''
        :param bad: 坏样本标记，默认label=1为坏样本
        :param trend: 趋势参数，up为woe递增，down为woe递减，默认为None，不考虑趋势，
                      取woe最大的切分点，只对woe有效
        :param num_split: 最大切割点数,不包含最大最小值
        :param minv: 最小分裂所需数值，woe/iv
        :param sby: 'woe','iv','woeiv'
        :return: numpy array -- 切割点数组
        '''
        self.value = np.array(self.y)
        self.allbad = len(self.value[self.value == bad])  # 好样本总数
        self.allgood = len(self.value) - self.allbad  # 坏样本总数

        if init_split == 0 or len(self.x) <= init_split:
            self.everysplit()
        else:
            self.equalSize(init_split)

        candidate = []
        for r in self.range_dict:
            candidate.append(r[0])
            candidate.append(r[1])
        self.candidate = sorted(list(set(candidate)))

        param = {'bad': bad, 'trend': trend, 'minv': minv, 'sby': sby}
        cut, woe ,iv = self.find_cut(**param)
        param['woe'] = woe
        param['iv'] = iv
        self.cut_range = [cut]
        self.candidate.remove(cut)
        if cut:
            while True:
                cut, woe ,iv = self.find_cut(**param)
                param['iv'] = iv
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

    def find_cut(self,**parms):
        '''
        寻找最优切点
        :param parms:参数字典
                      bad: 坏样本标记，默认label=1为坏样本
                      trend: 趋势参数，up为woe递增，down为woe递减，默认为None，不考虑趋势，
                      取woe最大的切分点，只对woe有效
                      num_split: 最大切割点数,不包含最大最小值
                      minv: 最小分裂所需数值，woe/iv
                      sby: 'woe','iv','woeiv'
        :return:
        '''
        if parms['minv']:
            minv = parms['minv']
        else:
            minv = 0
        woe = 0
        iv_base = parms.get("iv", minv)
        cut = None
        result = {}
        for i in range(1, len(self.candidate) - 1):
            if len(self.cut_range) == 0:
                woe_range = (self.candidate[0], self.candidate[i], self.candidate[-1]+1)
                iv_range = (self.candidate[0], self.candidate[i], self.candidate[-1]+1)
            else:
                range_list = sorted([self.candidate[0], self.candidate[i], self.candidate[-1]+1]+list(self.cut_range))
                canidx = range_list.index(self.candidate[i])
                woe_range = (self.candidate[0], self.candidate[i], self.candidate[-1]+1)
                iv_range = tuple(range_list)

            if parms['sby'] == 'woe':
                woe = self.cal_woe_by_range(woe_range, parms['trend'],parms['bad'])
                if woe > minv:
                    minv = woe
                    cut = self.candidate[i]
            elif parms['sby'] == 'iv':
                iv = self.cal_iv_by_range(iv_range,parms['bad'])
                result[self.candidate[i]] = iv
                if iv > minv and iv>iv_base:
                    minv = iv
                    cut = self.candidate[i]
            else:
                woe = self.cal_woe_by_range(woe_range,parms['trend'],parms['bad'])
                iv = self.cal_iv_by_range(iv_range,parms['bad'])
                if ((woe>=0 and parms['trend']=='up') or (woe<=0 and parms['trend']=='down') \
                    or parms['trend'] not in ('up','down')) and iv > minv:
                    minv = iv
                    cut = self.candidate[i]

        return cut, woe, iv

    def cal_woe_by_range(self,wrange,trend,bad):
        '''
        根据切点范围(start, mid, end)计算woe
        :param wrange:
        :param trend:
        :return:
        '''
        v_up = self.value[(self.x < wrange[1]) & (self.x >= wrange[0])]
        v_down = self.value[(self.x < wrange[2]) & (self.x >= wrange[1])]

        woe_up = self._cal_woe(v_up, bad=bad)
        woe_down = self._cal_woe(v_down, bad=bad)
        if trend == 'up':
            woe_sub = woe_up - woe_down
        elif trend == 'down':
            woe_sub = woe_down - woe_up
        else:
            woe_sub = abs(woe_down - woe_up)
        return woe_sub

    def cal_iv_by_range(self,vrange,bad):
        '''
        根据切点范围(start, mid, end)计算iv
        :param vrange:
        :param bad:
        :return:
        '''
        iv_split = 0
        for j in range(len(vrange)-1):
            vvalue = self.value[(self.x < vrange[j+1]) & (self.x >= vrange[j])]
            iv_box = self._cal_iv(vvalue, bad=bad)
            iv_split += iv_box
        return iv_split

