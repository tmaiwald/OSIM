from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations
from OSIM.Simulation.CircuitAnalysis.CircuitAnalyser import CircuitAnalyser
from OSIM.Simulation.NetToComp import NetToComp

seq = CircuitSystemEquations(NetToComp('ECLLatch/ECLLatch.net').getComponents())
ca = CircuitAnalyser(seq)
ca.printDCOp(["R1","OUT+"])
