import math
import numpy as np
from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations as ce
from OSIM.Modeling.Components.Capacity import Capacity

class Charge(Capacity):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(Charge, self).__init__(nodes, name, value, superComponent, **kwargs)
        self.charge = 0
        self.prevCharge = 0
        self.capacity = 0
        self.prevCapacity = 0
        self.ac_capacity = 0

    def doStep(self, freq_or_tau):
        self.performCalculations()
        myIdx = self.sys.compDict.get(self.name)
        [x1v,x2v] = self.insertAdmittanceintoSystem(freq_or_tau)

        if self.sys.atype == ce.ATYPE_TRAN:
            #tau = self.sys.tnow - self.sys.told
            #self.sys.b[myIdx] = (self.charge-self.prevCharge)#/tau
            adm = self.getAdmittance(self.nodes, freq_or_tau)
            self.sys.b[myIdx] = adm * (x1v - x2v)

    def getAdmittance(self, nodesFromTo, freq_or_tstep):
        '''
        if self.sys.atype == ce.ATYPE_TRAN:
            tau = self.sys.tnow - self.sys.told
            #return (self.capacity - self.prevCapacity)/tau
            return 0#(self.charge - self.prevCharge)

        return 0
        '''

        if self.sys.atype ==ce.ATYPE_TRAN:
            #return (self.dQdU_A()) / (self.sys.tnow - self.sys.told)
            return (self.ac_capacity)/(self.sys.tnow-self.sys.told)#
        if self.sys.atype == ce.ATYPE_DC:
            return 0
        else:
            return (np.complex128(1j * 2 * math.pi * freq_or_tstep * self.ac_capacity))


    def setOPValues(self):
        self.ac_capacity = self.dQdU_A()
        self.opValues["C"] = self.ac_capacity

    def dQdU_A(self):
        print("Abstract Charge - Implement it!")
        return 0

    def getCharge(self):
        print("Abstract Charge - Implement it!")

    def performCalculations(self):
        self.prevCharge = self.charge
        self.charge = self.getCharge()
        self.prevCapacity = self.capacity
        self.capacity = self.dQdU_A()

    def containsNonlinearity(self):
        return True

