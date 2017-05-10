import time

from OSIM.Optimizations.ConstraintFailureException import ConstraintFailureException
from OSIM.Optimizations.OptimizationComponents.Resultholder import Resultholder
from OSIM.Simulation.NRConvergenceException import NRConvergenceException
from OSIM.Optimizations.BruteForceOptimization.BruteForceParameterIterator import BruteForceParameterIterator
from copy import deepcopy

class BruteForceOptimizer(object):

     UNKNOWN_NUMBER_OF_ITERATIONS = -1

     def __init__(self,CircuitSysEq,olist,costFunction ,numberOfResults,empytResult,Log):

         self.Log = Log
         self.emptyResult = empytResult
         self.cCalc = costFunction
         self.complete = False
         self.numberOfResults = numberOfResults
         self.paramIter = BruteForceParameterIterator(deepcopy(CircuitSysEq),olist)
         self.numberOfIterations = BruteForceOptimizer.UNKNOWN_NUMBER_OF_ITERATIONS
         self.resultHolder = Resultholder(numberOfResults)
         self.oldResult =  empytResult

     '''
      hat explizit das Interface eines Threads -> zukuenftig als Thread lauffaehig
     '''
     def run(self):
         start = time.time()

         while(not self.complete):

            sys = self.paramIter.getSysOfNextIteration(self.oldResult.getCost())
            result = self.emptyResult.getNewInstance()
            try:
                print(self.cCalc.getCost(sys,result))
            except NRConvergenceException:
                if(not self.Log == None):
                    self.Log.error("Convergence Failure for...")
                print("Convergence problem at: ")
            except ConstraintFailureException:
                 if(not self.Log == None):
                    self.Log.error("Constraint missed for... ")
            else:
                result.setOptimizables(self.paramIter.getCurrentOptimizables())
                self.resultHolder.add(result)
                self.oldResult = result
                print("---------------------------------")
                print(self.paramIter.getProgressString())

            self.complete = self.paramIter.isFinished()

         print("----------->Optimization took: %G sec<----------------"%(time.time()-start))
         if(not self.Log == None):
            self.Log.notify("finished")

     def getResults(self):
         return self.resultHolder.getResults()





