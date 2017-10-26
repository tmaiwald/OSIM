import time
from copy import deepcopy
from OSIM.Optimizations.OptimizationComponents.AbstractParameterIterator import AbstractVariableIterator
from OSIM.Optimizations.BruteForceOptimization.Permutable import Permutable

class BruteForceParameterIterator(AbstractVariableIterator):

    def __init__(self,cirsys, olist , **kwargs):
        super(BruteForceParameterIterator, self).__init__(cirsys,olist,**kwargs)

        self.numberOfIterables = len(olist)
        self.currentIteration = int(0) # <--- erzeugt Bitmuster
        self.BITS_PER_ITERABLE = 1
        self.sys = cirsys
        self.startTime = time.time()
        self.olist = olist
        self.permutableList = list()

        self.numberOfBits = 0
        for idx, o in enumerate(olist):
            p = Permutable(o,self.numberOfBits)
            self.numberOfBits += p.getNumberOfBits()
            self.permutableList.append(p)

        self.numberOfIterations = 2**self.numberOfBits

        print("Brute-Force-Iteration with %i steps" % (self.numberOfIterations))

    def setSysOfNextIteration(self, sys):

        if(self.currentIteration == 0):
            self.startTime = time.time()

        if(not self.isFinished()):

            setableList = list()
            newCombination = False
            while(not newCombination):
                for p in self.permutableList:
                    newCombination,o = p.getCurOptimizable(self.currentIteration)
                    if(newCombination == False):
                        break
                    for n in o.getOptimizableComponentNames():
                        """compname, paramname, paramval"""
                        n = [n, o.getParamName(), o.getValue()]
                        setableList.append(n)
                    print(str(o.getOptimizableComponentNames()) + " " + str(o.getValue()))
                if (newCombination == True):
                    sys.setParameterForCompsList(setableList)

                self.currentIteration +=1

    def isFinished(self):

        if self.currentIteration >= self.numberOfIterations:
            return True

        return False

    def _getValueForListIdx(self,idx):

        # um idx*BITS_PER_ITERABLE nach rechts shiften
        # und den rest mit 0 maskieren ergibt ix in jeweiliger Liste

        i = self.currentIteration >> (idx*self.BITS_PER_ITERABLE)
        i &= 2**self.BITS_PER_ITERABLE-1

        plist = self.paramHolder[idx]
        return plist[i]

    def getProgressString(self):

         duration = time.time()-self.startTime
         percent = (float(self.currentIteration)/float(self.numberOfIterations))*100
         expAbsTime = (duration/percent) * 100
         rest = expAbsTime - duration

         str = ""
         if(expAbsTime < 300):
             str = ("Progress: %.1f %% \n" \
                   "Expected execution time: %.2f sec. \n"
                   "Expected remaining time: %.2f sec."%(percent,expAbsTime,rest))
         if(expAbsTime > 300 and expAbsTime <= 3600):
             str = ("Progress: %.1f %% \n" \
                   "Expected execution time: %.2f min. \n"
                   "Expected remaining time: %.2f min."%(percent,expAbsTime/60,rest/60))

         if(expAbsTime > 3600):
             str = ("Progress: %.1f %% \n" \
                   "Expected execution time: %.2f h. \n"
                   "Expected remaining time: %.2f h."%(percent,expAbsTime/60/60,rest/60/60))

         return str

    def getCurrentOptimizables(self):
        return self.olist



