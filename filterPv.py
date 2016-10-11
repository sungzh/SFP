#!/usr/local/bin/python
# -*- c ding: UTF-8 -*-

import sys
import random
import json
import math
import numpy as np
import matplotlib.pyplot as plt
from threshold import Threshold

reload(sys)
sys.setdefaultencoding("utf-8")

'''
    ad: ad info
'''
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
        self.usingthresholdlog = dict()

'''
    pv: user info
'''
class Pv(object):

    def __init__(self, cookie):
        self.cookie = cookie


class sfp(object):

    #ads = []
    pv = None
    cookie_strategy = dict()
    t = Threshold()

    '''
        init ads, 
        include name, pos, theta, demand
    '''
    def init_ads(self, num = -1, pos = 'PDPS'):
        ads = []
        if num == -1:
            num = random.randint(1, 1)
        print 'init ads: [',
        for i in range(0, num):
            theta = random.random()
            demand = random.randint(100, 10000)
            ad = Ad('ad'+str(i), pos, theta, demand)
            print ad.name, ',', 
            ads.append(ad)
        print '],', num, 'ads init finished'
        return ads
        #print 'init ads: ', self.ads

    '''
        copy ads
    '''
    def copy_ads(self, ads):
        copyads = []
        for ad in ads:
            nad = Ad(ad.name, ad.pos, ad.theta, ad.demand)
            copyads.append(nad)
        return copyads
    
    def setAdsCtr(self, ads):
        for ad in ads:
            ad.ctr = random.uniform(0.0005, 0.1)
    
    '''
        set ads1, ads2 ctr for the same
    '''
    def set_ads_ctr(self, ads1, ads2):
        for i in range(0, len(ads1)):
            ads1[i].ctr = random.uniform(0.0005, 0.1)
            ads2[i].ctr = ads1[i].ctr

    '''
        set adsList Ctr for the ads
    '''
    def setAdsListCtr(self, srcads, adsList):
        for ads in adsList:
            for i in range(0, len(ads)):
                ads[i].ctr = srcads[i].ctr


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


    def selectAd(self, pv, ads, threshold, paramNum, adjustThreshold, adjustParamNum):

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
            #ad.ctr = random.uniform(0.0005, 0.1)
            if not ad.ctrlog.has_key(strategy_name):
                ad.ctrlog[strategy_name] = []
                ad.thresholdlog[strategy_name] = []
                ad.usingthresholdlog[strategy_name] = []
                ad.ctrretain[strategy_name] = []
                ad.ctrfilter[strategy_name] = []
            ad.ctrlog[strategy_name].append(ad.ctr)
            ad.thresholdlog[strategy_name].append(ad.threshold[strategy_name])
            t = threshold(ad.thresholdlog[strategy_name], paramNum)
            ad.usingthresholdlog[strategy_name].append(t)
            print 'ctr, threshold, and using threshold is :', ad.ctr, ad.threshold[strategy_name], t,
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

        adjustThreshold(ads, strategy_name, adjustParamNum)

        print '\n\n\n'

    '''
        get strategy for current hashcode
    '''
    def strategy(self, hashcode):
        index = hashcode % 997
        index = index % 100
        return  self.cookie_strategy[index]


    def do(self):

        #self.init_ads()
        self.init_strategy()
        ads4simple = self.init_ads()
        adsList = []
        testNum = 20
        for i in range(0, testNum):
            ads = self.copy_ads(ads4simple)
            adsList.append(ads)

        i = 0
        while True:
            print 'round: ', i

            pv = Pv(random.randint(0, 1000))

            self.setAdsCtr(ads4simple)
            self.setAdsListCtr(ads4simple, adsList)

            ###default select
            self.selectAd(pv, ads4simple, self.t.simpleThreshold, 0, self.t.simpleAdjustThreshold, 0)

            ###using e select
            #for index in range(0, testNum):
            #    self.selectAd(pv, adsList[index], self.t.lastnumThreshold, (index+1)*20, self.t.simpleAdjustThreshold)

            ###weight adjust threshold
            for index in range(0, testNum):
                self.selectAd(pv, adsList[index], self.t.simpleThreshold, 0, self.t.weightedAdjustThreshold, 0.05*(index+1))
            i = i + 1
            if i >= 20000:
                break

        #evaluation

        ##E 
        titleList = []
        for index in range(0, len(adsList)):
            titleList.append(str((index+1)*20) + ' E Select')

        ##weigth 
        titleList = []
        for index in range(0, len(adsList)):
            titleList.append(str(0.05*(index+1)) + ' Weight Select')
        self.evals(ads4simple, 'Default Select', adsList, titleList)
        self.drawInOnePic(ads4simple, 'Default Select', adsList, titleList)
        self.draw(ads4simple, 'Default Select')
        #for ad in adsList:
        #    self.draw(ad, 'E Select')

        return 

    def draw(self, ads, testname):
        for ad in ads:
            for strategy in ad.ctrlog.keys():
                #self.drawPlot('retain vs retain', ad.ctrretain[strategy], ad.ctrfilter[strategy]) 
                print ad.name, strategy, testname
                self.evaluation(ad.ctrlog[strategy], ad.ctrretain[strategy], ad.ctrfilter[strategy], ad.theta)
                self.drawTwoPlot(ad.name+'-'+strategy+'-ctr', ad.ctrlog[strategy], 
                        ad.name+'-'+strategy+'-threshold', ad.thresholdlog[strategy], 
                        ad.name+'-'+strategy+'-usingthreshold', ad.usingthresholdlog[strategy])


    def drawPlot(self, title, data1, data2):
        plt.plot(data1, 'k')
        plt.plot(data2, 'g')
        plt.show()

    def drawTwoPlot(self, title1, data1, title2, data2, title3, data3):
        x1 = range(0, len(data1))
        x2 = range(0, len(data2))
        x3 = range(0, len(data3))
        
        y1 = data1
        y2 = data2
        y3 = data3
                   
        plt.subplot(3, 1, 1)
        #plt.plot(x1, y1, 'yo-')
        plt.plot(x1, y1)
        plt.title('A tale of 2 subplots')
        plt.ylabel(title1)
                        
        plt.subplot(3, 1, 2)
        plt.plot(x2, y2)
        plt.xlabel('time (s)')
        plt.ylabel(title2)

        plt.subplot(3, 1, 3)
        plt.plot(x3, y3)
        plt.xlabel('time (s)')
        plt.ylabel(title3)
        
        plt.show()


    def evals(self, ads, title, adsList, titleList):
        for ad in ads:
            for strategy in ad.ctrlog.keys():
                print ad.name, strategy, title
                self.evaluation(ad.ctrlog[strategy], ad.ctrretain[strategy], ad.ctrfilter[strategy], ad.theta)
        for i in range(0, len(adsList)):
            for ad in adsList[i]:
                for strategy in ad.ctrlog.keys():
                    print ad.name, strategy, titleList[i]
                    self.evaluation(ad.ctrlog[strategy], ad.ctrretain[strategy], ad.ctrfilter[strategy], ad.theta)

    '''
        only for on strategy
    '''
    def drawInOnePic(self, ads, title, adsList, titleList):
        strategy = 'strategy_baseline'
        l = len(adsList)
        col = math.ceil(math.sqrt(l+1))
        row = math.ceil(float(l+1)/col)
        print 'col:', col, ' row:', row

        x_ad = range(0, len(ads[0].usingthresholdlog[strategy]))

        plt.subplot(row, col, 1)
        plt.plot(x_ad, ads[0].usingthresholdlog[strategy])
        plt.xlabel('time (s)')
        plt.ylabel(title)

        for i in range(0, l):
            x = range(0, len(adsList[i][0].usingthresholdlog[strategy]))
            plt.subplot(row, col, i+2)
            plt.plot(x, adsList[i][0].usingthresholdlog[strategy])
            plt.xlabel('time (s)')
            plt.ylabel(titleList[i])
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
        print 'total pv num is: [', len(totallist), ']; theta is: [', theta, '], retain pro is: [', len(retainlist)*1.0/len(totallist), ']; key is: [', key, ']'
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





            
            









