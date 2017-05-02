
import numpy as np
from OSIM.Modeling.Components.Resistor import Resistor

class RBI(Resistor):
    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(RBI, self).__init__(nodes, name, value, superComponent, **kwargs)
        if(self.COMPONENT_PRINT_WARNINGS):
            print (name+"Warning: currently implemented as a Nonlinear Component " \
                       "\n Should be implemented as a CurrentSource (S105 unten Berkner)")

        self.rbi = value

    def getAdmittance(self, nodesFromTo, freq_or_tstep):
        return self.superComponent.IT.getqb()/self.rbi
