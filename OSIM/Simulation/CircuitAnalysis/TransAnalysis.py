

from __future__ import print_function
import numpy as np
from numba import jit
import time
from CircuitAnalysis import CircuitAnalysis as ca
from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations


@jit(nogil=True)
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

    start = time.time()

    for tIdx in range(1,absteps):
        sys.tnow = res[0][tIdx]
        remTime = (time.time() - start)/tIdx * ((res.shape[1]-tIdx))

        print("Trans.: t= %G, t_end = %G, %G %%, rem.time:%G  sec      "%(sys.tnow,res[0][-1],100*sys.tnow/(res[0][-1]-res[0][0]),remTime),end='\r')

        for b in sys.components:
                b.doStep(sys.tnow-sys.told)

        ca.newtonRaphson(sys)

        for i,o in enumerate(observeList):
            res[i+1][tIdx] = sys.getSolutionAt(o).real

        sys.xprev = sys.x
        sys.told  = sys.tnow

    print("                                                                                                  ",end='\r')

    return [res,observeList,"Transient"]


