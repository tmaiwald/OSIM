import numpy as np

import OSIM.Simulation.Utils as u
from OSIM.Modeling.AbstractComponents.NonlinearComponent import NonlinearComponent


class IBC(NonlinearComponent):  # behaves like a Diode

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(IBC, self).__init__(nodes, name, value, superComponent, **kwargs)

        if(self.COMPONENT_PRINT_WARNINGS):
            print (name + "VBIC Current IBC-Warning no avalanche effect implemented yet")

        self.bi = nodes[0]
        self.ci = nodes[1]

        '''
        TODO: Defaultwerte anpassen
        '''
        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec(variableExpr)

        self.UT = eval(self.paramDict.get("ut", "0.026"))
        self.IBCI = eval(self.paramDict.get("ibci", "1"))
        self.IBCN = eval(self.paramDict.get("ibcn", "1"))
        self.NCN = eval(self.paramDict.get("ncn", "1"))
        self.NCI = eval(self.paramDict.get("nci", "1"))
        self.AVC1 = eval(self.paramDict.get("avc1", "1"))
        self.AVC2 = eval(self.paramDict.get("avc2", "1"))
        self.MC = eval(self.paramDict.get("mc", "1"))
        self.PC = eval(self.paramDict.get("pc", "0.62"))

        self.Udlim = 0.8

    def performCalculations(self):
        self.current,self.gd  = self.getCharacterisitcs()

    def getCharacterisitcs(self):
        #ubi = (self.sys.getSolutionAt(self.bi).real)[0]
        #uci = (self.sys.getSolutionAt(self.ci).real)[0]
        ubi = (self.sys.getSolutionAt(self.bi).real)
        uci = (self.sys.getSolutionAt(self.ci).real)

        ibcn = self.IBCN * (u.exp((ubi - uci), 1 / (self.NCN * self.UT), self.Udlim) - 1.0)
        ibci = self.IBCI * (u.exp((ubi - uci), 1 / (self.NCI * self.UT), self.Udlim) - 1.0)
        #ig = self.igc(ubi, uci) # fehlt noch
        return ibcn + ibci ,ibcn / (self.NCN * self.UT) + ibci / (self.NCI * self.UT)

    def avalm(self, V, P, M, AV1, AV2):
        # aus http://www.designers-guide.org/VBIC/release1.1.5/vbic1.1.5_pseudoCode.html
        # Kloosterman/de Graaff weak avalanche model

        vl = 0.5 * (np.sqrt((P - V) ** 2 + 0.01) + (P - V))
        return AV1 * vl * np.exp(- AV2 * vl ** (M - 1.0))

    def igc(self, ubi, uci):
        #TODO: implement !
        return 0  # (Itzf - Itzr - Ibc ) *self.avalm(ubi-uci,self.PC,self.MC,self.AVC1,self.AVC2)

    def getESTDCAdmittance(self):
        ubi = (self.sys.getSolutionAt(self.bi).real)[0]
        uci = (self.sys.getSolutionAt(self.ci).real)[0]

        if(ubi-uci < 0):
            return 0
        ibcn = self.IBCN * (u.exp((0.8), 1 / (self.NCN * self.UT), self.Udlim) - 1.0)
        ibci = self.IBCI * (u.exp((0.8), 1 / (self.NCI * self.UT), self.Udlim) - 1.0)
        #ig = self.igc(ubi, uci) # fehlt noch
        return (self.alpha)*ibcn / (self.NCN * self.UT) + ibci / (self.NCI * self.UT)

    def reloadParams(self):

        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec (variableExpr)


        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec(variableExpr)

        self.UT = eval(self.paramDict.get("ut", "0.026"))
        self.IBCI = eval(self.paramDict.get("ibci", "1"))
        self.IBCN = eval(self.paramDict.get("ibcn", "1"))
        self.NCN = eval(self.paramDict.get("ncn", "1"))
        self.NCI = eval(self.paramDict.get("nci", "1"))
        self.AVC1 = eval(self.paramDict.get("avc1", "1"))
        self.AVC2 = eval(self.paramDict.get("avc2", "1"))
        self.MC = eval(self.paramDict.get("mc", "1"))
        self.PC = eval(self.paramDict.get("pc", "0.62"))