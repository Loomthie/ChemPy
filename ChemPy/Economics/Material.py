
class Material:
    def __init__(self,name,Fm):
        self.name = name
        self.Fm = Fm


CarbonSteel = Material('Carbon Steel',1.0)
Copper = Material('Copper',1.2)
StainlessSteel = Material('Stainless Steel',2.0)
NickelAlloy = Material('Nickel Alloy',2.5)
TitaniumClad = Material('Titanium Clad',3.0)