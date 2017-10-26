# Erstellt 12.01.2017 
#
# NPN Transistor -> Netzliste : Name Basis Emitter Collector __Parameter
#
from NPNTransportCurrent import NPNTransportCurrent
from OSIM.Modeling.AbstractComponents.CompositeComponent import CompositeComponent
from OSIM.Modeling.Components.Diode import Diode
from DiffusionCapacity import DiffusionCapacity
from JunctionCapacity import JunctionCapacity
from OSIM.Modeling.Components.Resistor import Resistor

class NPNTransistor_SGP(CompositeComponent):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(NPNTransistor_SGP, self).__init__(nodes, name, value, superComponent, **kwargs)

        self.b = self.nodes[1]
        self.c = self.nodes[0]
        self.e = self.nodes[2]

        self.bi = self.myName("bi")
        self.ci = self.myName("ci")
        self.ei = self.myName("ei")

        # Leckstrom-Dioden
        self.DL_E = Diode([self.bi, self.ei], self.myName("DL_E"), 0, self,dict=self.paramDict)
        self.DL_C = Diode([self.bi, self.ci], self.myName("DL_C"), 0, self,dict=self.paramDict)

        # PN-Uebergaenge
        self.DBE = Diode([self.bi, self.ei], self.myName("DBE"), 0, self,dict=self.paramDict)
        self.DBC = Diode([self.ei, self.ci], self.myName("DBC"), 0, self,dict=self.paramDict)

        # Transportstromquelle
        self.IT = NPNTransportCurrent([self.bi, self.ei, self.ci], self.myName("IT"), 0, self,dict=self.paramDict)

        # Sperrschicht-Kapatitaeten
        self.CS_Ce = JunctionCapacity([self.b, self.ci], self.myName("CS_Ce"), 0, self,dict=self.paramDict)
        self.CS_Ci = JunctionCapacity([self.bi, self.ci], self.myName("CS_Ci"), 0, self,dict=self.paramDict)
        self.CS_E = JunctionCapacity([self.bi, self.ei], self.myName("CS_E"), 0, self,dict=self.paramDict)

        # Diffusionskapazitateten
        #self.CD_I = DiffusionCapacity([self.bi, self.ei, self.ci], self.myName("CD_I"), 0, None, inverse=True)
        self.CD_N = DiffusionCapacity([self.bi, self.ei, self.ci], self.myName("CD_N"), 0, self,dict=self.paramDict)

        # Bahnwidestaende
        self.RB = Resistor([self.b, self.bi], self.myName("RB"), self.myParam("RB"), self, dict=self.paramDict)
        self.RC = Resistor([self.c, self.ci], self.myName("RC"), self.myParam("RC"), self, dict=self.paramDict)
        self.RE = Resistor([self.e, self.ei], self.myName("RE"), self.myParam("RE"), self, dict=self.paramDict)



