from OSIM.Optimizations import OptimizationAPI as o
from OSIM.Optimizations.OptimizationComponents.Optimizable import Optimizable as optis
from OSIM.Simulation.CircuitAnalysis.CircuitAnalysis import CircuitAnalysis
import math
from copy import copy
import numpy as np

class CostFunction(o.AbstractCostFunction):

     def __init__(self,constraintList,**kwargs):
         
         self.oldx = None
         self.oldA = None

     def getCost(self, ce , resultToFill):

        cost = 0
       
        ca = o.CircuitAnalyser(ce)
        ce.printComponents()
        np.set_printoptions(precision=1)
        #print(ce.A.shape)
        converged = ca.calcDCOperatingPoint()
        print(ce.compDict)
        res = CircuitAnalysis.newtonRaphson(ce)
        print(res[3])

        ca.printDCOp(["R3","R2","R1","R6"])
        print("A")
        print(ce.A.real)
        print("x")
        print(ce.x)
        
        if(not self.oldx == None):
            print("Differnez:")
            print(self.oldx - ce.x)
            print(self.oldA.real - ce.A.real)
        
        self.oldx = copy(ce.x)
        self.oldA = copy(ce.A)

        #print(ce.A)
        ca.plot_semilogx(ca.getACAnalysis_semilogx("V2",["OUT"],9,12,10)[0])

        '''hard constraints'''
    
        ''' optimizations '''
        mag = ca.getGain("V2","OUT",180e9)
        '''
        res = ca.getTrans(0,0.3e-10,1e-13,["Q3C","Q1C"])#,"LOPlus","RFPlus","RFIN1"])

        # how to get a diff-Signal
        out = np.zeros((2,res[0].shape[1]),dtype = np.float64)
        integ = 0
        for i in range(res[0].shape[1]):
            out[0][i] = (res[0])[0][i]
            out[1][i] = ((res[0])[1][i] - (res[0])[2][i])**2
            if (out[0][i] > 0.4e-10):
                integ += out[1][i]
        
        max = np.amax(out[1][:])
        '''
        if(math.isnan(mag)):
            mag = -100
        
        cost = -mag #-integ#-max
        resultToFill.setCost(cost)
        return cost

'''
setup optimization
'''

seq = o.CircuitSystemEquations(o.NetToComp('AmplifierTB.net').getComponents())

olist = [o.Optimizable(["R3"],"R",1250,1255),o.Optimizable(["R1"],"R",50000,50005),o.Optimizable(["R6"],"R",2000,2005)]
opti = o.BruteForceOptimizer(seq,olist,CostFunction(list()),10,o.SimpleResult(),None)
opti.run()


'''
result:
'''
ca = o.CircuitAnalyser(seq)
ca.plot_semilogx(ca.getACAnalysis_semilogx("V2",["OUT"],6,12,100)[0])

ranking = opti.getResults()
for r in ranking:
    print (r.toString())

seq.setParameterForCompsList(optis.getSetableList(ranking[0].getOptimizables()))

#ca = o.CircuitAnalyser(seq)
#ca.plot_semilogx(ca.getACAnalysis_semilogx("V2",["OUT"],6,12,100)[0])


'''
take results for DHS optimization
'''

opti = o.DownHillSimplexOptimizer(seq,olist,CostFunction(list()),10,o.SimpleResult(),None)

opti.setEdgesFromResultList(ranking)

opti.run()

ranking = opti.getResults()

seq.setParameterForCompsList(optis.getSetableList(ranking[0].getOptimizables()))

ca = o.CircuitAnalyser(seq)

ca.plot_semilogx(ca.getACAnalysis_semilogx("V2",["OUT"],6,12,100)[0])


