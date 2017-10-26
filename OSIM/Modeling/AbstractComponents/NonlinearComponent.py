
from OSIM.Modeling.AbstractComponents.SingleComponent import SingleComponent
from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations as c


class NonlinearComponent(SingleComponent):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(NonlinearComponent, self).__init__(nodes, name, value, superComponent, **kwargs)
        self.current = 0
        self.gd = 0
        self.alpha = 0.1

    def containsNonlinearity(self):
        return True

    def getAdmittance(self, nodesFromTo, freq_or_tstep):
        return 0

    def setOPValues(self):
        self.performCalculations()
        self.opValues["gd"] = self.gd

    def doStep(self, freq_or_tau):
        if self.sys.atype == c.ATYPE_AC:
            return
        if self.sys.atype in [c.ATYPE_DC,c.ATYPE_TRAN]:
            self.performCalculations()
            self.sys.g[self.bIdx] = self.current
            if self.nodes[0] is not '0':
                self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.nodes[0]), self.gd+self.sys.GMIN)
            if self.nodes[1] is not '0':
                self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.nodes[1]), -self.gd-self.sys.GMIN)


