import numpy as np


class _Measurement:
    accepted_units = []
    alt_units = {}
    unit_convs = {}

    def convert_units(self,new_unit):
        if new_unit in self.alt_units:new_unit=self.alt_units[new_unit]
        assert new_unit in self.accepted_units
        self.value *= self.unit_convs[self.unit]/self.unit_convs[new_unit]
        self.unit = new_unit

    def __init__(self, value, unit):
        if unit in self.alt_units: unit = self.alt_units[unit]
        assert unit in self.accepted_units
        self.value = value
        self.unit = unit

    def __repr__(self, val=None):
        val = val if val else self.value
        return f'{val} {self.unit}'

    def __format__(self, format_spec):
        return self.__repr__(val=format(self.value, format_spec))

    def __mul__(self, other):
        if isinstance(other,_Measurement):
            return self.value*other.value
        else:
            return self.value*other

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, power, modulo=None):
        return self.value**power % modulo if modulo else self.value**power

    def __float__(self):
        return float(self.value)

    def __truediv__(self, other):
        if isinstance(other,_Measurement):
            return self.value/other.value
        else:
            return self.__class__(self.value/other,self.unit)


class _Rate(_Measurement):
    alt_units = {}
    accepted_units_time = ['s', 'min', 'hr', 'day', 'yr']
    unit_convs_time = {
        's':1,
        'min':60,
        'hr':3600,
        'day':3600*24,
        'yr':3600*25*365
    }

    def convert_units(self,new_unit):
        if new_unit in self.alt_units: new_unit = self.alt_units[new_unit]
        new_unit, new_unit_time = new_unit.split('/')
        super().convert_units(new_unit)
        assert new_unit_time in self.accepted_units_time
        self.value *= self.unit_convs_time[self.unit_time]/self.unit_convs_time[new_unit_time]
        self.unit_time = new_unit_time

    def __init__(self, value, unit):
        if unit in self.alt_units: unit = self.alt_units[unit]
        unit_mass,unit_time = unit.split('/')
        super().__init__(value, unit_mass)
        assert unit_time in self.accepted_units_time
        self.unit_time = unit_time

    def __repr__(self, val=None):
        val = val if val else self.value
        return f'{val} {"/".join([self.unit, self.unit_time])}'

    def __truediv__(self, other):
        if isinstance(other,_Measurement):
            return self.value/other.value
        else:
            return self.__class__(self.value/other,'/'.join([self.unit,self.unit_time]))


class ProductionRate(_Rate):
    accepted_units = ['lbs','kg']
    unit_convs = {
        'lbs':1,
        'kg':2.205
    }


class Pressure(_Measurement):
    accepted_units = ['psi']
    unit_convs = {'psi':1}


class VolFlowRate(_Rate):
    accepted_units = ['gal']
    alt_units = {'gpm':'gal/min'}
    unit_convs = {'gal':1}


class Distance(_Measurement):
    accepted_units = ['ft']
    unit_convs = {'ft':1}


class Power(_Rate):
    accepted_units = ['ftlbf']
    alt_units={'hp':'ftlbf/min'}
    unit_convs = {'ftlbf':1.0}

