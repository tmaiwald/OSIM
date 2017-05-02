
from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations
from OSIM.Simulation.CircuitAnalysis.CircuitAnalyser import CircuitAnalyser
from OSIM.Simulation.NetToComp import NetToComp

seq = CircuitSystemEquations(NetToComp('Diverses/PlusTest.net').getComponents())
ca = CircuitAnalyser(seq)

ca.plot_lin(ca.getTrans(0,4e-6,1e-9,["VIN","VOUT"]))

ca.plot_lin(ca.getTrans(0,4e-6,1e-9,["VIN","VOUT"]))
