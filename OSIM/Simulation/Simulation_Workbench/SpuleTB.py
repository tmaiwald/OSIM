
from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations
from OSIM.Simulation.CircuitAnalysis.CircuitAnalyser import CircuitAnalyser
from OSIM.Simulation.NetToComp import NetToComp

seq = CircuitSystemEquations(NetToComp('Diverses/SpileTB.net').getComponents())

print(seq.A)

ca = CircuitAnalyser(seq)

#ca.calcDCOperatingPoint()

ca.plot_lin(ca.getTrans(0,3e-6,1e-9,["IN","OUT"]))
