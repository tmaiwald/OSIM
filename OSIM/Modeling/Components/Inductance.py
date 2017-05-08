import math

from OSIM.Modeling.AbstractComponents.SingleComponent import SingleComponent
from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations

class Inductance(SingleComponent):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(Inductance, self).__init__(nodes, name, value, superComponent, **kwargs)

    def doStep(self, freq_or_tau):
        myIdx = self.sys.compDict.get(self.name)
        self.insertAdmittanceintoSystem(freq_or_tau)
        if self.sys.atype == CircuitSystemEquations.ATYPE_TRAN:
            self.sys.b[myIdx] = -self.sys.xprev[myIdx]

    def getAdmittance(self, nodesFromTo, freq_or_tstep):

        if self.sys.atype == CircuitSystemEquations.ATYPE_TRAN:
            return (self.sys.tnow-self.sys.told)/self.value
        if freq_or_tstep == 0:
            return complex(1e256)
        return 1 / (1j * 2 * math.pi * freq_or_tstep * self.value)

    def initialSignIntoSysEquations(self): #TODO use function from Component.py
        algebraicSign = 1# Plus
        branchIdx = self.sys.compDict.get(self.name)
        for n in self.nodes:
            nodeIdx    = self.sys.compDict.get(n)
            if n is not '0':
                self.sys.A[nodeIdx, branchIdx] = algebraicSign*1
                self.sys.A[branchIdx, nodeIdx] = algebraicSign
                self.sys.b[branchIdx] = 0
            algebraicSign = algebraicSign*-1


    def setParameterValue(self,paramName,paramVal):
        if(paramName == "L"):
            self.value = paramVal
            return
        else:
            print(self.name+" ERROR: "+paramName+" unknown!!")

