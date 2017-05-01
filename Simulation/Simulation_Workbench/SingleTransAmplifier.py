import numpy as np

from Modeling.CircuitSystemEquations import CircuitSystemEquations
from Simulation.CircuitAnalysis.CircuitAnalyser import CircuitAnalyser
from Simulation.NetToComp import NetToComp


def sweepR3(sys):
    r = np.zeros((3,20),dtype=np.float)
    r3 = sys.getCompByName("R3")

    for i in range(r.shape[1]):
        resistance = 500+i*30
        r[0][i] = resistance
        sys.reset()
        r3.setValue(resistance)
        ca.calcDCOperatingPoint()
        y = ca.getImpedanceAt("V2",1e9)
        r[1][i] = y[0].real
        r[2][i] = y[0].imag

    ca.plot_lin([r,["real","imag"],"current through R3"])

seq = CircuitSystemEquations(NetToComp('SingleTransAmplifier/AmplifierTB.net').getComponents())
ca = CircuitAnalyser(seq)
ca.printDCOp(["Q1IT","Q1bi","Q1ei","Q1ci","R3"])
ca.plot_semilogx(ca.getACAnalysis_semilogx("V2",["OUT"],5,12,10)[0])
#print(ca.getImpedanceAt("V2",18e9))
#sweepR3(seq)
#res = ca.getSPAnalysis_linx(170e9,190e9,5e9)
#res = ca.getSPAnalysis_semilogx(9,12,10,["V2"])
#ca.plot_smith(res)


ca.plot_lin(ca.getTrans(0,2e-10,1e-13,["OUT","N1"]))
#ca.plot_lin(ca.getTrans(0,4e-6,1e-9,["IN","OUT"]))
