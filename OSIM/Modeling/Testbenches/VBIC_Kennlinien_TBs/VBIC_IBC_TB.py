import matplotlib.pyplot as plt
from OSIM.Modeling.Components.NPN_Vertical_Bipolar_Intercompany_Model.VBIC_Currents.IBC import *
from OSIM.Modeling.Components.Resistor import Resistor
from OSIM.Modeling.Components.VoltageSource import VoltageSource

from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations
from OSIM.Simulation.CircuitAnalysis.CircuitAnalysis import CircuitAnalysis

bi = 'b'
ci = 'c'

params = dict()
params["Nx"] = "1"
params["ibci"] ="1.5E-18*(1*0.25)" #"1.5E-18*(Nx*0.25)"
params["ibcn"] = "1E-15*(1*0.25)"#"1E-15*(Nx*0.25)"
params["ncn"] = "1.7"
params["nci"] = "1.05"
params["avc1"] = "2.4"
params["avc2"] = "11.5*(1*0.25)**0.01"#"11.5*(Nx*0.25)**0.01"
params["mc"] = "0.12"
params["pc"] = "0.62"

v1 = VoltageSource([bi,'0'],"V1",0,None)
ibc = IBC([bi,ci], "IBC", 0, None ,paramdict=params)
r = Resistor([ci,'0'],"R1",1e-10,None)
TBSys = CircuitSystemEquations([ibc,v1,r])
ca = CircuitAnalysis(TBSys)

x = np.arange(-0, 0.9, 0.001)
current = np.zeros((len(x), 1), dtype=np.float64)
gd = np.zeros((len(x), 1), dtype=np.float64)

TBSys.atype = CircuitSystemEquations.ATYPE_DC

for idx, v in enumerate(x):
    v1.changeMyVoltageInSys(v)
    ca.newtonRaphson(TBSys)
    current[idx] = ibc.current
    gd[idx] = ibc.gd

toFile = open("IBC_kennlinie_nonlin.csv", 'w')

for i in range (gd.shape[0]):
	t = str(x[i])
	plot = str(gd[i][0])
	wline = "".join((t,",",plot,"\n"))
	toFile.write(wline)

toFile.close()

plt.plot(x, gd , label="charge")
#plt.plot(x, current, label="capacity")
plt.show()
