#!/usr/local/bin/python
# -*- c ding: UTF-8 -*-

import sys
import random
import json
import numpy as np
import matplotlib.pyplot as plt

reload(sys)
sys.setdefaultencoding("utf-8")

class Threshold(object):

    '''
        using current threshold as threshold
    '''
    def simpleThreshold(self, thresholdlist, num=-1):
        return thresholdlist[-1]

    
    '''
        using e as threshold
    '''
    def eThreshold(self, thresholdlist, num):
        num = len(thresholdlist)
        return self.lastnumThreshold(thresholdlist, num)

    '''
        using the last num e as the threshold
    '''
    def lastnumThreshold(self, thresholdlist, num):
        l = len(thresholdlist)
        if l < num:
            return thresholdlist[-1]
        ll = len(thresholdlist[l-num:])
        t = sum(thresholdlist[l-num:]) / float(ll)
        return t
    
    '''
        using the last proportation num e as the threshold
    '''
    def lastproportionThreshold(self, thresholdlist, proportion):
        l = len(thresholdlog)
        ll = len(thresholdlist[l*proportion:])
        t = sum(thresholdlog[l*lastproportion:]) / float(l)
        return t


    def betaThreshold(self):
        return None







    '''
        adjust threshold by threshold*retain/theta
    '''
    def simpleAdjustThreshold(self, ads, strategy_name, alpha=0):
        print 'threshold adjust:'
        for ad in ads:
            ad.retainRate[strategy_name] = ad.selectedNum[strategy_name] * 1.0 / ad.candidateNum[strategy_name]
            if ad.retainRate[strategy_name] != 0.0:
                print ad.name, 'in ', strategy_name, ' threshold from ', ad.threshold[strategy_name],
                ad.threshold[strategy_name] = ad.threshold[strategy_name] * ad.retainRate[strategy_name] / ad.theta
                print ' to ', ad.threshold[strategy_name]
            if ad.threshold[strategy_name] >= 1.0:
                ad.threshold[strategy_name] = 1.0
            print ad.name, 'retain pro is', ad.retainRate[strategy_name], ' theta is', ad.theta, ' candidate num is', ad.candidateNum[strategy_name], ' selected num is', ad.selectedNum[strategy_name]
        print 'threshold adjusted finished'


    def weightedAdjustThreshold(self, ads, strategy_name, alpha):
        print 'threshold adjust:'
        for ad in ads:
            ad.retainRate[strategy_name] = ad.selectedNum[strategy_name] * 1.0 / ad.candidateNum[strategy_name]
            if ad.retainRate[strategy_name] != 0.0:
                print ad.name, 'in ', strategy_name, ' threshold from ', ad.threshold[strategy_name],
                ad.threshold[strategy_name] = ad.threshold[strategy_name]*alpha + ad.threshold[strategy_name] * ad.retainRate[strategy_name] / ad.theta * (1-alpha)
                print ' to ', ad.threshold[strategy_name]
                print 'alpha is: ', alpha
            if ad.threshold[strategy_name] >= 1.0:
                ad.threshold[strategy_name] = 1.0
            print ad.name, 'retain pro is', ad.retainRate[strategy_name], ' theta is', ad.theta, ' candidate num is', ad.candidateNum[strategy_name], ' selected num is', ad.selectedNum[strategy_name]
        print 'threshold adjusted finished'

    '''
    '''
    def MLEAdjustThreshold(self, ads):
        return None
        
if __name__ == "__main__":
    _sfp = sfp()
    _sfp.do()





            
            









