import numpy as np
from Modeling.Components.NPN_Vertical_Bipolar_Intercompany_Model.VBIC_Charges.VBIC_DepletionCharge import VBIC_DepletionCharge
from Modeling.Components.Resistor import Resistor
from Modeling.Components.VoltageSource import VoltageSource
from Modeling.Components.Capacity import Capacity

from Modeling.CircuitSystemEquations import CircuitSystemEquations
from Simulation.CircuitAnalysis.CircuitAnalyser import CircuitAnalyser

#QJBE
Nx = 1
vbic_cje_mm = 1
vbic_cje = 1
CJx = 9.7E-15*(Nx*0.25)**0.95*vbic_cje*(1+(vbic_cje_mm-1)/np.sqrt(Nx)) # CJE
P = 0.9 # PE
M = 0.105 # ME
AJ = -0.5 # AJE
WBx = 1 # WBE
F = 0.97 # FC

gnd = '0'
sigin = '1'
sigout = '2'
ik = '3'

vsource = VoltageSource([gnd,sigin],"V1",0,None,dict={'FUNC':'SIN','F':'1e11', 'DC':'0', 'AC':'1', 'P':'180'})
r1 = Resistor([sigin,sigout],"R1",0.00001,None)
c = VBIC_DepletionCharge([sigout, ik],"QJ", CJx, None, dict= {'P':P,'M':M,'F':F,'AJ':AJ,'FAK':WBx})
cref = Capacity([sigout, ik],"CR",0.35e-14, None)
r2 = Resistor([ik,gnd],"R2",1000,None)

TBSys = CircuitSystemEquations([vsource,r1,c,r2,cref])
ca = CircuitAnalyser(TBSys)

volts = [x/100 for x in range(-200,200)]
res = np.zeros((2,len(volts)),dtype= np.float64)

#for vidx,v in enumerate(volts):
#    vsource.changeMyVoltageInSys(v)
#    ca.calcDCOperatingPoint()
#    res[0][vidx] = v
#    res[1][vidx] = c.getCharge()

#ca.plot_lin([res,["Q"],"Ladung"])
ca.plot_lin(ca.getTrans(0 ,4e-11,1e-14,['CR','QJ']))


