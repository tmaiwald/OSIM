from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations
from OSIM.Simulation.CircuitAnalysis.CircuitAnalyser import CircuitAnalyser
from OSIM.Simulation.NetToComp import NetToComp
import numpy as np

seq = CircuitSystemEquations(NetToComp('LoBuffer/LoBuffer.net').getComponents())
ca = CircuitAnalyser(seq)
#ca.printDCOp(["R11","Cur2Out","IN1","Q7IT","Q4IT","Q3IT"])
#ca.plot_semilogx(ca.getACAnalysis_semilogx("V2",["OUT1"],1,12,10)[0])
#ca.plot_smith(ca.getSPAnalysis_semilogx(2,12,10,["V2"]))


res = ca.getTrans(0,3e-6,1e-9,["OUT2","OUT1","Cur2Out"])

# how to get a diff-Signal
out = np.zeros((2,res[0].shape[1]),dtype = np.float64)
for i in range(res[0].shape[1]):
    out[0][i] = (res[0])[0][i]
    out[1][i] = (res[0])[1][i] - (res[0])[2][i]

ca.plot_lin([out,["diffout"],"transient"])

print("Max %G "%np.amax(np.absolute(out[1][:])))

ca.plot_lin(res)
