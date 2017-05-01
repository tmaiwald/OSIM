import numpy as np
from numba import jit

import Simulation.Utils as u
from Modeling.AbstractComponents.NonlinearComponent import NonlinearComponent
from Modeling.CircuitSystemEquations import CircuitSystemEquations as ce


class IRCI(NonlinearComponent):  # behaves like a currentsource

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(IRCI, self).__init__(nodes, name, value, superComponent, **kwargs)

        self.hdiff = 0.00001

        self.cx = nodes[0]  # from
        self.ci = nodes[1]  # to
        self.bi = nodes[2]

        Nx = eval(self.paramDict.get("Nx", "1"))
        self.UT = eval(self.paramDict.get("ut", "0.026"))
        self.VO = eval(self.paramDict.get("vo", "0.8"))
        self.GAMM = eval(self.paramDict.get("gamm", "0.8"))
        self.RCI = eval(self.paramDict.get("rci", "0.8"))

        self.gdbi = 0
        self.gdci = 0
        self.gdcx = 0

    def setOPValues(self):
        self.performCalculations()
        self.opValues["S"] = self.gdci + self.gdbi  # self.Is / self.Ut * u.exp(ub - ue, 1 / self.Ut, 200)

    @jit
    def doStep(self, freq_or_tau):

        if self.sys.atype == ce.ATYPE_AC:
            # acts as voltage dependent current source
            self.sys.g[self.sys.compDict.get(self.name)] = 0
            S = self.opValues.get("S")
            self.sys.b[self.bIdx] = S * self.Udiff([self.cx, self.ci])
            return

        self.sys.b[self.bIdx] = 0
        self.performCalculations()
        self.sys.g[self.sys.compDict.get(self.name)] = self.current

        self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.cx), self.gdcx)
        self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.ci), self.gdci)
        self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.bi), self.gdbi)


    def initialSignIntoSysEquations(self):
        branchIdx = self.sys.compDict.get(self.name)
        nodeIdx_cx = self.sys.compDict.get(self.cx)
        nodeIdx_ci = self.sys.compDict.get(self.ci)

        self.sys.A[branchIdx, branchIdx] = -1
        self.sys.A[nodeIdx_cx, branchIdx] = 1
        self.sys.A[nodeIdx_ci, branchIdx] = -1


    @jit
    def performCalculations(self):
        ucx = self.sys.getSolutionAt(self.cx).real
        uci = self.sys.getSolutionAt(self.ci).real
        ubi = self.sys.getSolutionAt(self.bi).real

        self.current = self.irci(uci, ubi, ucx)

        ##Ableitungen:
        # in Richtung Anschluesse der Stromquelle
        self.gdbi = (self.irci(uci, ubi + self.hdiff, ucx) - self.current) / self.hdiff
        self.gdci = (self.irci(uci + self.hdiff, ubi, ucx) - self.current) / self.hdiff
        self.gdcx = (self.irci(uci, ubi, ucx + self.hdiff) - self.current) / self.hdiff

    @jit
    def irci(self, uci, ubi, ucx):

        ubici = ubi - uci
        ubicx = ubi - ucx
        KBCI = np.sqrt(1 + self.GAMM * u.exp(ubici, 1 / self.UT, 0.6))
        KBCX = np.sqrt(1 + self.GAMM * u.exp(ubicx, 1 / self.UT, 0.6))
        ucorr = self.UT * (KBCI - KBCX - np.log10((1 + KBCI) / (1 + KBCX)))
        Iohm = (ubicx - ubici + ucorr)
        return Iohm / np.sqrt(1 + (self.RCI * Iohm / self.VO) ** 2)




