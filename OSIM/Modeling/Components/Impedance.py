import numpy as np

from OSIM.Modeling.AbstractComponents.SingleComponent import SingleComponent
from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations

class Impedance(SingleComponent):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        if complex(value) == 0:
            print(name + " Resistor invalid value, will be is set to Rmin = 0.001")
            super(Impedance, self).__init__(nodes, name, 0.0000001, superComponent,**kwargs)
        else:
            super(Impedance, self).__init__(nodes, name, value, superComponent, **kwargs)

    def doStep(self, freq_or_tau):

        if self.sys.atype == CircuitSystemEquations.ATYPE_AC:
            return
        self.insertAdmittanceintoSystem(freq_or_tau)

    def getAdmittance(self, nodesFromTo, freq_or_tstep):
        return np.complex128(1 / self.value)
