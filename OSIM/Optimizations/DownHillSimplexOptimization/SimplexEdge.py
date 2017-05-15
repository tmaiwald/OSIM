import numpy as np
from copy import deepcopy
import random as rand

class SimplexEdge(object):

    def __init__(self,costFunction,sysEq,olist,resultTemplate,edgeNumber):

        self.edgeNumber = edgeNumber

        # index in Liste entspricht auch index in Werte
        self.olist = deepcopy(olist)
        self.x = np.zeros((len(olist),1),dtype=np.float64)
        self.g = np.zeros_like(self.x)
        self.costFunction = costFunction
        self.sys = sysEq
        self.cost = 100000
        self.curresult = resultTemplate.getNewInstance()
        '''
        gc = int(self.__getGrayCode(len(self.olist),self.edgeNumber),2)
        print(gc)
        '''
        # find initial EdgeValues, eg.random :
        for i in range(len(olist)):
            self.x[i] = rand.uniform(olist[i].getRangeBegin(),olist[i].getRangeEnd())#rand.randrange(olist[i].getRangeBegin(),olist[i].getRangeEnd())
            '''
            n = (gc >> i) & 1
            if(n == 0):
               self.x[i] = olist[i].getRangeBegin()
            if(n == 1):
               self.x[i] = olist[i].getRangeEnd()
            '''

        self.updateEdgeValues(self.x)

    def updateEdgeValues(self, x):
        self.x = np.copy(x)
        setableList = list()

        for vIdx in range(self.x.shape[0]):
            o = self.olist[vIdx]
            if(self.x[vIdx] < 0):
                self.x[vIdx] = 0.001
            o.setValue(self.x[vIdx][0])

        for o in self.olist:
            for n in o.getOptimizableComponentNames():
                """compname, paramname, paramval"""
                n = [n,o.getParamName(),o.getValue()]
                setableList.append(n)

        self.sys.setParameterForCompsList(setableList)
        print(setableList)

    def getEdgeValues(self):
        return self.x

    def getReflectedEdge(self,m,alpha):
        '''4) reflektiere den schlechtesten Punkt am Mittelpunkt:
        r = (1+alpha)*m - alpha*x_N'''
        r = m+alpha*(m-self.x)#(1+alpha)*m - alpha*self.x
        r_edge = SimplexEdge(self.costFunction,self.sys,self.olist,self.curresult,self.edgeNumber)
        r_edge.updateEdgeValues(r)
        r_edge.calcCost()
        return r_edge

    def getCost(self):
        return self.cost

    def calcCost(self):
        s = deepcopy(self.sys) #sys.reset() TODO !!
        self.cost = self.costFunction.getCost(s, self.curresult)

    def getResult(self):
        self.curresult.setOptimizables(self.olist)
        return self.curresult

    def getExpandedEdge(self,m,gamma):
        ''' bestimme den expandierten Punkt e = (1+ gamma)*m - gamma x_N,'''
        e = (1+gamma)*m - gamma*self.x
        e_edge = SimplexEdge(self.costFunction,self.sys,self.olist,self.curresult,self.edgeNumber)
        e_edge.updateEdgeValues(e)
        e_edge.calcCost()
        return e_edge

    def getContractedEdge(self,m,beta):
        c = m + beta*(self.x - m)
        c_edge = SimplexEdge(self.costFunction,self.sys,self.olist,self.curresult,self.edgeNumber)
        c_edge.updateEdgeValues(c)
        c_edge.calcCost()
        return c_edge

    def compress(self,bestEdge,sigma):
        '''komprimiere den Simplex: fuer jedes i in [1, N]: ersetze x_{i} durch sigma*x_{0}+(1-sigma )x_{i} ...'''
        self.updateEdgeValues(sigma * bestEdge.getEdgeValues() + (1 - sigma) * self.x)

    def toString(self):

        ret = ""
        ret+= "Edge Number "+str(self.edgeNumber)+"\n"
        ret += "Current Cost: "+str(self.cost)
        for o in self.olist:
            ret+= o.toString()

        return ret

    def __getGrayCode(self,numberOfVariables,index):
        #http://introcs.cs.princeton.edu/python/23recursion/graycode.py.html
        return self.__genCode(numberOfVariables)[index]

    def __genCode(self,n):

        if n == 0:
            return ['']

        code1 = self.__genCode(n-1)
        code2 = []
        for codeWord in code1:
            code2 = [codeWord] + code2

        for i in range(len(code1)):
            code1[i] += '0'
        for i in range(len(code2)):
            code2[i] += '1'
        return code1 + code2


    def setEdgeValues(self,list_x):

        for v in range(len(list_x)):
            self.x[v] = list_x[v]

        self.updateEdgeValues(self.x)
