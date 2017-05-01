from Modeling.Components.VoltageSource import VoltageSource
from Modeling.Components.Impedance import Impedance
from Modeling.AbstractComponents.CompositeComponent import CompositeComponent
import re

class Port(CompositeComponent):

    def __init__(self, nodes, name, voltage, superComponent, **kwargs):
        super(Port, self).__init__(nodes, name, voltage, superComponent,**kwargs)

        self.innerImpedance = eval(self.paramDict.get("RIN","0.00001"))
        self.InnerNode = self.myName("PI")
        sp = re.split('P|V',name)
        self.idx = sp[1]

        self.V = VoltageSource([self.InnerNode, nodes[1]], self.myName("V"),voltage, self,**kwargs)
        self.RI = Impedance([self.InnerNode, nodes[0]], self.myName("RI"), self.innerImpedance, self,**kwargs)

    def containsNonlinearity(self):
        return False

    def changeMyVoltageInSys(self, v):
        self.value = v
        self.V.changeMyVoltageInSys(v)

    def myBranchCurrent(self):
        return self.RI.myBranchCurrent()

    def voltageOverMe(self):
        return self.RI.Udiff([self.nodes[0], self.nodes[1]])

    def setInnerImpedance(self,imp):
        self.innerImpedance = imp
        self.RI.setValue(imp)

    def getInnerImpedance(self):
        return 1/self.RI.getAdmittance([],0)
