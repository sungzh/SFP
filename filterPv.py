#!/usr/local/bin/python
# -*- c ding: UTF-8 -*-

import sys
import random

reload(sys)
sys.setdefaultencoding("utf-8")

class Ad(object):

    ctr = 0.0
    threshold = 0.0
    candidateNum = 0
    selectedNum = 0
    retainRate = 0.0
    
    def __init__(self, name, pos, theta, demand):
        self.name = name
        self.pos = pos
        self.theta = theta
        self.demand = demand

class Pv(object):

    def __init__(self, cookie):
        self.cookie = cookie


class sfp(object):

    ads = []
    pv = None

    def init_ads(self, num = -1, pos = 'PDPS'):
        if num == -1:
            num = random.randint(0, 3)
        for i in range(0, num):
            theta = random.random()
            demand = random.randint(100, 10000)
            ad = Ad('ad'+i, pos, theta, demand)
            ad.ctr = random.random()
            ads.append(ad)


    def construct_pv(self):
        pv = Pv(random.randint(0, 10000))


    def selectAd(self, pv, ads):
        selectedAd = []
        for ad in ads:
            ad.candidateNum = ad.candidateNum + 1
            if ad.ctr > ad.threshold:
                selectAd.append(ad)
            
        if selectAd.size() > 0:
            num = random.randint(1, selectAd.size())
            selectAd[num].selectedNum = selectAd[num].selectedNum + 1

        for ad in ads:
            ad.retainRate = ad.selectedNum * 1.0 / ad.candidateNum
            ad.threshold = ad.threshold * ad.retainRate / ad.theta



        


    def do(self):

        self.init_ads

        while True:
            pv = Pv(random.randint(0, 1000))






            
            









