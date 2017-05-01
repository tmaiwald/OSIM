from Modeling.CircuitSystemEquations import CircuitSystemEquations
from Simulation.CircuitAnalysis.CircuitAnalyser import CircuitAnalyser
from Simulation.NetToComp import NetToComp

seq = CircuitSystemEquations(NetToComp('Transistor/TransDiode.net').getComponents())
ca = CircuitAnalyser(seq)

#ca.printDCOp(["R1","R2","Q1IT"])
#dcs = ca.getDCOpAt(["Q_BC","Q_E"])
#print(dcs)
#print(dcs[1]-dcs[0])
#print (seq.compDict)
#np.set_printoptions(precision=1)
#print(seq.A.real)
#print("#############")
#print(seq.b.real)
#print("#############")
#print(seq.g.real)

ca.plot_lin(ca.getDCParamSweep('V1',0.0,3.3,0.01,["Q1IT"],'bla',[3.3]))
#ca.plot_lin(ca.getDCParamSweep('V1',0.6,1,0.001,["Q1IT"],'bla',[3.3]))

