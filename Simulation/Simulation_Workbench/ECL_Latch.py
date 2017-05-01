from Modeling.CircuitSystemEquations import CircuitSystemEquations
from Simulation.CircuitAnalysis.CircuitAnalyser import CircuitAnalyser
from Simulation.NetToComp import NetToComp

seq = CircuitSystemEquations(NetToComp('ECLLatch/ECLLatch.net').getComponents())
ca = CircuitAnalyser(seq)
ca.printDCOp(["R1","OUT+"])
