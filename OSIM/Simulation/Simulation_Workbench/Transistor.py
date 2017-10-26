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
kemitterdirekt = 'e'
kemitter = '0'

v1 = Port([kbasis,kemitter], 'V1', 0.883, None)
v2 = Port([kv1,kemitter], 'V2', 1.6, None)
r1 = Resistor([kv1,kcollector],'R1',500,None)
re = Resistor([kemitterdirekt,kemitter],'RE',0.001,None)
npn = NPN_VBIC([kcollector,kbasis,kemitterdirekt,'SUB'], 'Q1', 0, None, pParams='NPN_VBIC_npn13G2.comp')
rsub = Resistor(['SUB','0'],"R3",264,None)
seq = CircuitSystemEquations([v1,v2,npn,r1,rsub,re])
#v1.setInnerImpedance(50)
ca = CircuitAnalyser(seq)

#for Nx in range(1,8):
    #seq.setParamterForComp("Q1","Nx",1)
    #npn.setParameterOrVariableValue("Nx", Nx)
    #ca.plot_lin(ca.getDCParamSweep('V2',-1,1.6,0.1,["Q1IT"],'V1',[0.8]))
res = ca.getACAnalysis_semilogx("V1",[kcollector],1,12,10)
ca.plot_semilogx(res[0])
#res = ca.getDCParamSweep('V2',0.01,1.6,0.01,["Q1IT"],'V1',[0.91])
#ca.plot_lin(res)
#res = ca.getSPAnalysis_semilogx(1,12,10,["V1"])
#ca.plot_smith(res)
res = res[0]

toFile = open("Betragsfrequenzgang_angepasst.csv", 'w')

for i in range(res[0].shape[1]):
	t = str((res[0])[0][i])
	plot = (res[0])[1][i]
	real = str(float(plot.real))
	imag = str(float(plot.imag))
	wline = "".join((t,",",str(plot),"\n"))
	#wline = "".join((real, " ", imag, "\n"))
	toFile.write(wline)

toFile.close()

#u.resToPGFPlotFile(res,"Eingangskennlinie")
