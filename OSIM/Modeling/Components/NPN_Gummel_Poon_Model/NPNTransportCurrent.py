import numpy as np
from OSIM.Modeling.AbstractComponents.NonlinearComponent import NonlinearComponent

import OSIM.Simulation.Utils as u
from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations


class NPNTransportCurrent(NonlinearComponent):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(NPNTransportCurrent, self).__init__(nodes, name, value, superComponent, **kwargs)

        self.parseArgs(**kwargs)

        self.Is = eval(self.getMyParameterFromDictionary("Is", self.paramDict,"0"))
        self.Ut = eval(self.getMyParameterFromDictionary("Ut", self.paramDict,"0.026"))
        self.UA_N = eval(self.getMyParameterFromDictionary("VAF", self.paramDict,"30"))
        self.UA_I = eval(self.getMyParameterFromDictionary("VAR", self.paramDict,"60"))
        self.IK_N = eval(self.getMyParameterFromDictionary("IKF", self.paramDict,"10e10"))
        self.IK_I = eval(self.getMyParameterFromDictionary("IKR", self.paramDict,"10e10"))

        self.b = nodes[0]
        self.e = nodes[1]
        self.c = nodes[2]

        self.current = 0
        self.dub = 0
        self.duc = 0
        self.due = 0

    def setOPValues(self):
        ub = [0]
        ue = [0]
        if self.b is not '0':
            ub = self.sys.getSolutionAt(self.b).real
        if self.e is not '0':
            ue = self.sys.getSolutionAt(self.e).real
        self.opValues["S"] = self.Is/self.Ut*u.exp(ub-ue,1/self.Ut, 200)

    def initialSignIntoSysEquations(self):
        super(NPNTransportCurrent, self).initialSignIntoSysEquations()

    def doStep(self, freq_or_tau):

        if self.sys.atype == CircuitSystemEquations.ATYPE_AC:
            # acts as voltage dependent current source
            self.sys.g[self.sys.compDict.get(self.name)] = 0
            S = self.opValues.get("S")
            self.sys.b[self.bIdx] = S*self.Udiff([self.b, self.e])
            return

        self.sys.b[self.bIdx] = 0
        self.performCalculations()
        self.sys.g[self.sys.compDict.get(self.name)] = self.current


        if self.b is not '0':
            self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.b), self.dub)

        if self.c is not '0':
            self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.c), self.duc)

        if self.e is not '0':
            self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.e), self.due)

    def containsNonlinearity(self):
        return True

    def getCurrent(self):
        return self.current

    def performCalculations(self):

        ub = 0
        uc = 0
        ue = 0

        if self.b is not '0':
            ub = self.sys.getSolutionAt(self.b).real
        if self.c is not '0':
            uc = self.sys.getSolutionAt(self.c).real
        if self.e is not '0':
            ue = self.sys.getSolutionAt(self.e).real

        ube = ub - ue
        ubc = ub - uc
        uce = uc - ue

        if self.sys.atype == CircuitSystemEquations.ATYPE_NONE:
            print("NPNTransportCurrent: WARNING: Analysis Type has to be set!")

        if self.sys.atype in [CircuitSystemEquations.ATYPE_DC,CircuitSystemEquations.ATYPE_TRAN]:

            BEMAX = 0.6
            CEMIN = 0.0

            # Normalbetrieb :

            if ube < BEMAX and uce > CEMIN:
                a = np.exp(ube/self.Ut)
                b = np.exp(ubc/self.Ut)
                qb = self.qb(ub, uc, ue, a, b)

                self.current = self.Is/qb*(a-b)

                self.dub = self.current/self.Ut# = dI_T/dub

                self.duc = self.Is / (qb * self.Ut) * b# = dI_T/duc

                self.due = -  self.Is /(qb * self.Ut) * a# = dI_T/due


            if ube > BEMAX and uce > CEMIN:

                a = np.exp(BEMAX/self.Ut)
                b = np.exp((BEMAX-uc)/self.Ut)
                qb = self.qb(BEMAX, uc, ue, a, b)

                i_bemax = self.Is/qb*(a-b)
                m = i_bemax/self.Ut
                self.current = i_bemax + m * (ube-BEMAX)

                self.dub = m# = dI_T/dub

                self.duc = self.Is / (qb * self.Ut) * b# = dI_T/duc

                self.due = -  self.Is /(qb * self.Ut) * a# = dI_T/due


            if ube < BEMAX and uce < CEMIN :

                a = np.exp(ube/self.Ut)

                icmin =  self.Is*(a-np.exp((ube-CEMIN)/self.Ut))
                m = self.Is/self.Ut*np.exp((ube-CEMIN)/self.Ut)
                self.current =  icmin + m * (uce-CEMIN)

                self.dub = icmin/self.Ut# = dI_T/dub -entspricht Anstieg am Rand

                self.duc = m# = dI_T/duc

                self.due = - self.Is /(self.Ut) * a# = dI_T/due


            if ube > BEMAX and uce < CEMIN :
                #im vierten Quadraten starten wir auf Linie entlang BEMAX und CEMIN
                a = self.Is*(np.exp((BEMAX)/self.Ut)-np.exp((BEMAX-CEMIN)/self.Ut))
                mb = a/self.Ut
                start = a + mb * (ube-BEMAX)
                #von der Linie aus in c-Richtung linear extrapliert
                mc = self.Is/self.Ut*np.exp((BEMAX-CEMIN)/self.Ut)
                self.current = start + mc * (uce-CEMIN)

                self.dub = mb# = dI_T/dub -entspricht Anstieg am Rand

                self.duc = mc# = dI_T/duc

                self.due = mb - mc# = dI_T/due ?????????




    def qb(self, ub, uc, ue, a, b):

        q1 = 1 / (1 - ((ub - ue) / self.UA_I) - ((ub - uc) / self.UA_N))

        s1 = self.Is / self.IK_N * (a - 1)
        s2 = self.Is / self.IK_I * (b - 1)
        # qb = aequivalente Basisladung (oa. Majoritaetstraegerladung)
        q2 = s1 + s2
        return (q1 / 2 * (1 + np.sqrt(1 + 4 * q2))).real

