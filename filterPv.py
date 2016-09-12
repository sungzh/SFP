#!/usr/local/bin/python
# -*- c ding: UTF-8 -*-

import sys
import random
import json
import numpy as np
import matplotlib.pyplot as plt

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

        self.ctrlog = dict()
        self.ctrretain = dict()
        self.ctrfilter = dict()
        self.thresholdlog = dict()

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


    def selectAd(self, pv, ads, threshold, adjustThreshold):

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
            if not ad.ctrlog.has_key(strategy_name):
                ad.ctrlog[strategy_name] = []
                ad.thresholdlog[strategy_name] = []
                ad.ctrretain[strategy_name] = []
                ad.ctrfilter[strategy_name] = []
            ad.ctrlog[strategy_name].append(ad.ctr)
            ad.thresholdlog[strategy_name].append(ad.threshold[strategy_name])
            t = threshold(ad, strategy_name)
            print 'ctr, threshold, adn using threshold is :', ad.ctr, ad.threshold[strategy_name], t,
            #if ad.ctr > ad.threshold[strategy_name]:
            if ad.ctr > t:
                selectedAd.append(ad)
                ad.ctrretain[strategy_name].append(ad.ctr)
                #ad.ctrfilter[strategy_name].append(-0.001)
                print 'selected ', ad.name
            else:
                #ad.ctrretain[strategy_name].append(-0.001)
                ad.ctrfilter[strategy_name].append(ad.ctr)
            #print ad.name, ad.candidateNum, ad.ctr
            
        if len(selectedAd) > 0:
            num = random.randint(0, len(selectedAd)-1)
            selectedAd[num].selectedNum[strategy_name] = selectedAd[num].selectedNum[strategy_name] + 1
            print 'selected ad: [', selectedAd[num].name, ']'
        else:
            print 'selected not ad'

        adjustThreshold(ads, strategy_name)

        print '\n\n\n'

    def simpleThreshold(self, ad, strategy_name):
        return ad.threshold[strategy_name]

    def simpleAdjustThreshold(self, ads, strategy_name):
        print 'threshold adjust:'
        for ad in ads:
            ad.retainRate[strategy_name] = ad.selectedNum[strategy_name] * 1.0 / ad.candidateNum[strategy_name]
            if ad.retainRate[strategy_name] != 0.0:
                print ad.name, 'in ', strategy_name, ' threshold from ', ad.threshold[strategy_name],
                ad.threshold[strategy_name] = ad.threshold[strategy_name] * ad.retainRate[strategy_name] / ad.theta
                print ' to ', ad.threshold[strategy_name]
            print ad.name, 'retain pro is', ad.retainRate[strategy_name], ' theta is', ad.theta, ' candidate num is', ad.candidateNum[strategy_name], ' selected num is', ad.selectedNum[strategy_name]
        print 'threshold adjusted finished'

    def eThreshold(self, ad, strategy_name):
        thresholdlist = ad.thresholdlog[strategy_name]
        t = sum(thresholdlist) / float(len(thresholdlist))
        return t

    def usingEAjustThreshold(self, ads):
        print 'threshold adjust:'
        for ad in ads:
            ad.retainRate[strategy_name] = ad.selectedNum[strategy_name] * 1.0 / ad.candidateNum[strategy_name]
            if ad.retainRate[strategy_name] != 0.0:
                print ad.name, 'in ', strategy_name, ' threshold from ', ad.threshold[strategy_name],
                ad.threshold[strategy_name] = ad.threshold[strategy_name] * ad.retainRate[strategy_name] / ad.theta
                print ' to ', ad.threshold[strategy_name]
            print ad.name, 'retain pro is', ad.retainRate[strategy_name], ' theta is', ad.theta, ' candidate num is', ad.candidateNum[strategy_name], ' selected num is', ad.selectedNum[strategy_name]
        print 'threshold adjusted finished'
        


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
            #self.selectAd(pv, self.ads, self.simpleThreshold, self.simpleAdjustThreshold)
            self.selectAd(pv, self.ads, self.eThreshold, self.simpleAdjustThreshold)
            i = i + 1
            if i >= 20000:
                break
        for ad in self.ads:
            for strategy in ad.ctrlog.keys():
                #self.drawPlot('retain vs retain', ad.ctrretain[strategy], ad.ctrfilter[strategy]) 
                #self.drawTwoPlot(ad.name+strategy+'ctr', ad.ctrlog[strategy], 
                #        ad.name+strategy+'threshold', ad.thresholdlog[strategy])
                self.evaluation(ad.ctrlog[strategy], ad.ctrretain[strategy], ad.ctrfilter[strategy], ad.theta)

        return 

    def drawPlot(self, title, data1, data2):
        plt.plot(data1, 'k')
        plt.plot(data2, 'g')
        plt.show()

    def drawTwoPlot(self, title1, data1, title2, data2):
        x1 = range(0, len(data1))
        x2 = range(0, len(data2))
        
        y1 = data1
        y2 = data2
                   
        plt.subplot(2, 1, 1)
        #plt.plot(x1, y1, 'yo-')
        plt.plot(x1, y1)
        plt.title('A tale of 2 subplots')
        plt.ylabel(title1)
                        
        plt.subplot(2, 1, 2)
        plt.plot(x2, y2)
        plt.xlabel('time (s)')
        plt.ylabel(title2)
        
        plt.show()

    def evaluation(self, totallist, retainlist, filterlist, theta):
        tlist = sorted(totallist, reverse=True)
        index = int(theta*len(tlist))
        key = tlist[index]
        print 'key is: [', key, ']; index is: [', index, ']'
        
        retain_greater = 0
        retain_lower = 0
        
        for ctr in retainlist:
            if ctr >= key:
                retain_greater = retain_greater + 1
            else:
                retain_lower = retain_lower + 1

        filter_greater = 0
        filter_lower = 0
        for ctr in filterlist:
            if ctr >= key:
                filter_greater = filter_greater + 1
            else:
                filter_lower = filter_lower + 1
        print 'total pv num is: [', len(totallist), ']; theta is: [', theta, '], key is: [', key, ']'
        if len(retainlist) != 0 :
            print 'retain pv num is: [', len(retainlist), '], greater than key num is: [', retain_greater, '], pro is: [', retain_greater*1.0/len(retainlist), '], lower than key num is: [', retain_lower, '], pro is: [', retain_lower*1.0/len(retainlist), ']'
        else:
            print 'no retain pv'
        if len(filterlist) != 0:
            print 'filter pv num is: [', len(filterlist), '], greater than key num is: [', filter_greater, '], pro is: [', filter_greater*1.0/len(filterlist), '], lower than key num is: [', filter_lower, '], pro is: [', filter_lower*1.0/len(filterlist), ']'
        else:
            print 'no filter pv'
        if len(retainlist) != 0 and len(filterlist) != 0:
            print 'average total ctr is: [', sum(filterlist)/float(len(filterlist)), '], average retain ctr is: [', sum(filterlist)/float(len(filterlist)), '], average filter ctr is: [', sum(filterlist)/float(len(filterlist)), ']'
        print '\n\n\n'


        


if __name__ == "__main__":
    _sfp = sfp()
    _sfp.do()





            
            









