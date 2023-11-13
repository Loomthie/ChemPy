import numpy as np
from scipy.integrate import solve_ivp
import plotly.graph_objects as go
import xlwings as xl


class BinaryDistillationTower:

    NT = 0
    NF = 0

    F = 0
    zF = 0
    qF = 0

    weir_const = 1.0
    tray_holdup = 0.1
    reboiler_holdup = 0.5
    condenser_holdup = 0.5
    Kc = 0

    D = 0
    R = 1

    alpha=0

    def __init__(self,**kwargs):
        for key,value in kwargs.items():
            self.__dict__[key] = value

    def eqy(self,eqx):
        return eqx * self.alpha/(1+eqx*(self.alpha-1))

    def run_simulation(self, tend=100, y0=None):

        def rhs(t, vec):
            m, x = np.split(vec, 2)

            y = self.eqy(x)

            Vrec = self.D * (self.R + 1)
            Vstr = Vrec - self.F * (1 - self.qF)
            V = np.r_[np.repeat(Vstr, self.NF), np.repeat(Vrec, self.NT - self.NF + 1), 0.]

            L = np.zeros_like(m)
            L[0] = self.F - self.D + self.Kc * (m[0] - self.reboiler_holdup)
            L[1:-1] = self.weir_const * (m[1:-1] - self.tray_holdup) ** 1.5
            L[-1] = self.D * self.R

            dm = np.zeros_like(m)
            dm[0] = L[1] - V[0] - L[0]
            dm[1:-1] = V[:-2] + L[2:] - V[1:-1] - L[1:-1]
            dm[-1] = V[-2] - L[-1] - self.D  # always 0 for perfect reboiler control
            dm[self.NF] += self.F

            dmx = np.zeros_like(m)
            dmx[0] = x[1] * L[1] - V[0] * y[0] - x[0] * L[0]
            dmx[1:-1] = y[:-2] * V[:-2] + x[2:] * L[2:] - V[1:-1] * y[1:-1] - x[1:-1] * L[1:-1]
            dmx[-1] = y[-2] * V[-2] - x[-1] * (L[-1] + self.D)
            dmx[self.NF] += self.F * self.zF

            dx = (dmx - x * dm) / m

            return np.r_[dm, dx]

        Vrec = self.D * (self.R + 1)
        Vstr = Vrec - self.F * (1 - self.qF)

        L_init = np.r_[self.F - self.D, np.repeat(Vstr - self.F + self.D, self.NF),
                       np.repeat(self.D * self.R, self.NT - self.NF + 1)]

        m_init = np.r_[self.reboiler_holdup,
                       (L_init[1:-1] / self.weir_const) ** (2 / 3) + self.tray_holdup,
                       self.condenser_holdup]

        x_init = np.repeat(self.zF, self.NT + 2)

        y0 = y0 if y0 is not None else np.r_[m_init, x_init]

        return solve_ivp(rhs, (0, tend), y0,
                         method='Radau', dense_output=True)

    def mccabe_thiele_plot(self,mcx):
        xplot = np.linspace(0, 1, 101)
        y = self.eqy(xplot)

        mcy = self.eqy(mcx)

        mcx = np.repeat(mcx, 2)
        mcy = np.repeat(mcy, 2)

        mcy[1:] = mcy[:-1]

        mc = np.c_[mcx, mcy][1:-1]

        layout = go.Layout(
            width=600, height=600,
            template='plotly_dark',
            showlegend=False
        )

        fig = go.Figure(layout=layout)

        fig.add_trace(go.Scatter(x=xplot, y=y, mode='lines'))
        fig.add_trace(go.Scatter(x=mc[:, 0], y=mc[:, 1], mode='lines'))
        fig.add_trace(go.Scatter(x=mc[1:-1:2, 0], y=mc[1:-1:2, 1], mode='lines'))

        return fig



    def export_to_excel(self):
        pass

