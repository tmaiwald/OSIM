# Erstellt 12.01.2017
#
# NPN Transistor -> Netzliste : Name Basis Emitter Collector __Parameter
#


from NPNTransportCurrent import NPNTransportCurrent
from Simulation.AbstractComponents.CompositeComponent import CompositeComponent
from Simulation.Components.Diode import Diode
from Simulation.Components.NPN_Gummel_Poon_Model.DiffusionCapacity  import DiffusionCapacity
from Simulation.Components.NPN_Gummel_Poon_Model.JunctionCapacity import JunctionCapacity
from Simulation.Components.Resistor import Resistor


class NPNEasy_SGP(CompositeComponent):
    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(NPNEasy_SGP, self).__init__(nodes, name, value, superComponent, **kwargs)

        self.paramdict = self.readParams("__Parameter/NPN_Gummel_BC547B.comp")
        self.baseNode = self.nodes[1]
        self.collectorNode = self.nodes[0]
        self.emitterNode = self.nodes[2]


        self.innerBaseNode = self.myName("B'")
        self.innerCollectorNode = self.myName("C'")
        self.innerEmitterNode = self.myName("E'")

        # Sperrschicht-Kapatitaeten
        self.CS_Ce = JunctionCapacity([self.baseNode, self.collectorNode], self.myName("CS_Ce"), self.paramdict, self)
        self.CS_Ci = JunctionCapacity([self.baseNode, self.collectorNode], self.myName("CS_Ci"), self.paramdict, self)
        self.CS_E = JunctionCapacity([self.baseNode, self.emitterNode], self.myName("CS_E"), self.paramdict, self)


        # PN-Uebergaenge
        #self.DBE = Diode([self.baseNode, self.emitterNode], self.myName("DBE"), self.paramdict)
        self.DBE = Resistor([self.baseNode, self.emitterNode], self.myName("DBE"), 10e3, self)
        self.DBC = Diode([self.baseNode, self.collectorNode], self.myName("DBC"), self.paramdict, self)

        # Leckstrom-Dioden
        self.DL_E = Diode([self.baseNode, self.emitterNode], self.myName("DL_E"), self.paramdict, self)

        # Transportstromquelle
        self.IT = NPNTransportCurrent([self.collectorNode, self.emitterNode], self.myName("IT"),
                                      [self.baseNode, self.emitterNode, self.collectorNode], self)

        self.C_DN = DiffusionCapacity([self.baseNode, self.collectorNode], [self.baseNode, self.emitterNode],
                                      [self.baseNode, self.emitterNode], self)


    def doStep(self, freq_or_tau):
        for c in self.internalComponents:
            c.doStep(freq_or_tau)

    def containsNonlinearity(self):
        return True
