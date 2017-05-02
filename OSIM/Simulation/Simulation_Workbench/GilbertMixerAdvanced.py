from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations
from OSIM.Simulation.CircuitAnalysis.CircuitAnalyser import CircuitAnalyser
import numpy as np
from OSIM.Simulation.NetToComp import NetToComp

seq = CircuitSystemEquations(NetToComp('GilbertMixer/GilberMixerAdvanced.net').getComponents())
ca = CircuitAnalyser(seq)
ca.printDCOp(["vCurMirror","Q7IT","Q6C","LOPlus"])
imp1_180 = ca.getImpedanceAt("V1",180e9)
imp4_18 = ca.getImpedanceAt("V4",18e9)
imp5_18 = ca.getImpedanceAt("V5",18e9)

print("IMP1_180 @180G: %s"%str(imp1_180))
print("IMP4_18 @18G: %s"%str((imp4_18)))
print("IMP5_18 @18G: %s"%str(imp5_18))

#print(imp6)
#v1 = seq.getCompByName("V1").setInnerImpedance(imp[0])
#seq.getCompByName("V3").setInnerImpedance(imp[0])
#print(v1.getInnerImpedance())
#ca.plot_smith(ca.getSPAnalysis_semilogx(8,12,10,["V1","V3"]))
ca.plot_semilogx(ca.getACAnalysis_semilogx("V1",["Q1C"],9,11,10)[0])

res = ca.getTrans(0,0.1e-9,1e-13,["Q4C","Q1C","LOPlus"])

# how to get a diff-Signal
out = np.zeros((2,res[0].shape[1]),dtype = np.float64)
for i in range(res[0].shape[1]):
    out[0][i] = (res[0])[0][i]
    out[1][i] = (res[0])[1][i] - (res[0])[2][i]

ca.plot_lin([out,["diffout"],"transient"])

print("Max %G "%np.amax(out[1][:]))

ca.plot_lin(res)
