# Erstellt 12.01.2017 
#
# SingleComponent -> Netzliste : Name Startnode Endnode __Parameter
#
#
from OSIM.Modeling.AbstractComponents.Component import Component

class SingleComponent(Component):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(SingleComponent, self).__init__(nodes, name, value, superComponent, **kwargs)
        self.fromNodeName = nodes[0]
        self.toNodeName   = nodes[1]

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value
        #self.initialSignIntoSysEquations()
        self.insertAdmittanceintoSystem(0)

    def calculateValue(self):
        self.value = self.value

