from Modeling.CircuitSystemEquations import CircuitSystemEquations
from Simulation.CircuitAnalysis.CircuitAnalyser import CircuitAnalyser
from Simulation.NetToComp import NetToComp
import Simulation.Utils as u

seq = CircuitSystemEquations(NetToComp('Transistor/Transistor.net').getComponents())

ca = CircuitAnalyser(seq)
dcs = ca.getDCOpAt(["1","IN"])

#ca.plot_lin(ca.getDCParamSweep('V2',-1,1.6,0.1,["Q1IT"],'V1',[0.8]))
#res = ca.getDCParamSweep("V2",0,1.6,0.01,["Q1IT"],'V1',[0.9])
res = ca.getDCParamSweep("V1",0,0.85,0.01,["Q1IBE"],'V2',[1.2])

ca.plot_lin(res)

u.resToPGFPlotFile(res,"Eingangskennlinie")
