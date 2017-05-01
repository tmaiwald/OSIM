import matplotlib.pyplot as plt
import numpy as np
from Modeling.Components.NPN_Vertical_Bipolar_Intercompany_Model.VBIC_Charges.VBIC_DepletionCharge import VBIC_DepletionCharge

from Modeling.CircuitSystemEquations import CircuitSystemEquations

#QJBE
Nx = 1
vbic_cje_mm = 3
vbic_cje = 1
CJx = 9.7E-15*(Nx*0.25)**0.95*vbic_cje*(1+(vbic_cje_mm-1)/np.sqrt(Nx)) # CJE
P = 0.9 # PE
M = 0.105 # ME
AJ = -0.5 # AJE
WBx = 1 # WBE
F = 0.97 # FC


'''
#QJBC
Nx = 1
vbic_cjc_mm = 3
vbic_cjc = 1
CJx = 8E-16*(Nx*0.25)**0.99*vbic_cjc*(1+(vbic_cjc_mm-1)/np.sqrt(Nx)) # CJC
P = 0.62 # PC
M = 0.12 # MC
AJ = -0.5 # AJC
WBx = 1 # WBC (Default = 1)
F = 0.97 # FC
'''

bx = "bx"
ei = "ei"

QJBE = VBIC_DepletionCharge([bx, ei],"QJ", CJx, None, dict= {'P':P,'M':M,'F':F,'AJ':AJ,'FAK':WBx})
TBSys = CircuitSystemEquations([QJBE])
x = np.arange(-1, 2, 0.001)
charge = np.zeros((len(x), 1), dtype=np.complex128)
capacity = np.zeros((len(x), 1), dtype=np.complex128)

for idx, v in enumerate(x):
    TBSys.x[TBSys.compDict.get(bx)] = v
    charge[idx] = QJBE.getCharge()
    capacity[idx] = QJBE.dQdU_A()

plt.plot(x, charge , label="charge")
plt.plot(x, capacity, label="capacity")
plt.legend(loc="lower right",fontsize=12)
plt.show()
