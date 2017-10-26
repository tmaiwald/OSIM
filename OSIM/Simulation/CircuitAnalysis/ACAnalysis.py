import numpy as np
from numba import jit
from scipy.sparse.linalg import spsolve
import scipy as np
import numpy
from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations
from OSIM.Modeling.Components.Port import Port
from OSIM.Modeling.Components.VoltageSource import VoltageSource

@jit
def getACAnalysis(sys, sigsourcename, obsNames, fs):

    numbOfFreqs = fs.shape[0]
    resMatMag = np.zeros((len(obsNames)+1,numbOfFreqs), dtype=np.float64)
    resMatPhase = np.zeros((len(obsNames)+1,numbOfFreqs), dtype=np.float64)

    for i,f in enumerate(fs):
        resMatMag[0,i] = f
        resMatPhase[0,i] = f

    xIdxOfObserves = np.zeros((len(obsNames),1), dtype=numpy.int)
    for i,o in enumerate(obsNames):
        xIdxOfObserves[i] = sys.compDict.get(o)
    ###anregende Spannungsquelle normieren:

    for b in sys.components:
            if isinstance(b, VoltageSource) or isinstance(b,Port):
                b.changeMyVoltageInSys(0)
            if b.name == sigsourcename:
                b.changeMyVoltageInSys(1.0)

    sys.atype = CircuitSystemEquations.ATYPE_AC

    for freqIdx in range(numbOfFreqs):
        freq = resMatMag[0,freqIdx]
        for b in sys.components:
            b.doStep(freq)
        if(sys.n > 1000):
            sys.x = spsolve(sys.A + sys.J, sys.b, permc_spec="NATURAL")
        else:
            sys.x = np.linalg.solve(sys.A + sys.J, sys.b)

        for obsIdx in range(len(obsNames)):
            xIdx = xIdxOfObserves[obsIdx]
            resMatMag[obsIdx+1,freqIdx] = np.sqrt((sys.x[xIdx].real)**2 + (sys.x[xIdx].imag)**2)
            resMatPhase[obsIdx+1,freqIdx] = np.angle(sys.x[xIdx], deg=True)

    resmag = [resMatMag,obsNames,"Magnitude"]
    resphase = [resMatPhase,obsNames,"Phase"]

    return [resmag,resphase]

def getImpedanceAt(sys,portname,freq):

    port = sys.getCompByName(portname)
    f = np.asarray([freq,freq+1,freq+2], dtype=np.int64)
    getACAnalysis(sys,portname,[port.InnerNode],f)
    Z = port.voltageOverMe()/port.myBranchCurrent()
    return Z


def getACAnalysis_linx(sys, sigsourcename, obsNames, f_from, f_to, f_step):

    numSteps = int((f_to-f_from)/f_step)
    a =  np.asarray([f_from+x*f_step for x in range(numSteps)], dtype=np.int64)
    return getACAnalysis(sys, sigsourcename, obsNames, a)

def getACAnalysis_semilogx(sys, sigsourcename, obsNames, dec_from, dec_to, f_perDec):

    fs = list()
    for i in range(dec_from,dec_to):#decades
        fs += (range((10 ** i), (10 ** (i+1)), 10**i/f_perDec))

    a = np.asarray(fs, dtype=np.int64)
    return getACAnalysis(sys, sigsourcename, obsNames, a)

