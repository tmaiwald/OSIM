import numpy as np
from numba import jit

import Simulation.Utils as u
from Modeling.AbstractComponents.NonlinearComponent import NonlinearComponent
from Modeling.CircuitSystemEquations import CircuitSystemEquations


class ParasitTransportCurrent(NonlinearComponent):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(ParasitTransportCurrent, self).__init__(nodes, name, value, superComponent, **kwargs)
        if(self.COMPONENT_PRINT_WARNINGS):
            print (name+"Warning: Reacht-Through-Effekt not implemented!")

        self.diffh = 0.000001

        vbic_is = 1  # TODO: !!
        vbic_is_mm = 1  # TODO: !!!

        Nx = eval(self.paramDict.get("Nx", "1"))
        self.NFP = eval(self.paramDict.get("nfp", "1"))
        self.ISP = eval(self.paramDict.get("isp", "1e-16"))
        self.UT = eval(self.paramDict.get("Ut", "0.026"))
        self.WSP = eval(self.paramDict.get("wsp", "1"))
        self.IKP = eval(self.paramDict.get("ikp", "1E-04*(Nx*0.25)"))

        if(not self.WSP == 1):
            print(name+" Warning: geometric factor WSP ist not implemented yet!!" )

        self.bx = nodes[0]
        self.bp = nodes[1]
        self.si = nodes[2]

        self.itfp = 0
        self.itrp = 0
        self.current = 0
        self.qb = 0
        self.dubx = 0
        self.dusi = 0
        self.dubp = 0

    def setOPValues(self):

        self.performCalculations()
        self.opValues["S"] = self.dubx

    def initialSignIntoSysEquations(self):
        branchIdx = self.sys.compDict.get(self.name)
        nodeIdx_bx = self.sys.compDict.get(self.bx)
        nodeIdx_si = self.sys.compDict.get(self.si)

        self.sys.A[branchIdx, branchIdx] = -1
        self.sys.A[nodeIdx_bx, branchIdx] = 1
        self.sys.A[nodeIdx_si, branchIdx] = -1

    @jit
    def doStep(self, freq_or_tau):

        if self.sys.atype == CircuitSystemEquations.ATYPE_AC:
            # acts as voltage dependent current source
            self.sys.g[self.sys.compDict.get(self.name)] = 0
            S = self.opValues.get("S")
            if(self.COMPONENT_PRINT_WARNINGS):
                print("Parasist Current Source  -TODO: !!!!")
            self.sys.b[self.bIdx] = S * self.Udiff([self.bx, self.bp])
            return

        self.performCalculations()
        self.sys.g[self.sys.compDict.get(self.name)] = self.current

        self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.bx), self.dubx)
        self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.si), self.dusi)
        self.putJ(self.sys.J, self.bIdx, self.sys.compDict.get(self.bp), self.dubp)

    def containsNonlinearity(self):
        return True

    def getCurrent(self):
        return self.current

    @jit
    def performCalculations(self):

        ubx = self.sys.getSolutionAt(self.bx).real
        ubp = self.sys.getSolutionAt(self.bp).real
        usi = self.sys.getSolutionAt(self.si).real

        if self.sys.atype == CircuitSystemEquations.ATYPE_NONE:
            print ("NPNTransportCurrent: WARNING: Analysis Type has to be set!")

        if self.sys.atype in [CircuitSystemEquations.ATYPE_DC, CircuitSystemEquations.ATYPE_TRAN]:

            self.Itfp = self.ISP * (u.exp((ubx-ubp),1/(self.NFP*self.UT),1) - 1.0)
            self._qb(ubp,ubx) # qb nur einmal berechnen statt 4 mal
            self.current = self.I_T(ubx,ubp,usi)
            self.dubx = (self.I_T(ubx+self.diffh,ubp,usi) - self.current)/self.diffh
            self.dusi = (self.I_T(ubx,ubp,usi+self.diffh) - self.current)/self.diffh
            self.dubp = (self.I_T(ubx,ubp+self.diffh,usi) - self.current)/self.diffh

    @jit
    def I_T(self,BX,BP,SI):

        self.Itfp = self.ISP * (u.exp((BX-BP),1/(self.NFP*self.UT),BP) - 1.0)
        self.Itrp = self.ISP * (u.exp((SI-BP),1/(self.NFP*self.UT),BP) - 1.0)
        self._qb(BP,BX)
        return (self.Itfp-self.Itrp)/self.qb

    def _qb(self,BP,BX):
        if(BP < 0):
            q2p = self.ISP * (u.exp((BX),1/(self.NFP*self.UT),BP) - 1.0)
        else:
            q2p = self.Itfp/self.IKP
        self.qb = 0.5*(1+np.sqrt(1+4*q2p))

    def ditrp_A(self):
        return self.itrp /(self.NFP*self.UT)
