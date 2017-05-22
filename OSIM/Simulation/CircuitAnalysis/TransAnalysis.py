import numpy as np
from numba import jit

from CircuitAnalysis import CircuitAnalysis as ca
from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations


@jit
def getTransient(sys,t_from, t_to, timeStep, observeList):

    abTime = t_to-t_from
    absteps = np.int(np.floor(abTime/timeStep))
    #zeitvektor
    res = np.zeros((len(observeList)+1,absteps),dtype=np.float64)

    #TODO: timeline starts after the first timestep!!!! Weil der Wert a
    for t in range(absteps):
        res[0][t] = t*timeStep

    sys.xprev = sys.x #TODO: kommt hier bisschen aus der Luft- kommentieren oder besser loesen
    sys.atype = CircuitSystemEquations.ATYPE_TRAN

    for i,o in enumerate(observeList):
        res[i+1][0] = sys.getSolutionAt(o).real

    for tIdx in range(1,absteps):
        sys.tnow = res[0][tIdx]
        print("t= %G, t_end = %G, %G %%        \r"%(sys.tnow,res[0][-1],100*sys.tnow/(res[0][-1]-res[0][0])))

        for b in sys.components:
                b.doStep(sys.tnow-sys.told)

        ca.newtonRaphson(sys)

        for i,o in enumerate(observeList):
            res[i+1][tIdx] = sys.getSolutionAt(o).real

        sys.xprev = sys.x
        sys.told  = sys.tnow

    return [res,observeList,"Transient"]


