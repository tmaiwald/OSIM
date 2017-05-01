import cmath

from Simulation.Components.Capacity import Capacity

import Simulation.Utils as u
from Modeling.CircuitSystemEquations import CircuitSystemEquations


class DiffusionCapacity(Capacity):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(DiffusionCapacity, self).__init__(nodes, name, value, superComponent, **kwargs)

        self.inverse = False

        self.parseArgs(**kwargs)

        self.bi = nodes[0]
        self.ei = nodes[1]
        self.ci = nodes[2]
        self.Utau = eval(self.getMyParameterFromDictionary("Utau",self.paramDict,"10e10"))
        self.tau0 = eval(self.getMyParameterFromDictionary("tau0",self.paramDict,"10e-9"))
        self.xtau = eval(self.getMyParameterFromDictionary("xtau",self.paramDict,"40"))
        self.Is = eval(self.getMyParameterFromDictionary("Is",self.paramDict,"7e-15"))
        self.Ut = eval(self.getMyParameterFromDictionary("Ut",self.paramDict,"0.026"))
        self.Itau = eval(self.getMyParameterFromDictionary("Itau",self.paramDict,"0"))

    def setOPValues(self):
        self.calculateValue()
        self.opValues["C"] = self.value

    def calculateValue(self):
        a = 0
        b = 0
        Udlim = 2
        tau = 0
        ubmem = self.Udiff([self.bi, self.ei])[0]
        ubmcm = self.Udiff([self.bi, self.ci])[0]
        if(ubmem == 0 or ubmcm == 0):
            self.value = 0
            return
        if self.inverse is True:
            tau = self.tau0
            b = u.exp(ubmcm,1/self.Ut,Udlim)
        else:
            #        i
            # x = -------
            #     i + Itau
            if ubmcm > Udlim:
                m = (cmath.log(2)*2**(Udlim/self.Utau))/(self.Utau)
                n = 2**(Udlim/self.Utau)-m*Udlim
                a = m*ubmcm+n
            else:
                a = 2**(ubmcm/self.Utau)
            if ubmem > Udlim:
                m = 1/self.Ut *cmath.exp(Udlim/self.Ut)
                n = ((cmath.exp(Udlim /self.Ut)) - 1)-m*Udlim
                b = m*ubmem+n
            else:
                b = cmath.exp(ubmem/self.Ut)
                i = self.Is*(b-1)
                x = i/(i+self.Itau)
                tau = self.tau0*(1+self.xtau*(3*x**2-2*x**3)*a)

        self.value = (tau * self.Is/self.Ut) * b

    def doStep(self, freq_or_tau):
        if self.sys.atype in [CircuitSystemEquations.ATYPE_DC,CircuitSystemEquations.ATYPE_TRAN]:
            self.calculateValue()
        super(DiffusionCapacity, self).doStep(freq_or_tau)


    def containsNonlinearity(self):
        return True

    def parseArgs(self, **kwargs):
        super(DiffusionCapacity,self).parseArgs(**kwargs)

        for name, value in kwargs.items():
            if name == 'inverse':
                self.inverse = value
