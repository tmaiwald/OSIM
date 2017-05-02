from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations
from OSIM.Simulation.CircuitAnalysis.CircuitAnalyser import CircuitAnalyser
from OSIM.Simulation.NetToComp import NetToComp

seq = CircuitSystemEquations(NetToComp('DiffAmplifier/Diffamp.net').getComponents())
ca = CircuitAnalyser(seq)
ca.printDCOp(["R6","R3","VCurSource"])
#print(seq.x)
#max = np.amax(np.absolute(seq.x))
#print(max)
#ca.plot_lin(ca.getDCParamSweep('V1',1,3.3,0.05,["VoutPlus","VoutMinus"],'VCC',[3.3]))
ca.plot_semilogx(ca.getACAnalysis_semilogx("V1",["VoutPlus"],2,10,11)[0])
