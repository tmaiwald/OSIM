from numba import jit

from OSIM.Modeling.AbstractComponents.NonlinearComponent import NonlinearComponent
from OSIM.Modeling.Components.Diode import Diode


class IBCP(NonlinearComponent):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        self.isExternal = False
        super(IBCP, self).__init__(nodes, name, value, superComponent, **kwargs)

        self.si = nodes[0]
        self.bp = nodes[1]

        '''
        TODO: Defaultwerte anpassen
        '''

        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec (variableExpr)

        self.UT = eval(self.paramDict.get("ut", "0.026"))
        self.IBCIP = eval(self.paramDict.get("ibcip", "2E-15"))
        self.IBCNP = eval(self.paramDict.get("ibcnp", "5E-15"))
        self.NCIP = eval(self.paramDict.get("ncip", "1"))
        self.NCNP = eval(self.paramDict.get("ncnp", "1"))
        self.Udlim = eval(self.paramDict.get("Udlim", "1.5"))

    @jit
    def performCalculations(self):

        usi = self.sys.getSolutionAt(self.si).real
        ubp = self.sys.getSolutionAt(self.bp).real

        ubcp = usi - ubp

        ideal = Diode.curr(1, self.IBCIP, ubcp, 1 / (self.UT * self.NCIP))
        nonideal = Diode.curr(1, self.IBCNP, ubcp, 1 / (self.UT * self.NCNP))

        self.current = ideal + nonideal
        self.gd = Diode.gdiff(ideal, self.NCIP, self.UT) + Diode.gdiff(nonideal, self.NCNP, self.UT)

    def reloadParams(self):

        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec (variableExpr)

        self.UT = eval(self.paramDict.get("ut", "0.026"))
        self.IBCIP = eval(self.paramDict.get("ibcip", "2E-15"))
        self.IBCNP = eval(self.paramDict.get("ibcnp", "5E-15"))
        self.NCIP = eval(self.paramDict.get("ncip", "1"))
        self.NCNP = eval(self.paramDict.get("ncnp", "1"))
        self.Udlim = eval(self.paramDict.get("Udlim", "1.5"))