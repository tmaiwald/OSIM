from copy import copy

import numpy as np

from CircuitAnalysis import CircuitAnalysis as ca
from OSIM.Modeling.AbstractComponents.NonlinearComponent import NonlinearComponent
from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations
from OSIM.Modeling.Components.Port import Port
from OSIM.Modeling.Components.VoltageSource import VoltageSource
from OSIM.Simulation.NRConvergenceException import NRConvergenceException


def calcDCOperatingPoint(sys):

        sys.atype = CircuitSystemEquations.ATYPE_DC
        converged = True
        '''
         Ziel ist es alle Spannungsquellen schrittweise auf Ziel-DC-Spannung
         zu bringen, damit der initiale Schaetzvektor x nicht so weit vom Ziel ent
         fernt ist.
        '''

        start = 0.1
        STEPS = 100
        loadVoltages  = list()
        for c in sys.components:
            if (isinstance(c,VoltageSource) or isinstance(c,Port)):
                incVoltPerStep = (c.value-start)/STEPS
                target = c.value
                d = (c,incVoltPerStep,target)
                loadVoltages.append(d)

        for d in loadVoltages:
            d[0].changeMyVoltageInSys(start)

        for i in range(STEPS):
            for d in loadVoltages:
                if(not d[0].value == d[2]):
                    d[0].changeMyVoltageInSys(d[0].value+d[1])
            ca.newtonRaphson(sys)

        for b in sys.components:
            b.setOPValues()

        return converged


def valForDCPointAt(sys,sweepable_name,sweep_from,sweep_to,condition):


    res_list = np.zeros()
    comp = sys.getCompByName(sweepable_name)

    comp.setValue(sweep_from)



def calcESTDCPoint(sys):


    tryCount = 0
    converged = False

    while tryCount < 10 and not converged:
        sys.reset()
        print(tryCount)
        sys.atype = CircuitSystemEquations.ATYPE_EST_DC
        for b in sys.components:
            for c in b.internalComponents:
                if isinstance(c,NonlinearComponent):
                    c.setAlpha(tryCount*0.1)

        try:
            ca.newtonRaphson(sys)
        except NRConvergenceException:
            tryCount+=1
            continue
        else:
            converged = True

        print("hier1")

        estx = copy(sys.x)
        estb = copy(sys.b)

        sys.atype = CircuitSystemEquations.ATYPE_DC
        sys.reset()
        sys.x = copy(estx)
        sys.b = copy(estb)
        ca.nonlin(sys)

        try:
            ca.newtonRaphson(sys)
        except NRConvergenceException:
            tryCount+=1
            continue
        else:
            converged = True


    for b in sys.components:
            b.setOPValues()

    return True

def calcDCOperatingPoint_convhelper(sys):

    sys.atype = CircuitSystemEquations.ATYPE_DC
    converged = True

    STEPS = 1000

    for s in range(STEPS):
        for b in sys.components:
            for c in b.internalComponents:
                if isinstance(c,NonlinearComponent):
                    c.convergenceHelp(s,STEPS)
        ca.newtonRaphson(sys)

    for b in sys.components:
        b.setOPValues()

    return converged

def getsoftDCOperatingPoint(sys):

        sys.atype = CircuitSystemEquations.ATYPE_DC
        converged = True
        '''
         Ziel ist es alle Spannungsquellen schrittweise auf Ziel-DC-Spannung
         zu bringen, damit der initiale Schaetzvektor x nicht so weit vom Ziel ent
         fernt ist.
        '''
        STEPS = 1000
        loadVoltages  = list()
        for c in sys.components:
            if (isinstance(c,VoltageSource) or isinstance(c,Port)):
                incVoltPerStep = c.value/STEPS
                target = c.value
                d = (c,incVoltPerStep,target)
                loadVoltages.append(d)

        old_i_for_conv = 10000
        i_for_conv = 0
        tryCount = 0
        all_sources_at_target = False

        for d in loadVoltages:
            d[0].changeMyVoltageInSys(0.2)

        while(not all_sources_at_target):
            for d in loadVoltages:
                if(not d[0].value == d[2]):
                    d[0].changeMyVoltageInSys(d[0].value+d[1])

                else:
                    continue
                i_for_conv = ca.newtonRaphson(sys)[3]
                if(i_for_conv > 5 and i_for_conv > 2*old_i_for_conv):
                    d[0].changeMyVoltageInSys(d[0].value-d[1])
                    i_for_conv = ca.newtonRaphson(sys)[3]
                    tryCount += 1
                    print(tryCount)

                old_i_for_conv = i_for_conv
            all_sources_at_target = True
            for d in loadVoltages:
                if(not d[0].value == d[2]):
                   all_sources_at_target = False
                   break
                else:
                   print(d[0].value)

            if(tryCount > 30):
                for d in loadVoltages:
                    print(d[0].value)
                converged = False
                raise NRConvergenceException

        for b in sys.components:
            b.setOPValues()

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

            resMat[1+oidx,swidx] = (sys.getSolutionAt(observables_list[oidx])[0]).real

    return [resMat,observables_list,"DC Sweep"]

