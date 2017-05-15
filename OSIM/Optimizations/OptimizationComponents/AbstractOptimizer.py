import time

from OSIM.Optimizations.ConstraintFailureException import ConstraintFailureException
from OSIM.Optimizations.OptimizationComponents.Resultholder import Resultholder


class AbstractOptimizer(object):

     UNKNOWN_NUMBER_OF_ITERATIONS = -1

     def __init__(self,CircuitSysEq,olist,costFunction ,numberOfResults,empytResult,Log):

         self.Log = Log
         self.emptyResult = empytResult
         self.cCalc = costFunction
         self.complete = False
         self.numberOfResults = numberOfResults
         self.numberOfIterations = AbstractOptimizer.UNKNOWN_NUMBER_OF_ITERATIONS
         self.resultHolder = Resultholder(numberOfResults)
         self.oldResult = empytResult
         self.sys = CircuitSysEq
         self.olist = olist

     '''
      hat explizit das Interface eines Threads -> zukuenftig als Thread lauffaehig
     '''
     def run(self):
        pass

     def getResults(self):
        pass





