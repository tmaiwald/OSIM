from OSIM.Modeling.Components.Capacity import Capacity
import numpy as np
import OSIM.Simulation.Utils as u
from OSIM.Modeling.Components.Charge import Charge

class QBC(Charge):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(QBC, self).__init__(nodes, name, value, superComponent, **kwargs)

        self.charge = value
        self.prevCharge = 0
        self.bi = nodes[0]
        self.ci_x = nodes[1]

        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec (variableExpr)

        self.UT = eval(self.paramDict.get("ut", "0.026"))
        self.GAMM = eval(self.paramDict.get("gamm", "3E-14"))
        self.QCO = eval(self.paramDict.get("qco", "1E-18"))

    def getCharge(self):
        ubi = self.sys.getSolutionAt(self.bi).real
        uci_x = self.sys.getSolutionAt(self.ci_x).real
        K = np.sqrt(1+self.GAMM*u.exp(ubi-uci_x, 1/self.UT, 2))
        return self.QCO#*K

    def dQdU_A(self):
        #   a
        #  ---
        #   b
        #ubi = (self.sys.getSolutionAt(self.bi).real)
        #uci_x = (self.sys.getSolutionAt(self.ci_x).real)
        #a = self.GAMM *u.exp(ubi-uci_x, 1/self.UT, 2)
        #b = 2*self.UT*np.sqrt(self.GAMM*u.exp(ubi-uci_x, 1/self.UT, 2)+1)
        return self.QCO#(a/b)
