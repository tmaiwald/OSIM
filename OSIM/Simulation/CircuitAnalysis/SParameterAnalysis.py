import numpy as np

from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations
from Modeling.Components.CurrentSource import CurrentSource
from Modeling.Components.Port import Port
from Modeling.Components.VoltageSource import VoltageSource


def getSPAnalysis_linx(sys,f_from, f_to, f_step,observeList):

    numSteps = int((f_to-f_from)/f_step)
    a =  np.asarray([f_from+x*f_step for x in range(numSteps)], dtype=np.int64)
    return getSPAnalysis(sys,a,observeList)

def getSPAnalysis_semilogx(sys,dec_from, dec_to, f_perDec,observeList):

    fs = list()
    for i in range(dec_from,dec_to+1):#decades
        fs += (range((10 ** i), (10 ** (i+1)), 10**i/f_perDec))

    a = np.asarray(fs, dtype=np.int64)
    return getSPAnalysis(sys,a,observeList)


def getSPAnalysis(sys, fs,observeList):

    ports = []
    portnames = []
    for b in sys.components:
        if isinstance(b,Port) and b.name in observeList:
            ports.append(b)
            portnames.append(b.name)

    if len(ports) == 0:
        print ("Error: No Ports in Netlist !")
        return

    sys.atype = CircuitSystemEquations.ATYPE_AC

    numbOfFreqs = fs.shape[0]
    resMat = np.zeros((len(ports)+1,numbOfFreqs), dtype=np.complex128)

    for pIdx,port in enumerate(ports):
        print(pIdx)
        ###anregende Spannungsquelle normieren:
        for b in sys.components:
            for c in b.internalComponents:
                if isinstance(c, VoltageSource):
                    c.changeMyVoltageInSys(0)

        # AC-Quelle auf Amplitude 1 setzen (Normierung)
        port.changeMyVoltageInSys(1)
        for i,f in enumerate(fs):
            print(f)
            resMat[0,i] = f
            for c in sys.components:
                if not isinstance(c, VoltageSource) and not isinstance(c, CurrentSource)\
                        and not isinstance(c, Port):
                    c.doStep(f)

                sys.x = np.linalg.solve(sys.A + sys.J, sys.b)
                Zout = (port.voltageOverMe()/port.myBranchCurrent())[0]
                resMat[pIdx+1,i] = (Zout-port.innerImpedance)/(port.innerImpedance+Zout)

    return [resMat,ports,"S11"]

