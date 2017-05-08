import matplotlib.pyplot as plt
from OSIM.Modeling.Components.NPN_Vertical_Bipolar_Intercompany_Model.VBIC_Currents.IRCI import *
from OSIM.Modeling.Components.Resistor import Resistor
from OSIM.Modeling.Components.VoltageSource import VoltageSource
from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations
from OSIM.Modeling.Components.NPN_Vertical_Bipolar_Intercompany_Model.NPN_VBIC import NPN_VBIC
from OSIM.Simulation.CircuitAnalysis.CircuitAnalysis import CircuitAnalysis
from OSIM.Simulation.NRConvergenceException  import NRConvergenceException
import numpy as np
fig = plt.figure()
ax = fig.gca(projection='3d')

nb = 'b'
nc = 'c'
ne = 'e'
m1 = 'm1'
m2 = 'm2'

#Anzeigeparamter
raster = 0.05
BFIX = 0.9
CMIN = -0.5
CMAX = 0.5
EMIN = -0.5
EMAX = 0.5

r1 = Resistor([m1,nb],"R1",0.001,None)
r2 = Resistor([m2,nc],"R2",0.001,None)
v1 = VoltageSource([m1,'0'],"V1",0,None)
v2 = VoltageSource([m2,'0'],"V2",0,None)
v3 = VoltageSource([ne,'0'],"V3",0,None)

npn = NPN_VBIC([nc, nb, ne, '0'], "Q", 0, None, pParams="../../__Parameter/NPN_VBIC_npn13G2.comp")
TBSys = CircuitSystemEquations([npn,r1,r2,v3,v1,v2])
print(TBSys.compDict)
ca = CircuitAnalysis(TBSys)
TBSys.atype = CircuitSystemEquations.ATYPE_DC

xE = np.arange(EMIN, EMAX, raster)
yC = np.arange(CMIN, CMAX, raster)
B, C = np.meshgrid(xE, yC)
I = np.zeros((len(yC),len(xE)))

v1.changeMyVoltageInSys(BFIX)

for cidx, c in enumerate(yC):
    for eidx,e in enumerate(xE):
        v3.changeMyVoltageInSys(e)
        v2.changeMyVoltageInSys(c)
        try:
            ca.newtonRaphson(TBSys)
            sol = npn.getTransportCurrent()
        except NRConvergenceException:
            print("Convergence problem at: ")
            print("E: %G"%(e))
            print("C: %G"%(c))
            npn.IT.debugPrint()
            #x = raw_input()
            sol = 0
        #print(TBSys.curNewtonIteration)
        #a = raw_input()
        I[cidx][eidx] = sol

# ax.plot_surface(B, C, I, rstride=8, cstride=8, alpha=0.3)
ax.plot_wireframe(B, C, I, rstride=5, cstride=5, alpha=0.3)

#cset = ax.contour(B, C, I, zdir='x', offset=BMAX, cmap=cm.coolwarm)

ax.set_xlabel('E')
ax.set_xlim(EMIN, EMAX)
ax.set_ylabel('C')
ax.set_ylim(CMIN, CMAX)
ax.set_zlabel('I')
ax.set_zlim(np.amin(I), np.amax(I))

plt.show()
