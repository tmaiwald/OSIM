from Simulation.Components.CurrentSource import CurrentSource

class CurrentDependentCurrentSource(CurrentSource):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(CurrentDependentCurrentSource, self).__init__(nodes, name, value, superComponent, **kwargs)
        self.observecomp = observecomp
        self.value = currentAmpl

    def getCurrent(self):
        return self.value*self.observecomp.myBranchCurrent(self.observecomp.name)
