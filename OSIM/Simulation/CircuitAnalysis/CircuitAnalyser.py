from copy import deepcopy
import DCAnalysis as dc
import SParameterAnalysis as sp
import ACAnalysis as ac
import TransAnalysis as ta
import numpy as np
import matplotlib.pyplot as pp
from smithplot import SmithAxes

class CircuitAnalyser(object):

    SEMILOG_X = 0

    def __init__(self, sysEquations):
        self.sys = sysEquations
        #self.sys = deepcopy(sysEquations)
        self.components = self.sys.components
        self.hasDCPoint = False
        self.hasConvergenceProb = False

    '''
    ---------->  DC ANALYSIS <--------------------
    '''

    def calcDCOperatingPoint(self):
        converged = dc.calcDCOperatingPoint(self.sys)#dc.calcESTDCPoint(self.sys)#
        if(converged):
            self.hasDCPoint = True
        else:
            self.hasConvergenceProb = True
        return converged

    def getDCValAt(self,name):
        if(not self.hasDCPoint and not self.hasConvergenceProb):
            self.calcDCOperatingPoint()
        return self.sys.getSolutionAt(name)

    def getDCVoltageOver(self,name):
        """ function to get voltage between each combination of two nodes of a component
        :param name:
        :type name: string
        :return: List of tuples([NodeFrom,NodeTo]:voltage)
        :rtype: List of tuples
        """
        if(not self.hasDCPoint and not self.hasConvergenceProb):
            self.calcDCOperatingPoint()
        c = self.sys.getCompByName(name)
        ret = list()
        if(not c == None):
            pass
        return "blan"

    def getDCParamSweep(self,sw_param_name,sw_from,sw_to,sw_step,observables_list,stepable_name,stepables_vals_list):

        c = self.sys.getCompByName(sw_param_name)
        c.changeMyVoltageInSys(sw_from)
        dc.calcDCOperatingPoint(self.sys)

        return dc.getDCParamSweep(self.sys,sw_param_name,sw_from,sw_to,sw_step,observables_list,stepable_name,stepables_vals_list)

    def getDCOpAt(self,complist):
        if(not self.hasDCPoint and not self.hasConvergenceProb):
            self.calcDCOperatingPoint()
        ret = []
        for c in complist:
            ret.append(self.sys.getSolutionAt(c)[0].real)
        return ret

    def printDCOp(self,complist):
        if(not self.hasDCPoint and not self.hasConvergenceProb):
            self.calcDCOperatingPoint()
        if complist == None:
            dc.printDCOP(self.sys)
        else:
            for name in complist:
                if(self.sys.isVoltage( name)):
                    unit = "V"
                else:
                    unit = "A"
                print("%s : %G %s"%(name,self.sys.getSolutionAt(name).real,unit))

    '''
    ---------->  AC ANALYSIS <--------------------
    '''
    def getACAnalysis_semilogx(self,sigsourcename, obsNames, dec_from, dec_to, f_perDec):

        if(not self.hasDCPoint and not self.hasConvergenceProb):
            self.calcDCOperatingPoint()

        return ac.getACAnalysis_semilogx(deepcopy(self.sys), sigsourcename, obsNames, dec_from, dec_to, f_perDec)

    def getACAnalysis_linx(self,sigsourcename,obsNames,f_from,f_to,f_step):
        if(not self.hasDCPoint and not self.hasConvergenceProb):
            self.calcDCOperatingPoint()

        return ac.getACAnalysis_linx(deepcopy(self.sys), sigsourcename, obsNames, f_from, f_to, f_step)

    def getImpedanceAt(self,portname,freq):
        if(not self.hasDCPoint and not self.hasConvergenceProb):
            self.calcDCOperatingPoint()
        return ac.getImpedanceAt(deepcopy(self.sys),portname,freq)

    def getGain(self,signame,observeName,freq):
        if(not self.hasDCPoint and not self.hasConvergenceProb):
            self.calcDCOperatingPoint()
        f = np.asarray([freq], dtype=np.int64)

        res = ac.getACAnalysis(deepcopy(self.sys), signame,[observeName],f)[0]
        vals = res[0]
        for idx,p in enumerate(res[1]):
            if(p == observeName):
                return vals[idx+1][0]

    '''
    ---------->  SP ANALYSIS <--------------------
    '''
    def getS11At(self, Portname, freq):
        if(not self.hasDCPoint and not self.hasConvergenceProb):
            self.calcDCOperatingPoint()
        f = np.asarray([freq], dtype=np.int64)
        res = sp.getSPAnalysis(deepcopy(self.sys),f,[Portname])
        vals = res[0]
        for idx,p in enumerate(res[1]):
            if(p.name == Portname):
                return vals[idx+1, 0]


    def getSPAnalysis_linx(self,f_from, f_to, f_step,observeList):
         if(not self.hasDCPoint and not self.hasConvergenceProb):
            self.calcDCOperatingPoint()
         return sp.getSPAnalysis_linx(deepcopy(self.sys),f_from, f_to, f_step,observeList)


    def getSPAnalysis_semilogx(self,dec_from, dec_to, f_perDec,observeList):
         if(not self.hasDCPoint and not self.hasConvergenceProb):
            self.calcDCOperatingPoint()
         return sp.getSPAnalysis_semilogx(deepcopy(self.sys),dec_from, dec_to, f_perDec,observeList)

    '''
    ---------->  TRANS ANALYSIS <--------------------
    '''
    def getTrans(self,t_from, t_to, timeStep, observeList):
        if(not self.hasDCPoint and not self.hasConvergenceProb):
           self.calcDCOperatingPoint()
        return ta.getTransient(deepcopy(self.sys),t_from, t_to, timeStep, observeList)


    '''
    ---------->  PLOTS  <--------------------
    '''
    def plot_lin(self,res):

        resMat = res[0]
        f = pp.figure(13)
        f.suptitle(res[2])
        for r in range(resMat.shape[0]-1):
            pp.plot(resMat[0,:], resMat[r+1,:], 'b', label=(res[1][r]),color=np.random.rand(3,1))
            pp.grid(True,which="both",ls="-", color='0.65')
            f.show()

        pp.legend(loc="lower right", fontsize=12)
        pp.show()

    def plot_smith(self, res):

        ports = res[1]
        resMat = res[0]

        f = pp.figure(10,figsize=(6, 6))
        ax = pp.subplot(1, 1, 1, projection='smith', grid_major_fancy=False,
                                                    grid_minor_enable=True,
                                                    grid_minor_fancy=False)

        for idx,p in enumerate(ports):
           pp.plot(resMat[idx+1,:],label=p.name,datatype=SmithAxes.S_PARAMETER)

        pp.legend(loc="lower right",fontsize=12)
        pp.title(res[2])
        pp.show()
        f.show()

    def plot_semilogx(self, res):

        resMat = res[0]
        fig1 = pp.figure(1)
        fig1.suptitle(res[2])

        for r in range(resMat.shape[0]-1):
            pp.semilogx(resMat[0,:], resMat[r+1,:],c='r',label=(res[1][r]))
            pp.grid(True,which="both",ls="-", color='0.65')

        pp.legend(loc="lower right", fontsize=12)

        fig1.show()
        pp.show()
