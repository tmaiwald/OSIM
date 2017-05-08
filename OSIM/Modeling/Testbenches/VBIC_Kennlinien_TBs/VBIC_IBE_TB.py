import matplotlib.pyplot as plt
import matplotlib as mpl
from OSIM.Modeling.Components.NPN_Vertical_Bipolar_Intercompany_Model.VBIC_Currents.IBE import *
from OSIM.Modeling.Components.Resistor import Resistor
from OSIM.Modeling.Components.VoltageSource import VoltageSource
from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations
from OSIM.Simulation.CircuitAnalysis.CircuitAnalysis import CircuitAnalysis


bi = 'b'
ei = 'e'

vbic_ibei_mm = 1
vbic_ibei = 1

params = dict()
params["Nx"] = "1"
params["ibei"] = "5.1E-20*(Nx*0.25)**1.03*vbic_ibei*(1+(vbic_ibei_mm-1)/np.sqrt(Nx))"
params["iben"] = "4E-15*(Nx*0.25)"
params["nen"] = "2.7"
params["nei"] = "1.022"

v1 = VoltageSource([bi,'0'],"V1",0,None)
ibe = IBE([bi,ei], "IBE", 0, None ,dict=params)
r = Resistor([ei,'0'],"R1",1e-10,None)
TBSys = CircuitSystemEquations([ibe,v1,r])
ca = CircuitAnalysis(TBSys)

x = np.arange(0.8, 1.5, 0.001)
current = np.zeros((len(x), 1), dtype=np.complex128)
gd = np.zeros((len(x), 1), dtype=np.complex128)

TBSys.atype = CircuitSystemEquations.ATYPE_DC

for idx, v in enumerate(x):
    v1.changeMyVoltageInSys(v)
    ca.newtonRaphson(TBSys)
    current[idx] = ibe.current
    gd[idx] = ibe.gd

plt.figure(figsize=(5,5))
plt.plot(x, gd , label="charge")
#plt.plot(x, current, label="capacity")
plt.show()
