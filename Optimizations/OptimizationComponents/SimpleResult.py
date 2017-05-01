from copy import deepcopy

class SimpleResult(object):

    def __init__(self):
        self.paramDict = dict()
        self.cost = 0
        self.optimizableList = []

    def setCost(self,cost):
        self.cost = cost

    def setParams(self,paramDict):
        self.paramDict = paramDict

    def setOptimizables(self,optis):
        self.optimizableList = deepcopy(optis)

    def getOptimizables(self):
        return self.optimizableList

    def getCost(self):
        return self.cost

    @staticmethod
    def getNewInstance():
        return SimpleResult()

    def toString(self):
        strng = ("cost: "+str(self.cost)+" for: \n")
        for o in self.optimizableList:
            strng = strng+o.toString()+"\n"
        return strng

