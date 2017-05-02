from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations
from OSIM.Simulation.CircuitAnalysis.CircuitAnalyser import CircuitAnalyser
from OSIM.Simulation.NetToComp import NetToComp

seq = CircuitSystemEquations(NetToComp('twoTrans.net').getComponents())
ca = CircuitAnalyser(seq)
ca.printDCOp(["R1"])
#ca.plot_lin(ca.getDCParamSweep('V1',0.7,1.3,0.005,["VoutMinus","VoutPlus"],'VCC',[2.3]))
