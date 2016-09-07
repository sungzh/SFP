#!/usr/local/bin/python
# -*- c ding: UTF-8 -*-

import sys
import random
import json

reload(sys)
sys.setdefaultencoding("utf-8")

class Ad(object):

    
    def __init__(self, name, pos, theta, demand):
        self.name = name
        self.pos = pos
        self.theta = theta
        self.demand = demand
        
        self.ctr = 0.0
        self.threshold = dict()
        self.candidateNum = dict()
        self.selectedNum = dict()
        self.retainRate = dict()

class Pv(object):

    def __init__(self, cookie):
        self.cookie = cookie


class sfp(object):

    ads = []
    pv = None
    cookie_strategy = dict()

    def init_ads(self, num = -1, pos = 'PDPS'):
        if num == -1:
            num = random.randint(1, 3)
        print 'init ads: [',
        for i in range(0, num):
            theta = random.random()
            demand = random.randint(100, 10000)
            ad = Ad('ad'+str(i), pos, theta, demand)
            print ad.name, ',', 
            self.ads.append(ad)
        print ']', num, 'ads init finished'
        #print 'init ads: ', self.ads

    def init_strategy(self):
        for i in range(0, 10):
            self.cookie_strategy[i] = 'strategy_baseline'
        for i in range(10, 20):
            self.cookie_strategy[i] = 'strategy_baseline'
        for i in range(20, 30):
            self.cookie_strategy[i] = 'strategy_baseline'
        for i in range(30, 40):
            self.cookie_strategy[i] = 'strategy_baseline'
        for i in range(40, 50):
            self.cookie_strategy[i] = 'strategy_baseline'
        for i in range(50, 60):
            self.cookie_strategy[i] = 'strategy_baseline'
        for i in range(60, 70):
            self.cookie_strategy[i] = 'strategy_baseline'
        for i in range(70, 80):
            self.cookie_strategy[i] = 'strategy_baseline'
        for i in range(80, 90):
            self.cookie_strategy[i] = 'strategy_baseline'
        for i in range(90, 100):
            self.cookie_strategy[i] = 'strategy_baseline'
        #print 'init startegy: ', json.dumps(self.cookie_strategy, indent=4)
       



    def construct_pv(self):
        pv = Pv(random.randint(0, 10000))


    def selectAd(self, pv, ads):

        strategy_name = self.strategy(pv.cookie)
        print 'pv:', pv.cookie, ' in strategy: ', strategy_name
        print 'candidate ads: ' 
        selectedAd = []
        for ad in ads:
            print ad.name, ',',
            if not ad.threshold.has_key(strategy_name):
                ad.threshold[strategy_name] = 0.00000001;
                ad.candidateNum[strategy_name] = 0
                ad.selectedNum[strategy_name] = 0
            ad.candidateNum[strategy_name] = ad.candidateNum[strategy_name] + 1
            ad.ctr = random.uniform(0.0005, 0.1)
            print 'ctr and threshold is :', ad.ctr, ad.threshold[strategy_name],
            if ad.ctr > ad.threshold[strategy_name]:
                selectedAd.append(ad)
                print 'selected ', ad.name
            #print ad.name, ad.candidateNum, ad.ctr
            
        if len(selectedAd) > 0:
            num = random.randint(0, len(selectedAd)-1)
            selectedAd[num].selectedNum[strategy_name] = selectedAd[num].selectedNum[strategy_name] + 1
            print 'selected ad: [', selectedAd[num].name, ']'
        else:
            print 'selected not ad'


        print 'threshold adjust:'
        for ad in ads:
            ad.retainRate[strategy_name] = ad.selectedNum[strategy_name] * 1.0 / ad.candidateNum[strategy_name]
            if ad.retainRate[strategy_name] != 0.0:
                print ad.name, 'in ', strategy_name, ' threshold from ', ad.threshold[strategy_name],
                ad.threshold[strategy_name] = ad.threshold[strategy_name] * ad.retainRate[strategy_name] / ad.theta
                print ' to ', ad.threshold[strategy_name]
            print ad.name, 'retain pro is', ad.retainRate[strategy_name], ' theta is', ad.theta, ' candidate num is', ad.candidateNum[strategy_name], ' selected num is', ad.selectedNum[strategy_name]
        print 'threshold adjusted finished'

        print '\n\n\n'


    def strategy(self, hashcode):
        index = hashcode % 997
        index = index % 100
        return  self.cookie_strategy[index]


    def do(self):

        self.init_ads()
        self.init_strategy()

        i = 0
        while True:
            pv = Pv(random.randint(0, 1000))
            self.selectAd(pv, self.ads)
            i = i + 1
            if i >= 2000:
                break

        return 


if __name__ == "__main__":
    _sfp = sfp()
    _sfp.do()





            
            









