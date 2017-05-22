'''
Wikipedia:

Das Downhill-Simplex-Verfahren findet ein lokales Optimum einer Funktion mit N Variablen (Parametern).
Gegeben ist eine Zielfunktion f:R^{N} -> R, die jedem Punkt im Loesungsraum einen Wert (Qualitaet der Loesung) zuordnet.

1) waehle N+1 Anfangspunkte x_{0},x_{1},.....,x_{N} Element {R} ^{N}}, die den Simplex bilden

2) sortiere die Punkte nach dem Wert der Zielfunktion  f, so dass x_{0} der beste, x_{N-1}
    der zweitschlechteste und x_{N} der schlechteste ist

3) bilde von allen ausser dem schlechtesten Punkt den Mittelpunkt m = 1/N *SUM(xi,0,N-1).

4) reflektiere den schlechtesten Punkt am Mittelpunkt: r = (1+alpha)*m - alpha*x_N

5) wenn r besser ist als x_{0}: bestimme den expandierten Punkt e = (1+ gamma)*m - gamma x_N, ersetze x_{N} durch
    den besseren der beiden Punkte  e, r und gehe zu Schritt 2

6) wenn r besser ist als der zweitschlechteste Punkt x_{N-1}: ersetze x_{N} durch  r und gehe zu Schritt 2

7) sei h der bessere der beiden Punkte x_N, r. Bestimme den kontrahierten Punkt c = beta*m + (1-beta)*h

8) wenn  c besser ist als x_{N}: ersetze x_{N} durch c und gehe zu Schritt 2

9) komprimiere den Simplex: fuer jedes  i in [1, N]: ersetze x_{i} durch sigma*x_{0}+(1-sigma )x_{i} gehe zu Schritt 2

 Typische Parameterwerte sind:
    alpha =1 (Reflexion)
    gamma = 2 (Expansion)
    beta = 1/2 (Kontraktion)
    sigma = 1/2 (Komprimierung)

'''

from OSIM.Optimizations.OptimizationComponents.AbstractOptimizer import AbstractOptimizer
from OSIM.Optimizations.DownHillSimplexOptimization.SimplexEdge import SimplexEdge
import numpy as np
from copy import deepcopy
import sys
import random as rand

