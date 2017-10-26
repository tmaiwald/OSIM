from Component import Component
from numba import jit

class CompositeComponent(Component):
    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(CompositeComponent, self).__init__(nodes, name, value, superComponent, **kwargs)
        self.internalComponents.remove(self)#unschoener hack

    def getAllInternalComponents(self):
        comps = list()
        for c in self.internalComponents:
            comps.append(c.internalComponents)
        return comps

    def initialSignIntoSysEquations(self):
        for c in self.internalComponents:
            c.initialSignIntoSysEquations()

    def setOPValues(self):
        for s in self.internalComponents:
            s.setOPValues()

    def printMyOPValues(self):
        for s in self.internalComponents:
            s.printMyOPValues()

    def myName(self, name):  # for sub-components
        return "".join((self.name, name))

    def myParam(self, p):
        ps = "".join((self.name, p))
        return self.paramDict.get(ps)

    @jit(nogil=True)
    def doStep(self, freq_or_tau):
        self.performCalculations()
        for c in self.internalComponents:
            c.doStep(freq_or_tau)
