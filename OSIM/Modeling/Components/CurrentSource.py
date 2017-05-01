import warnings

from Modeling.AbstractComponents.SingleComponent import SingleComponent

class CurrentSource(SingleComponent):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(CurrentSource, self).__init__(nodes, name, value, superComponent, **kwargs)

    def doStep(self, freq_or_tau):
        warnings.warn("CurrentSource: Not well implemente !!", DeprecationWarning)
        self.sys.b[self.sys.compDict.get(self.name)] = -self.getCurrent()

    def initialSignIntoSysEquations(self):
        super(CurrentSource, self).initialSignIntoSysEquations()
        self.sys.b[self.sys.compDict.get(self.name)] = -self.getCurrent()

    def getCurrent(self):
        return self.value

    def getAdmittance(self, nodesFromTo, freq_or_tstep):
        return 0
