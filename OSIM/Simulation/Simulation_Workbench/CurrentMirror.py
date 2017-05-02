from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations
from OSIM.Simulation.CircuitAnalysis.CircuitAnalyser import CircuitAnalyser
from OSIM.Simulation.NetToComp import NetToComp

seq = CircuitSystemEquations(NetToComp('CurrentMirror/CurrentMirror.net').getComponents())
ca = CircuitAnalyser(seq)

ca.printDCOp(["R1","RL"])
dcs = ca.getDCOpAt(["VIN","N004"])
print(dcs)
print(dcs[1]-dcs[0])

ca.plot_lin(ca.getDCParamSweep('V2',0,3.3,0.05,["R2","R1"],'V1',[3.3]))

