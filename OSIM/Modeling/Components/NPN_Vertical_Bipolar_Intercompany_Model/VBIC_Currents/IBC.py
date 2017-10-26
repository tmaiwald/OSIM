import numpy as np
from numba import jit
import OSIM.Simulation.Utils as u
from OSIM.Modeling.AbstractComponents.NonlinearComponent import NonlinearComponent


class IBC(NonlinearComponent):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(IBC, self).__init__(nodes, name, value, superComponent, **kwargs)

        if(self.COMPONENT_PRINT_WARNINGS):
            print (name + "VBIC Current IBC-Warning no avalanche effect implemented yet")

        self.bi = nodes[0]
        self.ci = nodes[1]
        #self.ei = nodes[2]

        '''
        TODO: Defaultwerte anpassen
        '''
        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec(variableExpr)

        self.UT = eval(self.paramDict.get("ut", "0.026"))
        self.IBCI = eval(self.paramDict.get("ibci", "1.5E-18"))
        self.IBCN = eval(self.paramDict.get("ibcn", "1E-15"))
        self.NCN = eval(self.paramDict.get("ncn", "1.7"))
        self.NCI = eval(self.paramDict.get("nci", "1.05"))
        self.AVC1 = eval(self.paramDict.get("avc1", "2.4"))
        self.AVC2 = eval(self.paramDict.get("avc2", "11.5"))
        self.MC = eval(self.paramDict.get("mc", "0.12"))
        self.PC = eval(self.paramDict.get("pc", "0.62"))
        self.IS = eval(self.paramDict.get("is", "1e-16"))
        self.ISSR = eval(self.paramDict.get("issr", "1"))
        self.NF = eval(self.paramDict.get("nf", "1.0"))
        self.NR = eval(self.paramDict.get("nr", "1.0"))
        self.Udlim = 0.8

    def performCalculations(self):
        self.current,self.gd  = self.getCharacterisitcs()

    def getCharacterisitcs(self):

        ubi = (self.sys.getSolutionAt(self.bi).real)
        uci = (self.sys.getSolutionAt(self.ci).real)
        #uei = (self.sys.getSolutionAt(self.ei).real)

        ibcn = self.IBCN * (u.exp((ubi - uci), 1 / (self.NCN * self.UT), self.Udlim) - 1.0)
        ibci = self.IBCI * (u.exp((ubi - uci), 1 / (self.NCI * self.UT), self.Udlim) - 1.0)
        igc = 0 #self.igc(ubi, uci,uei,ibcn + ibci) # fehlt noch
        dig = 0 #(self.igc(ubi+0.000001, uei, uci,ibcn + ibci)-igc)/0.000001
        return ibcn + ibci - igc , ibcn / (self.NCN * self.UT) + ibci / (self.NCI * self.UT)+dig + self.sys.GMIN

    def avalm(self, V, P, M, AV1, AV2):
        # aus http://www.designers-guide.org/VBIC/release1.1.5/vbic1.1.5_pseudoCode.html
        # Kloosterman/de Graaff weak avalanche model

        vl = 0.5 * (np.sqrt((P - V) ** 2 + 0.01) + (P - V))
        return AV1 * vl * np.exp(- AV2 * vl ** (M - 1.0))

    def igc(self, ubi, uci,uei,ibc):
        #TODO: implement !
        Itzf = self._ITF(ubi,uei)
        Itzr = self._ITR(ubi,uci)

        return (Itzf - Itzr - ibc )*self.avalm(ubi-uci,self.PC,self.MC,self.AVC1,self.AVC2)

    def reloadParams(self):

        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec (variableExpr)


        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec(variableExpr)

        self.UT = eval(self.paramDict.get("ut", "0.026"))
        self.IBCI = eval(self.paramDict.get("ibci", "1.5E-18"))
        self.IBCN = eval(self.paramDict.get("ibcn", "1E-15"))
        self.NCN = eval(self.paramDict.get("ncn", "1.7"))
        self.NCI = eval(self.paramDict.get("nci", "1.05"))
        self.AVC1 = eval(self.paramDict.get("avc1", "2.4"))
        self.AVC2 = eval(self.paramDict.get("avc2", "11.5"))
        self.MC = eval(self.paramDict.get("mc", "0.12"))
        self.PC = eval(self.paramDict.get("pc", "0.62"))
        self.IS = eval(self.paramDict.get("is", "1e-16"))
        self.ISSR = eval(self.paramDict.get("issr", "1"))
        self.NF = eval(self.paramDict.get("nf", "1.0"))
        self.NR = eval(self.paramDict.get("nr", "1.0"))

    @jit
    def _ITF(self, BI, EI):

        if (BI < 1.6):
            lim = BI
        else:
            lim = 1.6

        return self.IS * (u.exp(BI - EI, 1 / (self.NF * self.UT), lim) - 1.0)

    @jit
    def _ITR(self, BI, CI):

        if (BI < 1.6):
            lim = BI
        else:
            lim = 1.6
        return self.IS * self.ISSR * (u.exp(BI - CI, 1 / (self.NR * self.UT), lim) - 1.0)