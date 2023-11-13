import numpy as np
from ChemPy.Measurements import *
from ChemPy.Economics.Material import *
from ChemPy.Economics import Currency


class HillModule:

    def __init__(self,name,operating_pressure:Pressure,material:Material=CarbonSteel):

        self.pressure = operating_pressure
        self.material = material
        self.name = name

        self.Fp = (self.pressure.value/100)**0.25 if self.pressure.value>100 else 1
        self.Fm = self.material.Fm

    def calc_cost(self,Fpr):
        return Currency(Fpr*self.Fp*self.Fm*160e3)


class _Module:
    Fbm = 1
    Fd = 1
    Fp = 1

    def __init__(self,tag,desc,material=CarbonSteel):
        self.tag = tag
        self.desc = desc
        self.mat = material
        self.Fm = material.Fm

        self.base_cost = self._c_base()
        self.bm_cost = self._c_bm()

    @Currency.cit
    def _c_base(self):
        return 0

    @Currency.cit
    def _c_bm(self):
        return self.base_cost*(self.Fbm+(self.Fm*self.Fd*self.Fp-1))

    def __repr__(self):
        return f'tag              : {self.tag}\n' \
               f'Description      : {self.desc}\n' \
               f'Base Cost        : {self.base_cost}\n' \
               f'Bare Module Cost : {self.bm_cost}'


class _Pump(_Module):

    Fbm = 3.3

    __motor_types = {'open':1.0, 'enclosed':1.4, 'explosion proof':1.8}

    def __init__(self,tag,desc,vol_flow_rate:VolFlowRate,head:Distance,pump_power:Power,motor_type='open',
                 material=CarbonSteel,motor_Ft=None):

        self.Q = vol_flow_rate
        self.H = head
        self.Pt = pump_power

        self.Q.convert_units('gal/min')
        self.H.convert_units('ft')
        self.Pt.convert_units('hp')

        self.eta_p = -0.316+0.24015*np.log(self.Q.value)-0.01199*np.log(self.Q.value)**2
        self.Pb = self.Pt/self.eta_p
        self.eta_m = 0.8+0.0319*np.log(self.Pb.value)-0.00182*np.log(self.Pb.value)**2
        self.Pc = self.Pt/self.eta_m/self.eta_p

        assert motor_type in self.__motor_types
        self.motor_Ft = self.__motor_types[motor_type] if not motor_Ft else motor_Ft
        self.motor_cost = np.exp(5.9332+0.16829*np.log(self.Pc.value)-.110056*np.log(self.Pc.value)**2\
                                 +.071413*np.log(self.Pc.value)**3-0.0063788*np.log(self.Pc.value)**4)*self.motor_Ft

        super().__init__(tag,desc,material)


class CentrifugalPump(_Pump):

    def __init__(self,tag,desc,vol_flow_rate:VolFlowRate,head:Distance,pump_power:Power,motor_type='open',motor_Ft=None,
                 material=CarbonSteel,Ft=None):

        self.Q = vol_flow_rate
        self.H = head

        self.Q.convert_units('gpm')
        self.H.convert_units('ft')

        self.Ft = 1.0 if 50 <= self.Q.value <= 900 and 50 <= self.H.value <= 400 else \
            1.5 if 50 <= self.Q.value <= 3500 and 50 <= self.H.value <= 200 else \
                1.7 if 100 <= self.Q.value <= 1500 and 100 <= self.H.value <= 450 else \
                    2.0 if 250 <= self.Q.value <= 5e3 and 50 <= self.H.value <= 500 else \
                        2.7 if 50 <= self.Q.value <= 1.1e3 and 300 <= self.H.value <= 1.1e3 else \
                            8.9
        if Ft: self.Ft = Ft

        super().__init__(tag,desc,vol_flow_rate,head,pump_power,motor_type,material,motor_Ft)

    @Currency.cit
    def _c_base(self):
        self.S = self.Q*self.H**0.5
        Cb = np.exp(12.1656-1.1448*np.log(self.S)+.0862*np.log(self.S)**2)
        return self.Ft*self.Fm*Cb+self.motor_cost

