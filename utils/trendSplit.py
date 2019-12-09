# -*- coding: utf-8 -*-
from .simpleMethods import *
import numpy as np
import copy
import math


class trendSplit(simpleMethods):
    def __init__(self, x, y, bad=1):
        simpleMethods.__init__(self, x)
        self.y = y
        self.bad=bad
        self.set_init()

    def set_init(self):
        self.cut_range = []
        self.trend = None
        self.value = np.array(self.y)
        self.allbad = len(self.value[self.value == self.bad])  # 好样本总数
        self.allgood = len(self.value) - self.allbad  # 坏样本总数
        self.candidate = []

    def cal_woe_by_range(self,wrange):
        '''
        根据切点范围(start, mid, end)计算woe
        :param wrange:
        :param trend:
        :return:
        '''
        v_up = self.value[(self.x < wrange[1]) & (self.x >= wrange[0])]
        v_down = self.value[(self.x < wrange[2]) & (self.x >= wrange[1])]

        woe_up = self._cal_woe(v_up)
        woe_down = self._cal_woe(v_down)
        if self.trend == 'up':
            woe_sub = woe_up - woe_down
        elif self.trend == 'down':
            woe_sub = woe_down - woe_up
        else:
            woe_sub = abs(woe_down - woe_up)
        return woe_sub

    def cal_iv_by_range(self,vrange):
        '''
        根据切点范围(start, mid, end)计算iv
        :param vrange:
        :param bad:
        :return:
        '''
        iv_split = 0
        for j in range(len(vrange)-1):
            vvalue = self.value[(self.x < vrange[j+1]) & (self.x >= vrange[j])]
            iv_box = self._cal_iv(vvalue)
            iv_split += iv_box
        return iv_split

    def _cal_woe(self,v):
        '''
        计算woe
        :param v:
        :param bad:
        :return:
        '''
        bad_num = len(v[v == self.bad])
        count_num = len(v)

        if count_num-bad_num == 0 or self.allgood==0:
            woe = 0
        else:
            woe = math.log((bad_num / (count_num - bad_num)) / (self.allbad / self.allgood))
        return woe

    def _cal_iv(self, v):
        '''
        计算iv
        :param v:
        :param bad:
        :return:
        '''
        bad_num = len(v[v == self.bad])
        count_num = len(v)

        if count_num-bad_num == 0 or self.allgood==0:
            iv = 0
        else:
            iv = (bad_num / (count_num - bad_num))*math.log((bad_num / (count_num - bad_num)) / (self.allbad / self.allgood))
        return iv

    def candidateTrend(self):
        trend_up = 0
        trend_down = 0

        if len(self.cut_range) == 0:
            candidate_list = copy.deepcopy(self.candidate)
        else:
            candidate_list = [self.candidate[0]] + copy.deepcopy(self.cut_range) + [self.candidate[-1]]
        for i in range(1,len(candidate_list) - 1):
            v_up = self.value[(self.x < candidate_list[i]) & (self.x >= candidate_list[i-1])]
            v_down = self.value[(self.x < candidate_list[i+1]) & (self.x >= candidate_list[i])]
            woe_up = self._cal_woe(v_up)
            woe_down = self._cal_woe(v_down)
            iv_up = self._cal_iv(v_up)
            iv_down = self._cal_iv(v_down)
            if woe_up>woe_down:
                trend_up += 1
            elif woe_up<woe_down:
                trend_down += 1
        if trend_up>trend_down:
            self.trend = 'up'
        elif trend_up<trend_down:
            self.trend = 'down'