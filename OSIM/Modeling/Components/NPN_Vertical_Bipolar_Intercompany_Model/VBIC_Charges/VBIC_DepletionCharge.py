from OSIM.Modeling.Components.Charge import Charge
import numpy as np

class VBIC_DepletionCharge(Charge):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(VBIC_DepletionCharge, self).__init__(nodes, name, value, superComponent,**kwargs)

        self.charge = self.paramDict.get("CJx", "1")
        self.CJx = self.paramDict.get("CJx", "1") #0-V Sperrschichtkapazitaet
        self.P = self.paramDict.get("P", 1)
        self.M = self.paramDict.get("M", 1)
        self.F = self.paramDict.get("F", 1)
        self.P = self.paramDict.get("P", 1)
        self.AJ = self.paramDict.get("AJ", 1)
        self.FAK = self.paramDict.get("FAK", 1)

    def getCharge(self):
        ufrom = self.sys.getSolutionAt(self.nodes[0]).real
        uto = self.sys.getSolutionAt(self.nodes[1]).real
        V = ufrom-uto
        return self.FAK*self.CJx*self.qj(V)

    def getqj(self):
        ufrom = self.sys.getSolutionAt(self.nodes[0]).real
        uto = self.sys.getSolutionAt(self.nodes[1]).real
        V = ufrom-uto
        return self.qj(V)

    def dQdU_A(self):
        ufrom = self.sys.getSolutionAt(self.nodes[0]).real
        uto = self.sys.getSolutionAt(self.nodes[1]).real
        V = ufrom-uto
        h = 0.000001
        return self.CJx*(self.qj(V+h)-self.qj(V))/h

    def qj(self, V):
        P = self.P
        M = self.M
        FC = self.F
        A = self.AJ
        qj = 0
        if A <= 0.0:
            '''
            //Aus http://www.designers-guide.org/VBIC/release1.1.5/vbic1.1.5_pseudoCode.html
            //SPICE regional depletion capacitance model
            //
            '''

            if(V > 1):
                V = V/V

            dvh = V - FC * P
            if dvh > 0.0:
                qlo = P * (1.0 - (1.0 - FC) ** (1.0 - M)) / (1.0 - M)
                qhi = dvh * (1.0 - FC + 0.5 * M * dvh / P) / ((1.0 - FC) ** (1.0 + M))
            else:
                qlo = P * (1.0 - (1.0 - V / P) ** (1.0 - M)) / (1.0 - M)
                qhi = 0.0
            qj = qlo + qhi
        else:
            '''     Aus http://www.designers-guide.org/VBIC/release1.1.5/vbic1.1.5_pseudoCode.html
            //		Single piece depletion capacitance model
            //
            //		Based on c=1/(1-V/P)^M, with sqrt limiting to make it
            //		C-inf continuous (and computationally efficient), with
            //		added terms to make it monotonically increasing (which
            //		is physically incorrect, but avoids numerical problems
            //		and kinks near where the depletion and diffusion
            //		capacitances are of similar magnitude), and with appropriate
            //		offsets added to that qj(V=0)=0.
            '''
            dv0 = - P * FC
            mv0 = np.sqrt(dv0 * dv0 + A)
            vl0 = 0.5 * (dv0 - mv0) + P * FC
            q0 = - P * (1.0 - vl0 / P) ** (1.0 - M) / (1.0 - M)
            dv = V - P * FC
            mv = np.sqrt(dv * dv + A)
            vl = 0.5 * (dv - mv) + P * FC
            qlo = - P * (1.0 - vl / P) ** (1.0 - M) / (1.0 - M)
            qj = qlo + (1.0 - FC) ** (- M) * (V - vl + vl0) - q0

        return qj

    @staticmethod
    def sqj(V, P, M, FC, A):
        #TODO merge with qj
        qj = 0
        if A <= 0.0:
            '''
            //
            //SPICE regional depletion capacitance model
            //
            '''
            dvh = V - FC * P
            if dvh > 0.0:
                qlo = P * (1.0 - (1.0 - FC) ** (1.0 - M)) / (1.0 - M)
                qhi = dvh * (1.0 - FC + 0.5 * M * dvh / P) / ((1.0 - FC) ** (1.0 + M))
            else:
                qlo = P * (1.0 - (1.0 - V / P) ** (1.0 - M)) / (1.0 - M)
                qhi = 0.0
            qj = qlo + qhi

        else:
            '''
            //
            //		Single piece depletion capacitance model
            //
            //		Based on c=1/(1-V/P)^M, with sqrt limiting to make it
            //		C-inf continuous (and computationally efficient), with
            //		added terms to make it monotonically increasing (which
            //		is physically incorrect, but avoids numerical problems
            //		and kinks near where the depletion and diffusion
            //		capacitances are of similar magnitude), and with appropriate
            //		offsets added to that qj(V=0)=0.
            //
            '''
            dv0 = - P * FC
            mv0 = np.sqrt(dv0 * dv0 + A)
            vl0 = 0.5 * (dv0 - mv0) + P * FC
            q0 = - P * (1.0 - vl0 / P) ** (1.0 - M) / (1.0 - M)
            dv = V - P * FC
            mv = np.sqrt(dv * dv + A)
            vl = 0.5 * (dv - mv) + P * FC
            qlo = - P * (1.0 - vl / P) ** (1.0 - M) / (1.0 - M)
            qj = qlo + (1.0 - FC) ** (- M) * (V - vl + vl0) - q0
        return qj


    def reloadParams(self):

        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec(variableExpr)

        self.CJx = self.paramDict.get("CJx", "1")  # 0-V Sperrschichtkapazitaet
        self.P = self.paramDict.get("P", 1)
        self.M = self.paramDict.get("M", 1)
        self.F = self.paramDict.get("F", 1)
        self.P = self.paramDict.get("P", 1)
        self.AJ = self.paramDict.get("AJ", 1)
        self.FAK = self.paramDict.get("FAK", 1)