import numpy as np

from OSIM.Modeling.Components.Capacity import Capacity
from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations

class JunctionCapacity(Capacity):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(JunctionCapacity, self).__init__(nodes, name, value, superComponent, **kwargs)

        self.parseArgs(**kwargs)

        self.fak = eval(self.getMyParameterFromDictionary("fak",self.paramDict,"1"))
        self.Udifu = eval(self.getMyParameterFromDictionary("Udifu",self.paramDict,"0.5"))
        self.CS0 = eval(self.getMyParameterFromDictionary("CS0",self.paramDict,"0"))
        self.ms = eval(self.getMyParameterFromDictionary("ms",self.paramDict,"0.5"))
        self.fs = eval(self.getMyParameterFromDictionary("fs",self.paramDict,"0.5"))

    def setOPValues(self):
        self.calculateValue()
        self.opValues["C"] = self.value

    def calculateValue(self):

        Ud = np.absolute((self.Udiff(self.nodes))[0])
        if Ud <= self.fs*self.Udifu:
            self.value =self.fak*(self.CS0/(1-Ud/self.Udifu)**self.ms)
            return
        #           a
        # fak*CS0 ------
        #           b
        a = 1-self.fs*(1+self.ms)+(self.ms*Ud/self.Udifu)
        b = (1-self.fs)**(1+self.ms)
        self.value = self.fak*self.CS0*(a/b)

    def doStep(self, freq_or_tau):
        if self.sys.atype == CircuitSystemEquations.ATYPE_DC:
            self.calculateValue()
        super(JunctionCapacity, self).doStep(freq_or_tau)

    def containsNonlinearity(self):
        return True


