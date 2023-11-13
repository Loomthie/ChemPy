import numpy as np
from ChemPy.Economics import Currency
from ChemPy.Measurements import *
from ChemPy.Economics.Modules import *


class _CapitalCost:
    pass


class Hills(_CapitalCost):

    class PlantType:
        SOLIDS='SOLIDS'
        SOLID_FLUID='SOLID-FLUID'
        FLUIDS = 'FLUIDS'

    class Siting:
        OUTDOORS='OUTDOORS'
        MIXED = 'MIXED'
        INDOORS = 'INDOORS'

    class Scale:
        MINOR = 'MINOR'
        MAJOR = 'MAJOR'
        GRASSROOTS = 'GRASS ROOTS'

    m = 0.6

    def __init__(self,production_rate:ProductionRate,modules:list[HillModule],plant_type=PlantType.SOLIDS,
                 siting=Siting.OUTDOORS,scale=Scale.MINOR,CE=800):

        self.prod_rate = production_rate
        self.prod_rate.convert_units('lbs/yr')
        self.F_pr = (self.prod_rate.value/1e7)**0.6
        self.CE = CE
        self.mods = modules

        self.plant_type = plant_type
        self.siting = siting
        self.scale = scale

        plant_type_dict = {
            self.PlantType.SOLIDS:1.85,
            self.PlantType.SOLID_FLUID:2.00,
            self.PlantType.FLUIDS:2.15
        }

        siting_dict = {
            self.Siting.OUTDOORS: 0.15,
            self.Siting.MIXED: 0.4,
            self.Siting.INDOORS: 0.8
        }

        scale_dict = {
            self.Scale.MINOR:0.1,
            self.Scale.MAJOR:0.3,
            self.Scale.GRASSROOTS:0.8
        }

        self.F_pt = plant_type_dict[plant_type]
        self.F_1 = siting_dict[siting]
        self.F_2 = scale_dict[scale]

        self.C_TBM = self.F_pt*self.CE/500*sum([i.calc_cost(self.F_pr) for i in self.mods])
        self.C_DPI = (1+self.F_1+self.F_2)*self.C_TBM
        self.C_TPI = self.C_DPI*1.5
        self.C_TCI = self.C_TPI*1.15




