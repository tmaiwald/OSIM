from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations
from OSIM.Modeling.Components.Port import Port
from OSIM.Modeling.Components.Resistor import Resistor
from OSIM.Modeling.Components.NPN_Vertical_Bipolar_Intercompany_Model.NPN_VBIC import NPN_VBIC
from OSIM.Simulation.CircuitAnalysis.CircuitAnalyser import CircuitAnalyser
from OSIM.Simulation.NetToComp import NetToComp
import OSIM.Simulation.Utils as u

kbasis = 'b'
kcollector = 'c'
kv1 = 'v1'
kemitter = '0'

v1 = Port([kbasis,kemitter], 'V1', 0.6, None)
v2 = Port([kv1,kemitter], 'V2', 0.6, None)
r1 = Resistor([kv1,kcollector],'R1',0.00001,None)
npn = NPN_VBIC([kcollector,kbasis,kemitter,kemitter], 'Q1', 0, None, pParams='NPN_VBIC_npn13G2.comp')
seq = CircuitSystemEquations([v1,v2,npn,r1])

ca = CircuitAnalyser(seq)

#ca.plot_lin(ca.getDCParamSweep('V2',-1,1.6,0.1,["Q1IT"],'V1',[0.8]))
res = ca.getDCParamSweep('V2',0,1.6,0.01,["R1"],'V1',[0.9])
ca.plot_lin(res)

#u.resToPGFPlotFile(res,"Eingangskennlinie")
