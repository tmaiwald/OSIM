import numpy as np

from OSIM.Modeling.AbstractComponents.SingleComponent import SingleComponent
from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations

class Resistor(SingleComponent):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        if float(value) == 0:
            print(name + " Resistor invalid value, will be is set to Rmin = 0.001")
            super(Resistor, self).__init__(nodes, name, 0.0000001, superComponent,**kwargs)
        else:
            super(Resistor, self).__init__(nodes, name, value, superComponent, **kwargs)

        if(self.COMPONENT_PRINT_WARNINGS):
            print ("Resistor: #TODO: eigentlich ineffizient das bei jedem Step die Admittanz einzutragen - reicht eigentlich einmal initial"+
                   " kann man das optimieren ?")

    def doStep(self, freq_or_tau):
        if self.sys.atype == CircuitSystemEquations.ATYPE_AC:
            return
        self.insertAdmittanceintoSystem(freq_or_tau)

    def setParameterOrVariableValue(self, name, value):
        if(name == "R"):
            self.value = value
            self.insertAdmittanceintoSystem(0)
        else:
            print(self.name + " ERROR: " + name + " unknown!!")

    def getAdmittance(self, nodesFromTo, freq_or_tstep):
        return np.float64(1 / self.value)
