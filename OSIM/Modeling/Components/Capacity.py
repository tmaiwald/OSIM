import math
from OSIM.Modeling.AbstractComponents.SingleComponent import SingleComponent
from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations

class Capacity(SingleComponent):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(Capacity, self).__init__(nodes, name, value, superComponent, **kwargs)

    def doStep(self, freq_or_tau):
        myIdx = self.sys.compDict.get(self.name)
        [x1v,x2v] = self.insertAdmittanceintoSystem(freq_or_tau)
        if self.sys.atype == CircuitSystemEquations.ATYPE_TRAN:
            adm = self.getAdmittance(self.nodes, freq_or_tau)
            self.sys.b[myIdx] = adm * (x1v - x2v)

    def getAdmittance(self, nodesFromTo, freq_or_tstep):
        #TODO fuer nummerische Stabilitaet einen kleinen Leitwert parallel schalten
        if self.sys.atype == CircuitSystemEquations.ATYPE_TRAN:
            return self.value/(self.sys.tnow-self.sys.told)
        else:
            return (1j * 2 * math.pi * freq_or_tstep * self.value)

    def setParameterOrVariableValue(self, name, value):
        if (name == "C"):
            self.value = value
            return
        else:
            print(self.name + " ERROR: " + name + " unknown!!")

