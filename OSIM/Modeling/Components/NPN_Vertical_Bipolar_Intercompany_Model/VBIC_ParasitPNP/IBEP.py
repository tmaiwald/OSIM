from numba import jit

from OSIM.Modeling.AbstractComponents.NonlinearComponent import NonlinearComponent
from OSIM.Modeling.Components.Diode import Diode


class IBEP(NonlinearComponent):

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(IBEP, self).__init__(nodes, name, value, superComponent, **kwargs)

        self.bx = nodes[0]
        self.bp = nodes[1]

        '''
        TODO: Defaultwerte anpassen
        '''

        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec (variableExpr)
        self.UT = eval(self.paramDict.get("ut", "0.026"))
        self.IBEIP = eval(self.paramDict.get("ibeip", "4E-19"))
        self.IBENP = eval(self.paramDict.get("ibenp", "2E-14"))
        self.NCN = eval(self.paramDict.get("ncn", "1"))
        self.NCI = eval(self.paramDict.get("nci", "1"))
        self.Udlim = eval(self.paramDict.get("Udlim", "1.5"))



    @jit
    def performCalculations(self):

        ubx = self.sys.getSolutionAt(self.bx).real
        ubp = self.sys.getSolutionAt(self.bp).real

        ubep = ubx - ubp

        ideal = Diode.curr(1, self.IBEIP, ubep, 1 / (self.UT * self.NCI))
        nonideal = Diode.curr(1, self.IBENP, ubep, 1 / (self.UT * self.NCN))
        self.current = ideal + nonideal
        self.gd = Diode.gdiff(ideal, self.NCI, self.UT) + Diode.gdiff(nonideal, self.NCI, self.UT)

    def reloadParams(self):

        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec (variableExpr)

        self.UT = eval(self.paramDict.get("ut", "0.026"))
        self.IBEIP = eval(self.paramDict.get("ibeip", "4E-19"))
        self.IBENP = eval(self.paramDict.get("ibenp", "2E-14"))
        self.NCN = eval(self.paramDict.get("ncn", "1"))
        self.NCI = eval(self.paramDict.get("nci", "1"))
        self.Udlim = eval(self.paramDict.get("Udlim", "1.5"))