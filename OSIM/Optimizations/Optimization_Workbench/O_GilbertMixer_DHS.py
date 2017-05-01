from Optimizations import OptimizationAPI as o
import numpy as np
import math

class CostFunction(o.AbstractCostFunction):

     def getCost(self, ce , resultToFill):

        cost = 0
        ca = o.CircuitAnalyser(ce)

        converged = ca.calcDCOperatingPoint()

        '''hard constraints'''
        if(not converged and ce.getSolutionAt("Q7IT") < 1e-3 and not(
           np.abs(ce.getSolutionAt("Q1C")-ce.getSolutionAt("Q6C")) > 0.5)):
            cost = 1000
            resultToFill.setCost(cost)
            return cost

        ''' optimizations '''
        #mag = ca.getGain("V3","voutPlus",180e9)
        res = ca.getTrans(0,1e-10,1e-13,["Q3C","Q1C"])#,"LOPlus","RFPlus","RFIN1"])

        # how to get a diff-Signal
        out = np.zeros((2,res[0].shape[1]),dtype = np.float64)
        integ = 0
        for i in range(res[0].shape[1]):
            out[0][i] = (res[0])[0][i]
            out[1][i] = ((res[0])[1][i] - (res[0])[2][i])**2
            if (out[0][i] > 0.4e-10):
                integ += out[1][i]

        max = np.amax(out[1][:])
        if(math.isnan(max)):
            max = -100
        print("Max: %G"%max)
        cost = -integ#-max
        resultToFill.setCost(cost)
        return cost

'''
setup and run optimization
'''

seq = o.CircuitSystemEquations(o.NetToComp('GilbertMixer/GilberMixerEasy.net').getComponents())
cf = CostFunction(list()) # no constraints defined

olist = [o.Optimizable(["R4","R5"],400,800),o.Optimizable(["R10","R12"],35000,50000),o.Optimizable(["R6","R8"],10000,30000)]
#olist = [o.Optimizable(["R17","R20"],100,1000),o.Optimizable(["R15","R18"],300,1500)]

opti = o.DownHillSimplexOptimizer(seq,olist,CostFunction(list()),10,o.SimpleResult(),None)

opti.run()

'''
result:
'''
ca = o.CircuitAnalyser(seq)
ca.plot_semilogx(ca.getACAnalysis_semilogx("V3",["Q1C"],9,12,10)[0])

ranking = opti.getResults()
for r in ranking:
    print (r.toString())

seq = o.CircuitSystemEquations(o.NetToComp('GilbertMixer/GilberMixerEasy.net').getComponents()) #TODO: BUG

for op in ranking[0].getOptimizables():
    val = op.getValue()
    for c in op.getOptimizableComponentNames():
        seq.setValueForCompName(val[0],c)

ca = o.CircuitAnalyser(seq)
#ca.plot_semilogx(ca.getACAnalysis_semilogx("V3",["Q1C"],9,12,10)[0])

res = ca.getTrans(0,1e-10,1e-13,["Q3C","Q1C","LOPlus","RFPlus","RFIN1"])

# how to get a diff-Signal
out = np.zeros((2,res[0].shape[1]),dtype = np.float64)
for i in range(res[0].shape[1]):
    out[0][i] = (res[0])[0][i]
    out[1][i] = (res[0])[1][i] - (res[0])[2][i]

ca.plot_lin([out,["diffout"],"transient"])

print("Max %G "%np.amax(out[1][:]))

ca.plot_lin(res)
