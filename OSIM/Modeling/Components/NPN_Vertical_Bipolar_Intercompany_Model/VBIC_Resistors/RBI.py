
import numpy as np
from OSIM.Modeling.Components.Resistor import Resistor

class RBI(Resistor):
    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(RBI, self).__init__(nodes, name, value, superComponent, **kwargs)
        if(self.COMPONENT_PRINT_WARNINGS):
            print (name+"Warning: currently implemented as a linear Component " \
                       "\n Should be implemented as a CurrentSource (S105 unten Berkner)")

        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec(variableExpr)

        self.rbi = eval(self.paramDict.get("rbi", "1"))

    def getAdmittance(self, nodesFromTo, freq_or_tstep):
        return self.superComponent.IT.getqb()/self.rbi

    def setParameterOrVariableValue(self, name, value):

        if(name == "R"):
            self.rbi = value
            self.insertAdmittanceintoSystem(0)
        else:
            print(self.name + " ERROR: " + name + " unknown!!")

    def reloadParams(self):
        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec (variableExpr)

        self.rbi = eval(self.paramDict.get("rbi", "1"))
