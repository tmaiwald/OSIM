from numba import jit
import OSIM.Simulation.Utils as u
import numpy as np
from OSIM.Modeling.AbstractComponents.NonlinearComponent import NonlinearComponent


class IBE(NonlinearComponent):  # behaves like a Diode

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        self.isExternal = False
        super(IBE, self).__init__(nodes, name, value, superComponent, **kwargs)

        self.bi = nodes[0]
        self.ei = nodes[1]

        '''
        TODO: Defaultwerte anpassen
        '''
        self.WBE = eval(self.paramDict.get("wbe", "1"))
        if (self.isExternal == True):
            self.WBE = 1 - self.WBE

        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec(variableExpr)

        self.UT = eval(self.paramDict.get("ut", "0.026"))
        self.IBEI = eval(self.paramDict.get("ibei", "1"))
        self.IBEN = eval(self.paramDict.get("iben", "1"))
        self.NEN = eval(self.paramDict.get("nen", "1"))
        self.NEI = eval(self.paramDict.get("nei", "1"))
        self.Udlim = 0.9

    @jit
    def performCalculations(self):
        self.current,self.gd = self.getCharacterisitcs()

    def getCharacterisitcs(self):

        ubi = self.sys.getSolutionAt(self.bi).real
        uei = self.sys.getSolutionAt(self.ei).real
        ubei = ubi - uei

        ideal = self.WBE * self.IBEI * (u.exp(ubei, 1 / (self.NEI * self.UT), self.Udlim) - 1.0)
        nonideal = self.WBE * self.IBEN * (u.exp(ubei, 1 / (self.NEN * self.UT), self.Udlim) - 1.0)
        gd = ideal / (self.NEI * self.UT) + nonideal / (self.NEN * self.UT)
        return  [ideal+nonideal,gd]

    def parseArgs(self, **kwargs):
        super(IBE, self).parseArgs(**kwargs)
        for name, value in kwargs.items():
            if name == 'isExternal':
                self.external = value


    def getESTDCAdmittance(self):

        ubi = self.sys.getSolutionAt(self.bi).real
        uei = self.sys.getSolutionAt(self.ei).real
        ubei = ubi - uei
        if(ubei < 0):
            return 0

        ideal = self.WBE * self.IBEI * (u.exp(0.8, 1 / (self.NEI * self.UT), self.Udlim) - 1.0)
        nonideal = self.WBE * self.IBEN * (u.exp(0.8, 1 / (self.NEN * self.UT), self.Udlim) - 1.0)
        gd = ideal / (self.NEI * self.UT) + nonideal / (self.NEN * self.UT)

        return (self.alpha)*gd


    def reloadParams(self):

        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec(variableExpr)

        self.UT = eval(self.paramDict.get("ut", "0.026"))
        self.IBEI = eval(self.paramDict.get("ibei", "1"))
        self.IBEN = eval(self.paramDict.get("iben", "1"))
        self.NEN = eval(self.paramDict.get("nen", "1"))
        self.NEI = eval(self.paramDict.get("nei", "1"))