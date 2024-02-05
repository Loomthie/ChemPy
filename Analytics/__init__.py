import numpy as np
import pandas as pd


class StatisticalAnalysis:

    def __init__(self,dataset):
        self.data = sorted(dataset)
        self.avg = np.mean(dataset)
        self.median = np.median(dataset)
        self.size = len(dataset)
        self.stDev = np.std(self.data,ddof=1)
        self.var = np.var(self.data,ddof=1)
        self.coefVar = self.stDev/self.avg

        self.IQR = self.get_percentile(75)-self.get_percentile(25)
        self.range = self.data[-1]-self.data[0]

        self.lowerLimit = self.get_percentile(25)-1.5*self.IQR
        self.upperLimit = self.get_percentile(75)+1.5*self.IQR

    def __repr__(self):
        res = f'Size = {self.size:.0f}\nAverage = {self.avg:.2f}\nMedian = {self.median}\n' \
              f'IQR = {self.IQR:.2f}\nRange = {self.range:.2f}\nStandard Deviation = {self.stDev:.2f}\n' \
              f'Coefficeint of Variance = {self.coefVar*100:.2f}%\n' \
              f'Variance = {self.var:.2f}\nLower Limit = {self.lowerLimit:.2f}\nUpper Limit = {self.upperLimit:.2f}\n' \
              f''
        return res

    def get_percentile(self,per:float):
        per = per / 100
        indD = per * (self.size+1)-1

        ind = int(indD//1)
        dec = indD-ind

        return self.data[ind] + dec*(self.data[ind+1]-self.data[ind])

    def z_score(self,value):
        return (value-self.avg)/self.stDev


class TwoVarAnalysis:

    def __init__(self,x:list,y:list,ddof=1):
        self.x = x
        self.y = y

        xavg = np.mean(x)
        yavg = np.mean(y)

        self.covariance = sum([(xi-xavg)*(yi-yavg) for xi,yi in zip(x,y)])/(len(x)-ddof)

        self.statsX = StatisticalAnalysis(x)
        self.statsY = StatisticalAnalysis(y)

        self.correlation = self.covariance/(self.statsX.stDev*self.statsY.stDev)

        self.weightedAvg = sum([xi*yi for xi,yi in zip(x,y)])/sum(x)