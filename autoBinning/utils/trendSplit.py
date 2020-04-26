# -*- coding: utf-8 -*-
from .simpleMethods import *
import numpy as np
import copy
import math


class trendSplit(simpleMethods):
    def __init__(self, x, y, bad=1,missing=None,force=False):
        simpleMethods.__init__(self, x,  missing=missing,force=force)
        self.y = y
        self.bad=bad
        self.set_init()

    def set_init(self):
        self.cut_range = []
        self.trend = None
        self.value = np.array(self.y)
        if self.missing == None:
            self.value_miss = None
        else:
            self.value_miss = self.value[self.x_org == self.missing]
            self.value = self.value[self.x_org!=self.missing]

        self.allbad = len(self.value[self.value == self.bad])  # 好样本总数
        self.allgood = len(self.value) - self.allbad  # 坏样本总数
        self.candidate = []
        self.woe_cache = {}
        self.iv_cache = {}
        self.chisquare_cache = {}
        self.know_box = {}

    def cal_woe_by_range(self,wrange):
        '''
        根据切点范围(start, mid, end)计算woe
        :param wrange:
        :param trend:
        :return:
        '''
        woe_up = self.cal_woe_by_start_end(wrange[0], wrange[1])
        woe_down = self.cal_woe_by_start_end(wrange[1], wrange[2])

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
        result = []
        for j in range(len(vrange)-1):
            if (vrange[j], vrange[j+1]) not in self.iv_cache:
                vvalue = self.value[(self.x < vrange[j+1]) & (self.x >= vrange[j])]
                iv_box = self._cal_iv(vvalue)
                self.iv_cache[(vrange[j], vrange[j+1])] = iv_box
            else:
                iv_box = self.iv_cache[(vrange[j], vrange[j+1])]
            result.append(iv_box)
            iv_split += iv_box

        return iv_split

    def cal_woe_by_start_end(self, start, end):
        if (start, end) not in self.woe_cache:
            vvalue = self.value[(self.x < end) & (self.x >= start)]
            woe_box = self._cal_woe(vvalue)
            self.woe_cache[(start, end)] = woe_box
        else:
            woe_box = self.woe_cache[(start, end)]
        return woe_box

    def _cal_woe(self,v):
        '''
        计算woe
        :param v:
        :param bad:
        :return:
        '''
        bad_num = len(v[v == self.bad])
        count_num = len(v)

        if count_num-bad_num==0 or self.allgood==0 or bad_num==0:
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

        if count_num-bad_num == 0 or self.allgood==0 or bad_num==0:
            iv = 0
        else:
            iv = (bad_num / (count_num - bad_num))*math.log((bad_num / (count_num - bad_num)) / (self.allbad / self.allgood))
        return iv

    def candidateTrend(self,cut_range):
        #print(cut_range)
        trend_up = 0
        trend_down = 0
        result = {}
        if len(cut_range) == 0:
            candidate_list = copy.deepcopy(self.candidate)
        else:
            candidate_list = [self.candidate[0]] + copy.deepcopy(cut_range) + [self.candidate[-1]]
        for i in range(1,len(candidate_list) - 1):
            woe_up = self.cal_woe_by_start_end(candidate_list[i-1], candidate_list[i])
            woe_down = self.cal_woe_by_start_end(candidate_list[i], candidate_list[i+1])

            if woe_up>woe_down:
                trend_up += 1
            elif woe_up<woe_down:
                trend_down += 1
            result[candidate_list[i]] = (woe_up, woe_down)

        if trend_up>trend_down:
            self.trend = 'up'
        elif trend_up<trend_down:
            self.trend = 'down'
        #print(trend_up, trend_down, result)
        return trend_up, trend_down

    def cal_chisquare_by_range(self, chi_range):
        if chi_range not in self.chisquare_cache:
            v_up = self.value[(self.x < chi_range[1]) & (self.x >= chi_range[0])]
            v_down = self.value[(self.x < chi_range[2]) & (self.x >= chi_range[1])]
            all_num = len(v_up)+len(v_down)
            up_bad = len(v_up[v_up==self.bad])
            up_good = len(v_up)-up_bad
            down_bad = len(v_down[v_down==self.bad])
            down_good = len(v_down)-down_bad
            all_g = up_good + down_good
            all_b = up_bad + down_bad

            if len(v_up)==0 or len(v_down)==0:
                chisquare_value = 10**7
            else:
                chisquare_value = (up_bad-len(v_up)*all_b/all_num)/len(v_up)*all_b/all_num + \
                     (up_good-len(v_up)*all_g/all_num)/len(v_up)*all_g/all_num + \
                     (down_good-len(v_down)*all_g/all_num)/len(v_down)*all_g/all_num + \
                     (down_bad-len(v_down)*all_b/all_num)/len(v_down)*all_b/all_num
            self.chisquare_cache[chi_range] = chisquare_value
        else:
            chisquare_value = self.chisquare_cache[chi_range]
        return chisquare_value
