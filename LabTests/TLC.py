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


class Plate:

    def __init__(self,*args:Series):
        self.args = args
