import OSIM.Simulation.Utils as u
from OSIM.Modeling.Components.Charge import Charge
from OSIM.Modeling.Components.NPN_Vertical_Bipolar_Intercompany_Model.VBIC_ParasitPNP.VBIC_ParasitTransportCurrent import ParasitTransportCurrent
import numpy as np
from numba import jit

class QDBE(Charge):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(QDBE, self).__init__(nodes, name, value, superComponent,**kwargs)

        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec (variableExpr)

        self.UT = eval(self.paramDict.get("ut", "0.026"))
        self.TF = eval(self.paramDict.get("tf", "2.67E-13"))
        self.QTF = eval(self.paramDict.get("qtf", "1E-18"))
        self.XTF = eval(self.paramDict.get("xtf", "20"))
        self.VTF = eval(self.paramDict.get("vtf", "10"))
        self.ITF = eval(self.paramDict.get("itf", "0.1"))
        self.diffh = 0.000000001

    def TFF(self,V):
        itf = self.superComponent.IT.itf
        q1 = self.superComponent.IT.getq1()
        b = 1+self.XTF*(itf/(itf+self.ITF))**2*u.exp(V,1/(1.44*self.VTF), 1.5)
        return self.TF*(1+self.QTF*q1)*b

    def getCharge(self):
        ufrom = self.sys.getSolutionAt(self.nodes[0]).real
        uto = self.sys.getSolutionAt(self.nodes[1]).real
        V = (ufrom-uto)
        qb = self.superComponent.IT.getqb()
        return self.TFF(V)*self.superComponent.IT.itf/qb

    @jit
    def dQdU_A(self):
        ufrom = self.sys.getSolutionAt(self.nodes[0]).real
        uto = self.sys.getSolutionAt(self.nodes[1]).real
        V = (ufrom-uto)
        return np.abs((self.TFF(V+self.diffh)*self.superComponent.IT.itf/self.superComponent.IT.getqb()-self.getCharge())/self.diffh)

    def reloadParams(self):

        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec(variableExpr)

        self.UT = eval(self.paramDict.get("ut", "0.026"))
        self.TF = eval(self.paramDict.get("tf", "2.67E-13"))
        self.QTF = eval(self.paramDict.get("qtf", "1E-18"))
        self.XTF = eval(self.paramDict.get("xtf", "20"))
        self.VTF = eval(self.paramDict.get("vtf", "10"))
        self.ITF = eval(self.paramDict.get("itf", "0.1"))


class QDBC(Charge):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(QDBC, self).__init__(nodes, name, value, superComponent,**kwargs)

        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec(variableExpr)

        self.TR = eval(self.paramDict.get("tr", "5E-12"))

    def getCharge(self):
        return self.TR*self.superComponent.IT.itr

    @jit
    def dQdU_A(self):
        return np.abs(self.TR*self.superComponent.ditr_A())

    def reloadParams(self):

        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec(variableExpr)

        self.TR = eval(self.paramDict.get("tr", "5E-12"))


class QDBEP(Charge):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        self.PCS = ParasitTransportCurrent(['0','0','0'], "0", "0", None,**kwargs)
        super(QDBEP, self).__init__(nodes, name, value, superComponent,**kwargs)

        if self.PCS.name == "0":
            print (name+" ERROR: ParasitCurrentSource has to be set!")

        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec(variableExpr)

        self.TR = eval(self.paramDict.get("tr", "5E-12"))

    def getCharge(self):
        return [self.TR*self.PCS.itfp]

    def dQdU_A(self):
        return self.TR*self.PCS.ditrp_A()

    def parseArgs(self, **kwargs):
        super(QDBEP,self).parseArgs(**kwargs)
        for name, value in kwargs.items():
            if name == 'ParasitCurSource':
                self.PCS = value

    def reloadParams(self):

        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec(variableExpr)

        self.TR = eval(self.paramDict.get("tr", "5E-12"))