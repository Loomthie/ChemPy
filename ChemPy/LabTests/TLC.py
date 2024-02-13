import urllib.request as re
import numpy as np
import scipy.stats as stats
import pandas as pd


class Spot:
    def __init__(self,rfValue,color="#ddd"):
        self.rfValue = rfValue
        self.color = color


class Series:

    def __init__(self,seriesName,*spots:Spot):
        self.name = seriesName
        self.spots = spots

    def __iter__(self):
        rfVals = [i.rfValue for i in self.spots]
        colors = [i.color for i in self.spots]
        return (i for i in [self.name,rfVals,colors])

    def __str__(self):
        return str(list(self))


class Plate:

    __templateFile = "https://raw.githubusercontent.com/Loomthie/ChemPy/master/LabTests/TLC_template.html"

    width = 200
    height = 500

    def __init__(self,Plate_Title,*args:Series):
        self.title = Plate_Title
        self.args = args

    def __repr__(self):
        return ""

    def _repr_html_(self):
        cnt = "".join([i.decode('utf-8') for i in re.urlopen(self.__templateFile)])
        tlcSpots = "[" + ",".join([str(i) for i in self.args]) + "]"
        return cnt.format(tlcSpots=tlcSpots,width=self.width,height=self.height,title=self.title)


class SeriesAvg:

    stats_mode = "t"

    def __init__(self,series_name, **spots:list[Spot]):
        self.seriesName = series_name
        self.spots = {}
        for key,val in spots.items():
            rfVals = [i.rfValue for i in val]
            self.spots[key] = [np.average(rfVals),val[0].color,
                               np.std(rfVals)/np.sqrt(len(rfVals)*(stats.t.ppf(0.95,len(rfVals)-1)
                                                                   if self.stats_mode == "t" else
                                                                   1.96))]

    def __iter__(self):
        return (i for i in [self.seriesName,[self.spots[key][0] for key in self.spots],[self.spots[key][1] for key in self.spots],
                            [self.spots[key][2] for key in self.spots]])

    def __str__(self):
        return str(list(self))


class PlateAvg:

    width = 200
    height = 500

    __templateFile = "https://raw.githubusercontent.com/Loomthie/ChemPy/master/LabTests/TLCAvg_template.html"

    def __init__(self,Plate_Title,*series_avgs:SeriesAvg):
        self.series = series_avgs
        self.title = Plate_Title

    def _repr_html_(self):
        # with open("TLCAvg_template.html",'r') as file:
        #     cnt = file.read().format(tlcSpots="[" + ",".join([str(i) for i in self.series]) + "]")

        cnt = "".join([i.decode('utf-8') for i in re.urlopen(self.__templateFile)])
        tlcSpots = "[" + ",".join([str(i) for i in self.series]) + "]"
        return cnt.format(tlcSpots=tlcSpots,width=self.width,height=self.height,title=self.title)

