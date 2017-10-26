from OSIM.Optimizations import OptimizationAPI as o
import numpy as np

class CostFunction(o.AbstractCostFunction):

     def getCost(self, ce , resultToFill):

        ca = o.CircuitAnalyser(ce)
        converged = ca.calcDCOperatingPoint()

        '''hard constraints'''
        if(not converged):
            cost = 1000
            resultToFill.setCost(cost)
            return cost

        mag = ca.getGain("V2","OUT",10e10)
        cost = - mag
        resultToFill.setCost(cost)

        return cost

'''
setup optimization
'''

seq = o.CircuitSystemEquations(o.NetToComp('AmplifierTB.net').getComponents())

olist = [o.Optimizable(["R3"],"R",600,1800),
        o.Optimizable(["R1"],"R",50000,80000)]
        #o.Optimizable(["Q1"],"Nx",1,8)]
        
opti = o.DownHillSimplexOptimizer(seq,olist,CostFunction(list()),10,o.SimpleResult(),None)
opti.run()


'''
result:
'''
ca = o.CircuitAnalyser(seq)
ca.plot_semilogx(ca.getACAnalysis_semilogx("V2",["OUT"],6,12,100)[0])

ranking = opti.getResults()
for r in ranking:
    print (r.toString())

seq = o.CircuitSystemEquations(o.NetToComp('AmplifierTB.net').getComponents())

for op in ranking[0].getOptimizables():
    val = op.getValue()
    for c in op.getOptimizableComponentNames():
        seq.setValueForCompName(val[0],c)

ca = o.CircuitAnalyser(seq)
ca.printDCOp(["Q1IT"])
ca.plot_semilogx(ca.getACAnalysis_semilogx("V2",["OUT"],6,12,100)[0])
ca.plot_smith(ca.getSPAnalysis_semilogx(8,11,10,"V2"))
