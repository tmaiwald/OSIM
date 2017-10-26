from __future__ import print_function
from copy import copy
import numpy as np
from numba import jit
from CircuitAnalysis import CircuitAnalysis as ca
from OSIM.Modeling.AbstractComponents.NonlinearComponent import NonlinearComponent
from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations
from OSIM.Modeling.Components.Port import Port
from OSIM.Modeling.Components.VoltageSource import VoltageSource
from OSIM.Simulation.NRConvergenceException import NRConvergenceException

"""
@jit(nogil=True)
def _subVoltageStepping(start,stop,sys,oldStepSize,loadVoltages):

    v = np.arange(start,stop,oldStepSize/10)

    for d in loadVoltages:
        if (not d[0].value == d[2]):
            d[0].changeMyVoltageInSys(d[0].value + d[1])
    ca.nonlin(sys)

    res = ca.newtonRaphson(sys)
    if (res[3] >= ca.MAX_NEWTON_ITERATIONS):
        _subVoltageStepping(d[0].value - d[1])
        break
"""

@jit(nogil=True)
def calcDCOperatingPoint(sys):

        sys.atype = CircuitSystemEquations.ATYPE_DC
        converged = True
        '''
         Ziel ist es alle Spannungsquellen schrittweise auf Ziel-DC-Spannung
         zu bringen, damit der initiale Schaetzvektor x nicht so weit vom Ziel ent
         fernt ist.
        '''

        start = 0.1
        STEPS = [50,100,200]

        attempt = 0
        loadVoltages  = list()

        while attempt < len(STEPS)-1:

            for c in sys.components:
                if (isinstance(c,VoltageSource) or isinstance(c,Port)):
                    incVoltPerStep = (c.value-start)/STEPS[attempt]
                    target = c.value
                    d = (c,incVoltPerStep,target)
                    loadVoltages.append(d)

            for d in loadVoltages:
                d[0].changeMyVoltageInSys(start)

            gmin = np.arange(1e-12, 1e-11, (1e-11 - 1e-12) / float(STEPS[attempt]),np.float64)

            for i in range(STEPS[attempt]):
                sys.gmin = gmin[-i-1]
                for d in loadVoltages:
                    if(not d[0].value == d[2]):
                        d[0].changeMyVoltageInSys(d[0].value+d[1])
                res = ca.newtonRaphson(sys)
                if (res[3] >= ca.MAX_NEWTON_ITERATIONS):
                    #_subVoltageStepping(d[0].value-d[1])
                    break

            if(res[3] >= ca.MAX_NEWTON_ITERATIONS):
                converged = False
                sys.reset()
                sys.atype = CircuitSystemEquations.ATYPE_DC
            else:
                for b in sys.components:
                    b.setOPValues()
                return True

            attempt+=1

        return converged

def printDCOP(sys):

    print ("DCOPS: ->")
    for k in sys.compDict.keys():
        print(str(k) + " " + str(sys.x[sys.compDict.get(k)]))
    print ("<- DCOPS")

def getDCParamSweep(sys,sw_param_name,sw_from,sw_to,sw_step,observables_list,stepable_name,stepables_vals_list):

    if(len(stepables_vals_list) > 1):
        print("getDCParamSweep(): not implemented !!")

    sys.atype = CircuitSystemEquations.ATYPE_DC

    sweep =  np.arange(sw_from,sw_to,sw_step)
    resMat = np.zeros((len(observables_list)+1,len(sweep)), dtype=np.float64)

    for swidx,val in enumerate(sweep):

        resMat[0,swidx]=val
        for b in sys.components:
            if b.name == sw_param_name:
                print(val)
                b.changeMyVoltageInSys(val)
        for oidx,step in enumerate(observables_list):
            for b in sys.components:
                if b.name == stepable_name:
                    b.changeMyVoltageInSys(stepables_vals_list[0])
            try:
                ca.newtonRaphson(sys)
            except NRConvergenceException:
                print("Convergence problem at: ")
                print("sweep %s: %G"%(sw_param_name,val))
                #print("step %s : %G"%(stepable_name,step))

            resMat[1+oidx,swidx] = (sys.getSolutionAt(observables_list[oidx])).real

    return [resMat,observables_list,"DC Sweep"]

