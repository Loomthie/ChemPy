import numpy as np


class DataSet:
    """
        Represents a 1 dimension dataset

        Attributes:
            data (numpy array): represents the actual datapoints
            avg (float): average of the datapoints

        Methods:
            args(*data):
                Allows user to input data element wise

                *data (float): datapoints
    """

    def __init__(self,data: iter):
        self.data = np.array(data)
        self.avg = np.mean(self.data)

    @classmethod
    def args(cls,*data: float):
        return cls(data=data)


class LinearTrend:
    """
        Represents a Linear trend based on two datasets

        Attributes:
            x (DataSet): Dataset for the Independent Variable (x)
            y (DataSet): Dataset for the Dependent Variable (y)
            coefs (numpy array): m,b value for the linear model
            r2 (float): R2 value measuring correlation

        Methods:
            model(x):
                Model of the line of best fit for the x and y datasets

                x (float): x value to determine estimate of the corresponding y value
    """

    def __init__(self,x:DataSet,y:DataSet):
        self.x = x
        self.y = y

        a = np.c_[x.data,np.ones_like(x.data)]
        b = np.r_[y.data]

        self.coefs = np.linalg.solve(a.T @ a, a.T @ b)
        self.model = lambda x: self.__model(x,*self.coefs)

        self.r2 = 1 - np.sum((self.y.data - self.model(self.x.data))**2)/np.sum((self.y.data-self.y.avg)**2)

    def __model(self,x,a,b):
        return a*x+b

    def __repr__(self):
        eq = f"y = {self.coefs[0]:.2f}x + {self.coefs[1]:.2f}" if self.coefs[1] > 0 else\
            f"y = {self.coefs[0]:.2f}x - {-self.coefs[1]:.2f}"
        return f'''{eq}
R2 = {self.r2:.4f}'''
