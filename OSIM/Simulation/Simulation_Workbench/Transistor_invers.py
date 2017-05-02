from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations
from OSIM.Simulation.CircuitAnalysis.CircuitAnalyser import CircuitAnalyser
from OSIM.Simulation.NetToComp import NetToComp

#seq = CircuitSystemEquations(NetToComp('Transistor_invers.net').getComponents())
#ca = CircuitAnalyser(seq)
#ca.plot_lin(ca.getDCParamSweep('V2',0,0.3,0.001,["Q1bi","Q1ci","Q1ei"],'V1',[0.85]))

seq = CircuitSystemEquations(NetToComp('Transistor_invers.net').getComponents())
ca = CircuitAnalyser(seq)
ca.plot_lin(ca.getDCParamSweep('V2',0,0.5,0.01,["Q1IT"],'V1',[0.85]))
