
import numpy as np
from OSIM.Modeling.Components.Resistor import Resistor
from OSIM.Modeling.AbstractComponents.NonlinearComponent import NonlinearComponent
from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations

class RBI(NonlinearComponent):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(RBI, self).__init__(nodes, name, value, superComponent, **kwargs)
        if(self.COMPONENT_PRINT_WARNINGS):
            print (name+"Warning: currently implemented as a linear Component " \
                       "\n Should be implemented as a CurrentSource (S105 unten Berkner)")

        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec(variableExpr)

        self.current = 0
        self.g = 0
        self.dc_qb = 0

        self.rbi = eval(self.paramDict.get("rbi", "1"))

    def setParameterOrVariableValue(self, name, value):
        print(self.name + " ERROR: " + name + " unknown!!")

    def containsNonlinearity(self):
        return True

    def doStep(self, freq_or_tau):

        self.performCalculations()

        if self.sys.atype == CircuitSystemEquations.ATYPE_DC:
            self.sys.g[self.sys.compDict.get(self.name)] = self.current
            self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.nodes[0]), self.g)
            self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.nodes[1]), -self.g)
            return

        if self.sys.atype == CircuitSystemEquations.ATYPE_AC:
            self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.nodes[0]), self.g)
            self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.nodes[1]), -self.g)
            return

        if self.sys.atype == CircuitSystemEquations.ATYPE_TRAN:
            self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.nodes[0]), self.g)
            self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.nodes[1]), -self.g)

    def performCalculations(self):

        if self.sys.atype == CircuitSystemEquations.ATYPE_AC:
            pass

        if self.sys.atype == CircuitSystemEquations.ATYPE_DC:
            A = self.sys.getSolutionAt(self.nodes[0])
            B = self.sys.getSolutionAt(self.nodes[1])
            self.dc_qb = self.superComponent.IT.getqb()
            self.current = (A-B)*self.dc_qb/self.rbi
            self.g = self.dc_qb/self.rbi

        if self.sys.atype == CircuitSystemEquations.ATYPE_TRAN:
            pass


    def reloadParams(self):
        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec (variableExpr)

        self.rbi = eval(self.paramDict.get("rbi", "1"))
