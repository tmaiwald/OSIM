import matplotlib.pyplot as plt
import numpy as np
from Modeling.Components.NPN_Vertical_Bipolar_Intercompany_Model.VBIC_Charges.VBIC_DiffusionCharges import *
from Modeling.Components.VoltageSource import VoltageSource
from Modeling.Components.Resistor import Resistor
from Simulation.CircuitAnalysis.CircuitAnalyser import CircuitAnalyser
from Modeling.CircuitSystemEquations import CircuitSystemEquations

class IT(object):

    def __init__(self):
        self.itf = 0.5e-3
        self.qb = 1
        self.q1 = 1

    def getqb(self):
        return self.qb

    def getq1(self):
        return self.q1

class dummyMainTransportCurrent(object):

    def __init__(self):
        self.internalComponents = []
        self.IT = IT()


bi = "bi"
ei = "ei"

vbic_tf = 1
vbic_tf_mm = 1
params = dict()
params["Nx"] = "1"
params["ut"] = "0.026"
params["temp"] = "27"
params["tf"] = "2.67E-13*vbic_tf*(1+(vbic_tf_mm-1)/np.sqrt(Nx))*((temp+273)/300)**0.7"
params["qtf"] = "1E-18"
params["xtf"] = "20"
params["vtf"] = "10"
params["itf"] = "0.4*(Nx*0.25)"


dummyIT = dummyMainTransportCurrent()
Q_DBE = QDBE([bi, ei],"QDBE",0,dummyIT,dict=params)
vsource = VoltageSource(["0",bi],"V1",0,None,dict={'FUNC':'SIN','F':'1e11', 'DC':'0', 'AC':'1', 'P':'180'})
r1 = Resistor([ei,"0"],"R1",0.00001,None)
TBSys = CircuitSystemEquations([Q_DBE,vsource,r1])
ca = CircuitAnalyser(TBSys)

x = np.arange(-1, 2, 0.1)
charge = np.zeros((len(x), 1), dtype=np.complex128)
capacity = np.zeros((len(x), 1), dtype=np.complex128)

for idx, v in enumerate(x):
    #vsource.changeMyVoltageInSys(v)
    dummyIT.IT.itf += 0.1e-3
    ca.calcDCOperatingPoint()
    charge[idx] = Q_DBE.TFF(v)#Q_DBE.getCharge()
    #capacity[idx] = Q_DBE.dQdU_A()

plt.plot(x, charge , label="charge")
#plt.plot(x, capacity, label="capacity")
plt.show()
