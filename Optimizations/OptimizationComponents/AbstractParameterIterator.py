
import abc

'''
z.B:
    variables: dict(list("R1","R2"):(0,200),list("C"):(0,200))
'''

class AbstractVariableIterator(object):

     INITIAL_ITERATION = -1

     def __init__(self,cirsys,optimizableList , **kwargs):
        self.finished = False
        '''
        self.args = kwargs

        #Idee fuer "intelligenten Iterator" :
        self.variables = dict()
        self.oldVariables = dict()
        self.oldCost = 0
        self.newCost = 0
        '''

     @abc.abstractmethod
     def getSysOfNextIteration(self, costLastIter):
         pass

     def isFinished(self):
         return self.finished

     @abc.abstractmethod
     def getProgressString(self):
         pass

     @abc.abstractmethod
     def getCurrentOptimizables(self):
         pass
