import numpy as np
import pandas as pd
import scipy.stats as stats
import plotly.graph_objects as go
from ChemPy import HTMLDict


class ConfidenceInterval:

    plotly_layout = go.Layout(showlegend=False)

    def __init__(self, avg, conf, stDev):
        self.avg = avg
        self.conf = conf
        self.stDev = stDev
        self.CI = (avg - conf, avg + conf)

    def bell_curve(self, **kwargs):
        layout = go.Layout(**kwargs) if kwargs != {} else self.plotly_layout
        fig = go.Figure(layout=layout)
        x = np.linspace(self.avg - 4 * self.stDev, self.avg + 4 * self.stDev, 200)
        y = (1 / (self.stDev * np.sqrt(2 * np.pi))) * np.exp(-.5 * ((x - self.avg) / self.stDev) ** 2)
        fig.add_trace(go.Scatter(x=x, y=y))
        x = np.linspace(*self.CI, 100)
        y = (1 / (self.stDev * np.sqrt(2 * np.pi))) * np.exp(-.5 * ((x - self.avg) / self.stDev) ** 2)
        fig.add_trace(go.Scatter(x=x, y=y, fill='tozeroy'))
        return fig

    def _repr_html_(self):
        with open('ConfidenceIntervalTemplate.html','r') as file:
            cnt = file.read()
        return cnt.format_map(HTMLDict(bell_curve=self.bell_curve().to_html(),
                                       lowerLimit=self.CI[0],
                                       average=self.avg,
                                       upperLimit=self.CI[1]))
