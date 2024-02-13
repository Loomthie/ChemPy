import pandas as pd
import numpy as np
import plotly.graph_objects as go


class Correlation:

    def __init__(self,*args,names=None,ddof=1):

        self.args = args

        assert all([len(self.args[0])==len(i) for i in self.args[1:]])

        if not names:
            names = [f'Variable {i+1}' for i in range(len(self.args))]

        assert len(names)==len(self.args)

        self.names = names

        if len(args) < 2:
            raise ValueError("Need 2 or more variables")

        self.data = {f"{var}":arg for var,arg in zip(names,args)}
        self.avgs = {f"{key}":np.mean(val) for key,val in self.data.items()}
        self.stds = {f"{key}":np.std(val,ddof=ddof) for key,val in self.data.items()}

        self.covariance = pd.DataFrame(
            [[sum([(k-self.avgs[key1])*(l-self.avgs[key2])/(len(self.data[key1])-ddof) for k,l in zip(self.data[key1],self.data[key2])]
                  ) for key1 in self.names] for key2 in self.names],
            columns=self.names,
            index=self.names
        )

        self.coefCorr = pd.DataFrame(
            [[self.covariance[key1][key2]/(self.stds[key1]*self.stds[key2]) for key1 in self.names]
             for key2 in self.names],
            columns=self.names,
            index=self.names
        )