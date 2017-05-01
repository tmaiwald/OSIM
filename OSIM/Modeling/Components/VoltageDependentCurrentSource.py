
from Modeling.Components.CurrentSource import CurrentSource

class VoltageDependentCurrentSource(CurrentSource):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(VoltageDependentCurrentSource, self).__init__(nodes, name, value, superComponent, **kwargs)
        self.observeNodes = observeNodes

    def getCurrent(self):
        u = self.Udiff(self.observeNodes)
        return u*self.value
