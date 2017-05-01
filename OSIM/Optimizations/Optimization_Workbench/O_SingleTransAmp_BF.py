from Optimizations import OptimizationAPI as o

class CostFunction(o.AbstractCostFunction):

     def getCost(self, ce , resultToFill):

        ca = o.CircuitAnalyser(ce)
        converged = ca.calcDCOperatingPoint()

        if(not converged):
            raise o.NRConvergenceException
        if(not ce.checkConstraints(self.constraintList)):
            raise o.ConstraintFailureException

        mag = ca.getGain("V2","OUT",1e9)
        cost = -mag #5*(1-np.absolute(ref)) + 10 * mag
        resultToFill.setCost(cost)

'''
setup optimization
'''

seq = o.CircuitSystemEquations(o.NetToComp('SingleTransAmplifier/AmplifierTB.net').getComponents())

olist = [o.Optimizable(["R3"],600,1800),o.Optimizable(["R1"],50000,80000)]
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

seq = o.CircuitSystemEquations(o.NetToComp('SingleTransAmplifier/AmplifierTB.net').getComponents()) #TODO: BUG

for op in ranking[0].getOptimizables():
    val = op.getValue()
    for c in op.getOptimizableComponentNames():
        seq.setValueForCompName(val,c)

ca = o.CircuitAnalyser(seq)
ca.plot_semilogx(ca.getACAnalysis_semilogx("V2",["OUT"],6,12,100)[0])
