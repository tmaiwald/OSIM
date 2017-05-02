from OSIM.Optimizations import OptimizationAPI as o
import numpy as np

class CostFunction(o.AbstractCostFunction):

     def getCost(self, ce , resultToFill):

        ca = o.CircuitAnalyser(ce)
        converged = ca.calcDCOperatingPoint()

        '''hard constraints'''
        if(not converged and ce.getSolutionAt("Q7IT") < 1e-3 and ce.getSolutionAt("Q9IT") < 1e-3):
            cost = 1000
            resultToFill.setCost(cost)
            return cost

        ''' optimizations '''
        #mag = ca.getGain("V2","OUT1",18e9)
        res = ca.getTrans(0,0.5e-6,1e-8,["OUT2","OUT1"])

        # how to get a diff-Signal
        out = np.zeros((2,res[0].shape[1]),dtype = np.float64)
        for i in range(res[0].shape[1]):
            out[0][i] = (res[0])[0][i]
            out[1][i] = (res[0])[1][i] - (res[0])[2][i]

        max = np.amax(np.absolute(out[1][:]))
        print("Max: %G"%max)

        cost = - max
        resultToFill.setCost(cost)
        return cost


'''
setup optimization
'''

seq = o.CircuitSystemEquations(o.NetToComp('LoBuffer/LoBuffer.net').getComponents())
cf = CostFunction(list()) # no constraints defined

olist = [o.Optimizable(["R1","R3"],400,800),o.Optimizable(["R2","R4"],400,800),o.Optimizable(["R16","R14"],30000,50000)]

opti = o.BruteForceOptimizer(seq,olist,CostFunction(list()),10,o.SimpleResult(),None)

opti.run()

'''
result:
'''
ca = o.CircuitAnalyser(seq)
ca.plot_semilogx(ca.getACAnalysis_semilogx("V2",["OUT1"],5,12,10)[0])

ranking = opti.getResults()
for r in ranking:
    print (r.toString())

seq = o.CircuitSystemEquations(o.NetToComp('LoBuffer/LoBuffer.net').getComponents()) #TODO: BUG

for op in ranking[0].getOptimizables():
    val = op.getValue()
    for c in op.getOptimizableComponentNames():
        seq.setValueForCompName(val,c)

ca = o.CircuitAnalyser(seq)
ca.plot_semilogx(ca.getACAnalysis_semilogx("V2",["OUT1"],5,12,10)[0])