class DownHillSimplexOptimizer(AbstractOptimizer):

     def __init__(self,CircuitSysEq,olist,costFunction ,numberOfResults,empytResult,Log):
        super(DownHillSimplexOptimizer, self).__init__(CircuitSysEq,olist,costFunction ,numberOfResults,empytResult,Log)

        self.eps = 0.01
        self.alpha = 1
        self.beta = 1/2
        self.gamma = 2
        self.sigma = 1/2
        self.edges = list()
        self.olist = olist
        self.m = np.zeros((len(olist),1),dtype=np.float)
        self.maxIter = 100
        self.emptyResult = empytResult
        self.costFunction = costFunction
        self.oldworstCost = 100
        self.CircuitSysEq = CircuitSysEq

     def run(self):
        print(len(self.edges))

        if(len(self.edges) == 0): #in case no edges are set yet
            #1) waehle N+1 Anfangspunkte x_{0},x_{1},.....,x_{N} Element {R} ^{N}}, die den Simplex bilden
            for i in range(len(self.olist)+1):
                e = SimplexEdge(self.costFunction,deepcopy(self.CircuitSysEq),self.olist,self.emptyResult,i)
                self.edges.append(e)
                self.printEdges()
                e.calcCost()

        #Quelle: http://www.mathematik.uni-wuerzburg.de/~kanzow/books/NelMead.pdf
        iteration = 0
        while((not self.isCompleted()) and iteration < self.maxIter):

            print("Iteration %i"%(iteration))

            iteration += 1
            #2) sortiere die Punkte nach dem Wert der Zielfunktion  f, so dass x_{0} der beste, x_{N-1}
            #   der zweitschlechteste und x_{N} der schlechteste ist
            self.edges = sorted(self.edges,cmp=lambda x,y:cmp(x.getCost(), y.getCost()))

            self.printEdges()

            #3) bilde von allen ausser dem schlechtesten Punkt den Mittelpunkt m = 1/N *SUM(xi,0,N-1).
            self.m = np.zeros((len(self.edges)-1,1),dtype=np.float64)
            for i in range(len(self.edges)-1):
                self.m +=self.edges[i].getEdgeValues()
            self.m = self.m/(len(self.edges)-1)

            #4) reflektiere den schlechtesten Punkt am Mittelpunkt: r = (1+alpha)*m - alpha*x_N
            r = self.edges[-1].getReflectedEdge(self.m,self.alpha)

            print("schlechtester Cost %G: "%(self.edges[-1].getCost()))
            print(self.edges[-1].x)

            print("reflektiert Cost %G: "%(r.getCost()))
            print(r.x)

            #5) unterscheide 3 Faelle

            #5a) f(x_0) < f(x_r) < f(x_N-1)
            if(r.getCost() > self.edges[0].getCost() and r.getCost() < self.edges[-2].getCost()):
                #ersetze x_N durch r
                self.edges[-1] = r
                continue

            #5b) f(x_r) < f(x_0)
            if(r.getCost() < self.edges[0].getCost()):
                #bestimme expandierte Ecke
                e = self.edges[-1].getExpandedEdge(self.m,self.gamma)
                if(e.getCost() < self.edges[0].getCost()):
                    self.edges[-1] = e
                else:
                    self.edges[-1] = r
                continue

            #5c) f(x_r) > f(x_N-1)
            if(r.getCost() > self.edges[-2].getCost()):

                if(self.edges[-1].getCost() < r.getCost()):
                    h = self.edges[-1]
                else:
                    h = r

                print(h.x)
                print(h.cost)
                c = h.getContractedEdge(self.m,self.beta)
                print(c.x)
                print(c.getCost())
                if(c.getCost() < self.edges[-1].getCost()):
                    self.edges[-1] = c
                else:
                    for i in range(1,len(self.edges)):
                        self.edges[i].compress(self.edges[0],self.sigma)
                continue

     def getResults(self):
        results = list()
        print("getResults:")
        print(len(self.edges))
        for e in self.edges:
           results.append(e.getResult())
        return results

     def isCompleted(self):
        # finish optimization if worst cost is 0.01% away from best
        worstCost = self.edges[-1].getCost()
        bestCost = self.edges[0].getCost()

        self.printEdges()

        print("isfinished ?: %G < %G"%(np.absolute(worstCost-bestCost)/np.absolute(bestCost),self.eps))

        if np.absolute(worstCost-bestCost)/np.absolute(bestCost) < self.eps and not self.oldworstCost == worstCost:
            print("True!")
            return True
        else:
            self.oldworstCost = worstCost
            return False

     def printEdges(self):
         for e in self.edges:
             print(e.toString())

     def setEdges(self,edges):
         if(len(edges) <  len(self.olist)+1):
             print("Error ! number of edges has to be len(self.olist)+1")
             sys.exit(1)
         for i in range(len(self.olist)+1):
                self.edges.append(edges[i])

     def setEdgesFromResultList(self,resultList):
         """ converts a sorted list of results to corresponding edges of the DownHillSimplex
         Algorithmn-> list has to be longer than number of optimizables+1 !!!

         :param resultList: list(results)
         :type resultList:
         """
         edges = []
         numofedges = len(resultList[0].getOptimizables())+1
         if(len(resultList) < numofedges):
             print("ERROR: more results are needed !")

         for i in range(numofedges):
             optis = resultList[i].getOptimizables()
             ## 5% Rauschen auf die Ecken, um zu vermeiden, dass Startwerte alle gleich sind
             for o in optis:
                 v = o.getValue()
                 o.setValue(rand.uniform(v-(0.05*v),v+(0.05*v)))

             e = SimplexEdge(self.costFunction,deepcopy(self.CircuitSysEq),optis,resultList[0].getNewInstance(),i)
             list_x = []

             for op in optis:
                 list_x.append(op.getValue())

             e.setEdgeValues(list_x)
             e.cost = resultList[i].getCost()
             edges.append(e)

         self.edges = edges













