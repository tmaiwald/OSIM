from OSIM.Optimizations import OptimizationAPI as o
from OSIM.Optimizations.OptimizationComponents.Optimizable import Optimizable as optis

class CostFunction(o.AbstractCostFunction):

     def getCost(self, ce , resultToFill):

        ca = o.CircuitAnalyser(ce)
        converged = ca.calcDCOperatingPoint()

        mag = ca.getGain("V2","OUT",1e9)
        cost = -mag #5*(1-np.absolute(ref)) + 10 * mag
        resultToFill.setCost(cost)

        return cost

'''
setup optimization
'''

seq = o.CircuitSystemEquations(o.NetToComp('AmplifierTB.net').getComponents())

olist = [o.Optimizable(["R3"],"R",600,1800),o.Optimizable(["R1"],"R",50000,80000)]#,o.Optimizable(["Q1"],"Nx",1,8)]
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


