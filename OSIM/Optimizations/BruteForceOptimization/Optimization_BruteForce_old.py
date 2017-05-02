
#!/usr/bin/python
import matplotlib.pyplot as plt
import numpy as np

from Modeling.CircuitSystemEquations import CircuitSystemEquations
from Simulation.NetToComp import NetToComp

fig = plt.figure()
ax = fig.gca(projection='3d')

from OSIM.Simulation.CircuitAnalysis.ACAnalysis import ACAnalysis
from OSIM.Simulation.CircuitAnalysis.SParameterAnalysis import SParameterAnalysis


#circuit = '__Circuits/TransistorTB.net'
#circuit = '__Circuits/AmplifierTB2.net'
#circuit = '__Circuits/AmplifierTB.net'
#circuit = '__Circuits/lowpassTB.net'
#circuit = '__Circuits/CapacityTB.net'
#circuit = '__Circuits/SParameterTB.net'
#circuit = '__Circuits/TransAnalysisTB.net'
#circuit = '__Circuits/TransTransistorAnalysisTB.net'
circuit = '__Diverse Schaltungen/OptimizerAmplifierTB.net'

seq = CircuitSystemEquations(NetToComp(circuit).getComponents())
sp =  SParameterAnalysis(seq)
ac = ACAnalysis(seq)

print (seq.compDict)

def cost(R1,R1val,R2,R2val):
    R1.setValue(R1val)
    R2.setValue(R2val)
    ref = sp.reflection("P1",180e9)
    mag = ac.mag("P1V","OUT",180e9)
    #print  (5*(1-np.absolute(ref)) + 10 * mag)
    return 5*(1-np.absolute(ref)) + 10 * mag


###1) get changeable Components
R1 = seq.getCompByName("R1")
R2 = seq.getCompByName("R2")

RFROM = 1
RTO = 20001
RSTEP = 1000

R1vals = np.arange(RFROM, RTO, RSTEP)
R2vals = np.arange(RFROM, RTO, RSTEP)

R1valsg, R2valsg = np.meshgrid(R1vals, R2vals)
f_x = np.zeros((len(R1vals),len(R2vals)))
for r1idx, r1 in enumerate(R1vals):
    for r2idx, r2 in enumerate(R2vals):
        f_x[r1idx][r2idx] = cost(R1,r1,R2,r2)


ax.plot_wireframe(R1valsg, R2valsg, f_x, rstride=3, cstride=3, alpha=0.3)

#cset = ax.contour(B, C, I, zdir='x', offset=BMAX, cmap=cm.coolwarm)
#cset = ax.contour(bB, bC, bI, zdir='y', offset=0.3, cmap=cm.coolwarm)
#cset = ax.contour(B, C, I, zdir='y', offset=1, cmap=cm.coolwarm)

ax.set_xlabel('R1')
ax.set_xlim(RFROM, RTO)
ax.set_ylabel('R2')
ax.set_ylim(RFROM, RTO)
ax.set_zlabel('Cost')
ax.set_zlim(np.amin(f_x), np.amax(f_x))

plt.show()

#CharactersiticCurves(seq).createCharacteristicCurves('P1V',0.1,0.6 ,0.0025, 'V2',0, 2.51, 0.5, ["Q1IT"])
#ACAnalysis(seq).analyse(1,11,10,"OUT", 'P1V')
#SParameterAnalysis(seq).analyse(1,10,10)
#DCAnalysis(seq).analyse('V1',-1, 2, 0.01, ["D1","V1"])
#TransAnalysis(seq).analyse(0, 3e-3, 3e-6, ["OUT","IN","Q1IT"], "P1V")
