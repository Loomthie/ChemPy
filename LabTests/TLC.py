import urllib.request as re
from IPython.display import display_html


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

    def __init__(self,*args:Series):
        self.args = args

    def __repr__(self):
        return ""

    def _repr_html_(self):
        cnt = "".join([i.decode('utf-8') for i in re.urlopen(self.__templateFile)])
        tlcSpots = "[" + ",".join([str(i) for i in self.args]) + "]"
        return cnt.format(tlcSpots=tlcSpots)

