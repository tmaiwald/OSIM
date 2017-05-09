import numpy as np
from numba import jit

import OSIM.Simulation.Utils as u
from OSIM.Modeling.AbstractComponents.NonlinearComponent import NonlinearComponent
from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations
from OSIM.Modeling.Components.NPN_Vertical_Bipolar_Intercompany_Model.VBIC_Charges.VBIC_DepletionCharge import VBIC_DepletionCharge as dc

'''
UBE | UBC | Betriebszustand Einsatzgebiete
> 0 | < 0 | aktiv normal Verstaerker
< 0 | > 0 | aktiv invers -
< 0 | < 0 | gesperrt Schaltzustand AUS Schalter
> 0 | > 0 | uebersteuert Schaltzustand EIN
'''

class MainTransportCurrent(NonlinearComponent):
    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(MainTransportCurrent, self).__init__(nodes, name, value, superComponent, **kwargs)

        if(self.COMPONENT_PRINT_WARNINGS):
            print (name+"Warning: Reacht-Through-Effekt not implemented!")
            print (name+"Warning: AC-Model not implemented right () Berkner S132!")

        self.diffh = 1e-10

        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec(variableExpr)

        self.NF = eval(self.paramDict.get("nf", "1"))
        self.NR = eval(self.paramDict.get("nr", "1"))
        self.IS = eval(self.paramDict.get("is", "1e-16"))
        self.ISSR = eval(self.paramDict.get("issr", "1"))
        self.UT = eval(self.paramDict.get("Ut", "0.026"))
        self.VEF = eval(self.paramDict.get("vef", "30"))
        self.VER = eval(self.paramDict.get("ver", "60"))
        self.IKF = eval(self.paramDict.get("ikf", "10e10"))
        self.IKR = eval(self.paramDict.get("ikr", "10e10"))
        self.NKF = eval(self.paramDict.get("nkf", "0.5"))
        self.FC = eval(self.paramDict.get("fc", "0.97"))
        self.AJE = eval(self.paramDict.get("aje", "-0.5"))
        self.AJC = eval(self.paramDict.get("ajc", "-0.5"))
        self.AJS = eval(self.paramDict.get("ajs", "-0.5"))
        self.PC = eval(self.paramDict.get("pc", "0.62"))
        self.PS = eval(self.paramDict.get("ps", "0.42"))
        self.PE = eval(self.paramDict.get("pe", "0.9"))
        self.ME = eval(self.paramDict.get("me", "0.105"))
        self.MC = eval(self.paramDict.get("mc", "0.12"))
        self.VRT = eval(self.paramDict.get("vrt", "0 "))  # TODO: Paramter von VBIC 1.2
        self.ART = eval(self.paramDict.get("art", "0.1"))  # TODO:  Paramter von VBIC 1.2

        self.bi = nodes[1]
        self.ei = nodes[2]
        self.ci = nodes[0]
        #self.Udlim = 0.9

        self.itf = [0]
        self.itr = [0]
        self.current = 0
        self.dub = 0
        self.duc = 0
        self.due = 0
        self.sc = self.superComponent
        self.dUBEI = 0
        self.dUBCI = 0
        self.EST_BV = 1000
        self.EST_BR = 1000

    def setOPValues(self):

        self.performCalculations()
        self.dUBEI = self.itf/(self.NF+self.UT)
        self.dUBCI = self.itr/(self.NR+self.UT)
        self.opValues["dUBCI"] = self.dUBCI
        self.opValues["dUBEI"] = self.dUBEI
        self.opValues["current"] = self.current


    def initialSignIntoSysEquations(self):
        branchIdx = self.sys.compDict.get(self.name)
        nodeIdx_ci = self.sys.compDict.get(self.ci)
        nodeIdx_ei = self.sys.compDict.get(self.ei)

        self.sys.A[branchIdx, branchIdx] = -1
        self.sys.A[nodeIdx_ci, branchIdx] = 1
        self.sys.A[nodeIdx_ei, branchIdx] = -1

    @jit
    def doStep(self, freq_or_tau):

        if self.sys.atype == CircuitSystemEquations.ATYPE_AC:
            # acts as voltage dependent current source
            self.sys.g[self.sys.compDict.get(self.name)] = 0
            self.sys.b[self.bIdx] = self.dUBEI*self.Udiff([self.bi,self.ei]) - self.dUBCI * self.Udiff([self.bi, self.ci])
            return

        if self.sys.atype == CircuitSystemEquations.ATYPE_EST_DC:

            c,g = self.superComponent.IBE.getCharacterisitcs()
            d,f = self.superComponent.IBC.getCharacterisitcs()

            self.sys.b[self.bIdx] =(self.EST_BV*c - self.EST_BR*d)
            j = (g* self.EST_BV - f*self.EST_BR)

            self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.bi), j)
            self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.ei), -j)
            self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.ci), -2*j)

        if self.sys.atype in [CircuitSystemEquations.ATYPE_DC,CircuitSystemEquations.ATYPE_TRAN]:
            self.performCalculations()
            self.sys.g[self.sys.compDict.get(self.name)] = self.current
            self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.bi), self.dub)
            self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.ci), self.duc)
            self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.ei), self.due)

    def containsNonlinearity(self):
        return True

    def _q1(self,UBE, UBC):
        qjbc = dc.sqj(UBC, self.PC, self.MC, self.FC , self.AJC)
        qjbe = dc.sqj(UBE, self.PE, self.ME, self.FC, self.AJE)
        return 1 + qjbe / self.VER + qjbc / self.VEF

    def _q2(self,Itf, Itr, IKR, IKF):
        return Itf / IKF + Itr / IKR

    def _qb(self,B,C,E,Itf,Itr):  # TODO: gibt noch eine zweite Gleichung (siehe S. 99)

        if(C < 0):
            C = 0
            Itr = self._ITR(B,C)

        if(E < 0):
            E = 0
            Itf = self._ITF(B,C)

        q1 = self._q1(B-E,B-C)
        q2 = self._q2(Itf,Itr,self.IKR,self.IKF)
        return q1 / 2 * (1 + (1 + 4 * q2) ** self.NKF)

    def _ITF(self,BI, EI):
        if(BI < 1.6):
            lim = BI
        else:
            lim = 1.6
        return self.IS * (u.exp(BI - EI,1/(self.NF * self.UT),lim) - 1.0)

    def _ITR( self,BI,CI):

        if(BI < 1.6):
            lim = BI
        else:
            lim = 1.6
        return self.IS *self.ISSR * (u.exp(BI - CI,1/(self.NR * self.UT),lim) - 1.0)

    @jit
    def _IT(self,BI,CI,EI):

        self.itf = self._ITF(BI, EI)
        self.itr = self._ITR(BI, CI)
        q_b =  self._qb(BI,CI,EI,self.itf,self.itr)
        return (self.itf - self.itr)/q_b

    @jit
    def performCalculations(self):

        ubi = self.sys.getSolutionAt(self.bi).real
        uei = self.sys.getSolutionAt(self.ei).real
        uci = self.sys.getSolutionAt(self.ci).real

        if self.sys.atype == CircuitSystemEquations.ATYPE_NONE:
            print ("NPNTransportCurrent: WARNING: Analysis Type has to be set!")

        if self.sys.atype in [CircuitSystemEquations.ATYPE_DC, CircuitSystemEquations.ATYPE_TRAN]:

            self.current = self._IT(ubi,uci,uei)
            db_current = self._IT(ubi+self.diffh,uci,uei)
            dc_current = self._IT(ubi,uci+self.diffh,uei)
            de_current = self._IT(ubi,uci,uei+self.diffh)

            self.dub = (db_current-self.current)/self.diffh  # = dI_T/dub
            self.duc = (dc_current-self.current)/self.diffh   # = dI_T/duc
            self.due = -self.dub-self.duc #(de_current-self.current)/self.diffh   #TODO: Ueberpruefen !!!

            '''
            if(self.sys.getSolutionAt("N001")>= 0.773 and self.sys.curNewtonIteration == 1):
                print ("ubi: %G, uci: %G, uei: %G"%(ubi,uci,uei))
                print ("dub: %G, duc: %G, due: %G"%(self.dub,self.duc,self.due))
                print ("current: %G"%(self.current))
                print ("itf: %G , itr: %G"%(self.itf,self.itr))
                x = raw_input()
            '''

    def getq1(self):
        B = self.sys.getSolutionAt(self.bi).real
        E = self.sys.getSolutionAt(self.ei).real
        C = self.sys.getSolutionAt(self.ci).real
        return self._q1(B-E,B-C)

    def getqb(self):
        BI = self.sys.getSolutionAt(self.bi).real
        EI = self.sys.getSolutionAt(self.ei).real
        CI = self.sys.getSolutionAt(self.ci).real
        return self._qb(BI,CI,EI,self.itf[0],self.itr[0])

    def debugPrint(self):
        print(self.sys.compDict)
        ubi = self.sys.getSolutionAt(self.bi).real
        uei = self.sys.getSolutionAt(self.ei).real
        uci = self.sys.getSolutionAt(self.ci).real
        print ("ubi: %G, uci: %G, uei: %G"%(ubi,uci,uei))
        print ("dub: %G, duc: %G, due: %G"%(self.dub,self.duc,self.due))
        print("xmax: %G, idx:%i"%(np.amax(self.sys.x),np.argmax(self.sys.x)))
        #x = raw_input()

    def reloadParams(self):

        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec (variableExpr)

        self.NF = eval(self.paramDict.get("nf", "1"))
        self.NR = eval(self.paramDict.get("nr", "1"))
        self.IS = eval(self.paramDict.get("is", "1e-16"))
        self.ISSR = eval(self.paramDict.get("issr", "1"))
        self.UT = eval(self.paramDict.get("Ut", "0.026"))
        self.VEF = eval(self.paramDict.get("vef", "30"))
        self.VER = eval(self.paramDict.get("ver", "60"))
        self.IKF = eval(self.paramDict.get("ikf", "10e10"))
        self.IKR = eval(self.paramDict.get("ikr", "10e10"))
        self.NKF = eval(self.paramDict.get("nkf", "0.5"))
        self.FC = eval(self.paramDict.get("fc", "0.97"))
        self.AJE = eval(self.paramDict.get("aje", "-0.5"))
        self.AJC = eval(self.paramDict.get("ajc", "-0.5"))
        self.AJS = eval(self.paramDict.get("ajs", "-0.5"))
        self.PC = eval(self.paramDict.get("pc", "0.62"))
        self.PS = eval(self.paramDict.get("ps", "0.42"))
        self.PE = eval(self.paramDict.get("pe", "0.9"))
        self.ME = eval(self.paramDict.get("me", "0.105"))
        self.MC = eval(self.paramDict.get("mc", "0.12"))
        self.VRT = eval(self.paramDict.get("vrt", "0 "))  # TODO: Paramter von VBIC 1.2
        self.ART = eval(self.paramDict.get("art", "0.1"))  # TODO:  Paramter von VBIC 1.2