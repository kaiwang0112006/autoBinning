# -*- coding: utf-8 -*-
from .trendSplit import *
import numpy as np
import copy
import math
import time


class backwardSplit(trendSplit):
    def __init__(self, x, y, bad=1):
        trendSplit.__init__(self, x, y, bad)

    def fit(self, init_split=0, num_split=0, minv=0, sby='iv', trend=None):
        '''
        :param num_split: 最大切割点数,不包含最大最小值
        :param minv: 最小分裂所需数值，woe/iv
        :param sby: 'woe','iv','woeiv'
        :return: numpy array -- 切割点数组
        '''
        self.set_init()
        self.trend = trend
        if init_split == 0 or len(self.x) <= init_split:
            self.everysplit()
        else:
            self.equalSize(init_split)

        candidate = []
        for r in self.range_dict:
            candidate.append(r[0])
            candidate.append(r[1])
        self.candidate = sorted(list(set(candidate)))

        param = {'minv': minv, 'sby': sby, 'num_split':num_split}
        cut, iv = self.find_cut(**param)

        self.candidate.remove(cut)

        # merge by iv
        if cut:
            while True:
                cut, iv = self.find_cut(**param)

                if cut:
                    self.candidate.remove(cut)
                else:
                    break

                if num_split:
                    if len(self.candidate) <= num_split:
                        break

            self.bins = np.array(sorted(list(set(self.candidate))))
        else:
            self.bins = None


    def find_cut(self, num_split=0, minv=None, sby='iv'):
        '''
        寻找最优切点
        :param parms:参数字典
                      minv: 最小分裂所需数值，woe/iv
                      sby: 'woe','iv','woeiv'
                      iv_base: 上一轮的iv值
        :return:
        '''


        if not minv:
            minv = 0

        if (sby == 'woeiv') and (not self.trend):
            self.candidateTrend()

        iv = 0
        cut = None
        if len(self.candidate)>num_split:
            for i in range(1, len(self.candidate)-1):
                candidate_list = [c for c in self.candidate if c!=self.candidate[i]]
                down_idx = candidate_list.index(self.candidate[i+1])
                iv_range = tuple(candidate_list)
                iv = self.cal_iv_by_range(iv_range)

                if sby == 'woeiv' and self.trend in ('up','down'):
                    # find new trend
                    trend_constant = self.istrendConstant(candidate_list, down_idx)
                else:
                    trend_constant = True

                if trend_constant and iv > minv:
                    minv = iv
                    cut = self.candidate[i]
        #print(cut, iv_range, iv)

        return cut, iv

    def istrendConstant_loss(self, candidates, idx):

        v_mid = self.value[(self.x < candidates[idx]) & (self.x >= candidates[idx-1])]
        woe_mid = self._cal_woe(v_mid)

        if (woe_mid>0 and self.trend == 'up') or (woe_mid<0 and self.trend == 'down'):
           return True
        else:
            return False

    def istrendConstant(self, candidates, idx):
        woe_mid = self.cal_woe_by_start_end(candidates[idx-1], candidates[idx])
        woe_up = None
        woe_down = None
        know_box_range = sorted(list(self.know_box.keys()))
        for i in range(len(know_box_range)):
            if know_box_range[i][0]>=candidates[idx]:
                woe_down = self.cal_woe_by_start_end(know_box_range[i][0], know_box_range[i][1])
            break
        for i in range(len(know_box_range)-1,-1,-1):
            if know_box_range[i][1]<=candidates[idx-1]:
                woe_up = self.cal_woe_by_start_end(know_box_range[i][0], know_box_range[i][1])
            break


        if not woe_up and idx-2 >= 0:
            woe_up = self.cal_woe_by_start_end(candidates[idx-2], candidates[idx-1])
        else:
            woe_up = woe_mid

        if not woe_down and idx+1 <= len(candidates)-1:
            woe_down = self.cal_woe_by_start_end(candidates[idx], candidates[idx+1])
        else:
            woe_down = woe_mid
        print(woe_up, woe_mid, woe_down, self.trend)
        if (woe_up>=woe_mid and woe_mid>=woe_down and self.trend == 'up') or \
           (woe_up<=woe_mid and woe_mid<=woe_down and self.trend == 'down'):
           return True
        else:
            return False



