import numpy as np


class Currency:

    mode = None

    def xl_number_format(self):
        return f'{self.unit} 0.00{"".join(self.mode*[","])} "{"".join(self.mode*["M"])}";(Red)({self.unit} 0.00{"".join(self.mode*[","])} "{"".join(self.mode*["M"])}")'

    @classmethod
    def cit(cls,f):

        def new_f(*args):
            res = f(*args)
            if isinstance(res,Currency):
                return res
            else:
                return Currency(res)

        return new_f

    def __init__(self,value,unit='$',mode=None):

        self.value = value
        self.unit = unit

        if mode: self.mode = mode
        elif not self.mode: self.mode = np.log(np.abs(self.value)) // np.log(1e3) if self.value != 0 else 0

        self.mode = int(self.mode)

    def __repr__(self):
        return f'{self.unit} {self.value/(1e3**self.mode):0.2f} {"".join(self.mode*["M"])}' if self.value >= 0 else\
                f'({self.unit} {self.value/(1e3**self.mode):0.2f} {"".join(self.mode*["M"])})'

    def __format__(self, format_spec):
        if format_spec == '':
            format_spec='.2f'
        return f'{self.unit} {format(self.value / (1e3 ** self.mode),format_spec)} {"".join(self.mode * ["M"])}' if self.value >= 0 else \
            f'({self.unit} {format(self.value / (1e3 ** self.mode),format_spec)} {"".join(self.mode * ["M"])})'

    def __add__(self, other):
        return Currency(self.value+other.value,self.unit) if isinstance(other,Currency) else Currency(self.value+other,self.unit)

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        return Currency(self.value*other,self.unit)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return Currency(self.value/other,self.unit)

    def __rtruediv__(self, other):
        return Currency(other/self.value,self.unit)