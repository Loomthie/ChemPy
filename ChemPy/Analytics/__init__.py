import numpy as np
import pandas as pd
import scipy.stats as stats
import plotly.graph_objects as go


class ConfidenceInterval:

    layout = go.Layout(showlegend=False,width=500,height=500)
    def __init__(self,avg,std,size,alpha):
        self.avg = avg
        self.std = std
        self.alpha = alpha
        self.size = size

        p = 1-self.alpha/2
        self.confidence = stats.norm.ppf(p)*self.std/np.sqrt(self.size)

        self.interval = (self.avg-self.confidence,self.avg+self.confidence)

    def scatter_series(self,name,**kwargs):
        return go.Scatter(x=[name],y=[self.avg],error_y=dict(type='data',array=[self.confidence]),name=name,**kwargs)


class Dataset:
    class __FiveNumberSummary:

        def __init__(self, *args):
            self.min, self.q1, self.q2, self.q3, self.max = args

        def __repr__(self):
            res = {
                "Minimum": self.min,
                "1st Quartile": self.q1,
                "2nd Quartile (Median)": self.q2,
                "3rd Quartile": self.q3,
                "Maximum": self.max
            }

            return "\n".join([f'{key:>21} {value}' for key, value in res.items()])

    def __init__(self, name, dataset, ddof=1):
        self.name = name
        self.data = np.array(dataset)
        self.sorted_data = sorted(self.data)

        self.size = self.data.shape[0]

        self.avg = np.mean(self.data)
        self.median = np.median(self.data)
        self.stDev = np.std(self.data, ddof=ddof)
        self.variance = np.var(self.data, ddof=ddof)
        self.coefVariance = self.stDev / self.avg

        self.iqr = self.percentile(75) - self.percentile(25)

        self.min = min(self.data)
        self.max = max(self.data)
        self.range = self.max - self.min

        self.firstQuartile = self.percentile(25)
        self.thirdQuartile = self.percentile(75)

        self.fiveNumSum = self.__FiveNumberSummary(self.min, self.firstQuartile, self.median, self.thirdQuartile,
                                                   self.max)

    def percentile(self, per):
        per = per / 100
        indD = per * (self.size + 1) - 1

        ind = int(indD // 1)
        dec = indD - ind

        return self.sorted_data[ind] + dec * (self.sorted_data[ind + 1] - self.sorted_data[ind])

    def boxplot(self):
        fig = go.Figure()
        fig.add_trace(go.Box(x=self.data, name=self.name))

        return fig

    def __repr__(self):
        res = {
            "Dataset Name": self.name,
            "Average": self.avg,
            "Median": self.median,
            "Standard Deviation": self.stDev,
            "Variance": self.variance,
            "Coefficient of Variance": self.coefVariance,
            "Range": self.range
        }

        return "\n".join([f'{key:>23}: {val}' for key, val in res.items()])

    def _repr_html_(self):
        style = '''
        <style scoped>
            
        </style>
        '''

        body = f'''
        <table>
            <tr>
                <th colspan="2">{self.name}</th>
            </tr>
            <tr>
                <th>Average</th>
                <td>{self.avg}</td>
            </tr>
        </table>
        '''


class HypothesisTest:

    def __init__(self,Population:Dataset,*args:Dataset,alpha=.05):
        self.pop = Population
        self.args = args
        self.alpha = alpha

        self.pop_ci = ConfidenceInterval(self.pop.avg,self.pop.stDev,self.pop.size,alpha)
        self.args_ci = [ConfidenceInterval(i.avg,i.stDev,i.size,alpha) for i in self.args]

        self.results = pd.DataFrame(
            data=[
                [*self.pop_ci.interval,True],
                *[[*i_ci.interval,self.__run_test(i_ci)] for i_ci in self.args_ci]
            ],
            columns=['Lower Limit','Upper Limit','Result'],
            index=[self.pop.name,*[i.name for i in self.args]]
        )

    def __run_test(self,ci:ConfidenceInterval):
        if ci.interval[0] > self.pop_ci.interval[1] or ci.interval[1] < self.pop_ci.interval[0]:
            return False
        else:
            return True

    def fig(self,**kwargs):
        fig = go.Figure(layout=go.Layout(**kwargs))

        fig.add_trace(self.pop_ci.scatter_series(self.pop.name))

        for i in range(len(self.args)):
            fig.add_trace(self.args_ci[i].scatter_series(self.args[i].name))

        return fig