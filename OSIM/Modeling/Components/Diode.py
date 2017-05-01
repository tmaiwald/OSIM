import numpy as np
from numba import jit

import Simulation.Utils as u
from Modeling.AbstractComponents.NonlinearComponent import NonlinearComponent


# Is = Sperrsaettigungsstrom
# Ut = Temperaturspannung = Boltzmannkonstante*Temperatur/Elementarladung
# I_SR = Leck-Saettigungsstrom
# nr = Emissionskoeffizient in Sperrrichtung
# Udifu = Diffusionsspannung am PN-Uebergang
# ms = Kapazitaetskoeffizient

class Diode(NonlinearComponent):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(Diode, self).__init__(nodes, name, value, superComponent, **kwargs)

        if not value in["",0,[]]:
            print ("Diode-Warning: setting a value has no influence")

        '''
        Default path:
        '''

        self.Is = eval(self.paramDict.get("Is","0"))
        self.n = eval(self.paramDict.get("n", "2"))
        self.ms = eval(self.paramDict.get("ms","0.5"))
        self.Udifu = eval(self.paramDict.get("Udifu", "0.7"))
        self.Ut = eval(self.paramDict.get("Ut", "0.026"))
        self.B = eval(self.paramDict.get("B","1"))#correction factor
        self.kathode = nodes[1]
        self.anode = nodes[0]
        self.Udlim = eval(self.paramDict.get("Udlim","1"))#correction factor


    def setOPValues(self):
        self.performCalculations()
        self.opValues["gd"] = self.gd

    @jit
    def performCalculations(self):

        Ud = self.Udiff(self.nodes)

        if Ud < 0:
            # Strom:
            expo = u.exp(Ud[0],1/(self.n * self.Ut),-self.Udlim)
            ausdr = ((1 - (Ud[0] / self.Udifu)) ** 2 + 5e-3) ** (self.ms / 2)
            self.current = (self.Is * (expo - 1) * ausdr)

            # Differentieller Leitwert: TODO ueberpruefen !
            # a * b^(ms/2)
            # ------------- * d
            #     c
            a = self.ms * (Ud[0] - self.Udifu)
            b = (Ud[0] * (Ud[0] - 2 * self.Udifu)) / self.Udifu ** 2
            c = Ud[0] * (2 * self.Udifu - Ud[0])
            d = self.Is * np.exp(Ud[0] / (self.n * self.Ut)) / (self.n * self.Ut)
            self.gd = ((a * b ** (self.ms / 2) / c) * d)

        # Schockley Equation:
        self.current = self.Is/self.B * (u.exp(Ud[0],1/(self.Ut * self.n), self.Udlim)-1)
        self.gd = self.Is/self.B * u.dexp(Ud[0],1/(self.Ut * self.n), self.Udlim)

    @staticmethod
    def curr(FAK, IS, exp, expfak):
        return FAK*IS*(u.exp(exp,expfak,1.5)-1)

    @staticmethod
    def gdiff(current, n, ut):
        return current/(n*ut)
