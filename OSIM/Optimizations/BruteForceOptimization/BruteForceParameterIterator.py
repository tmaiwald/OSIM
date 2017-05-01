import time
from copy import deepcopy
from Optimizations.OptimizationComponents.AbstractParameterIterator import AbstractVariableIterator


class BruteForceParameterIterator(AbstractVariableIterator):

    def __init__(self,cirsys, olist , **kwargs):
        super(BruteForceParameterIterator, self).__init__(cirsys,olist,**kwargs)
        self.numberOfIterables = len(olist)
        self.currentIteration = int(0) # <--- erzeugt Bitmuster
        self.BITS_PER_ITERABLE = 1
        self.sys = deepcopy(cirsys)
        self.startTime = time.time()
        self.olist = olist

        if self.numberOfIterables > 6:
            print("ERROR: NOT IMPLEMENTED!!!")

        self.numberOfIterations = 2**(self.BITS_PER_ITERABLE*self.numberOfIterables)
        print("Brute-Force-Iteration with %i steps"%(self.numberOfIterations))

        '''
            Note: pro key spendieren wir n Bit (entspricht 2^n -1 Werten) in einem Integer
            diese n Bit kodieren den jeweiligen Index in einem Array in dem
            die Werte abgelegt sind, die das(bzw. die) ensprechende Bauelement
            annehemen kann.
            Das Integer wird von rechts aufgefuellt.
            Das heisst das erste Element im dictionay bekommt die 5 Least-Significant
            Bits im Integer

            Step0: - Liste erzeugen die alle Listen der moeglichen Bauteilparameter enthaelt
                   - Dictionary erzeugen, das hilft von Integer-Bit-Ausschnitt auf Bauteil und Liste
                     in Liste zu mappen -> Bauteile:Listen-Listen-Idx
                     z.B: {("R1","R2"):0}
        '''
        self.paramHolder = list()
        self.param_idx_dict = dict()
        '''
            Step1: Ereugen der Listen mit den Werten, in die Liste fuer die Listen eintragen sowie
            den zugehoerigen index in das dictionay eintragen
        '''
        for idx, o in enumerate(olist):
            _step = (o.vTo-o.vFrom)/2**self.BITS_PER_ITERABLE
            l = [o.vFrom+x*_step for x in range(0,2**self.BITS_PER_ITERABLE)]
            self.paramHolder.append(l)
            self.param_idx_dict[o] = idx

    def getSysOfNextIteration(self, costLastIter):

        retsys = deepcopy(self.sys)

        if(self.currentIteration == 0):
            self.startTime = time.time()

        if(not self.isFinished()):

            for o in self.param_idx_dict:
                listIdx = self.param_idx_dict[o]
                paraVal = self._getValueForListIdx(listIdx)
                o.setValue(paraVal)
                for b in o.names:
                   print(b+": %G"%(paraVal))
                   retsys.getCompByName(b).setValue(complex(paraVal))
                   #succ = csys.setValueForCompName(paraVal,b)

            self.currentIteration +=1

        return retsys

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
                   "Expexted execution time: %.2f sec. \n"
                   "Expected rest time: %.2f sec."%(percent,expAbsTime,rest))
         if(expAbsTime > 300 and expAbsTime <= 3600):
             str = ("Progress: %.1f %% \n" \
                   "Expexted execution time: %.2f min. \n"
                   "Expected rest time: %.2f min."%(percent,expAbsTime/60,rest/60))

         if(expAbsTime > 3600):
             str = ("Progress: %.1f %% \n" \
                   "Expexted execution time: %.2f h. \n"
                   "Expected rest time: %.2f h."%(percent,expAbsTime/60/60,rest/60/60))

         return str

    def getCurrentOptimizables(self):
        return self.olist



