
# Schematic example:
#														=               _      _
#														A		   *	b   =  x
#
#                 ____
#      __1_______|  R |___2__					|	  			|	 | u1 |   | 0 |
#     _|_        |____|      |					|				|	 | u2 |	  | 0 |
#    | V |                   |        ----->    |				|  * |----| = |---|
#    |___|                 __|_					|				|	 |iV1 |   | V1|
#      |                   ____ C				|				|	 |iR1 |	  | 0 |
#      |                     |					|				|	 |iC1 |	  | 0 |
#     _|_ 0                __|__ 0
#
#

import numpy as np

class CircuitSystemEquations(object):
    """Class that contains the main data structures for a curcuit"""

    """
    Constants to define which simulation type is performed. The
     corresponding value has to be set before a simulation
    """
    ATYPE_NONE = 1
    ATYPE_DC   = 2
    ATYPE_AC   = 3
    ATYPE_TRAN = 4
    ATYPE_EST_DC = 5

    def __init__(self, components):

        self.curNewtonIteration = 0
        self.atype = CircuitSystemEquations.ATYPE_NONE
        self.components = components
        self.compDict = dict()
        sysIdx = 0
        ###mapping der Knoten-/Branch-namen auf Index im Gleichungssystem

        for c in components:
            c.assignToSystem(self)
            sysIdx = c.signIntoSysDictionary(self.compDict, sysIdx)

        self.n = len(self.compDict)#nnodes + nbranches  # Anzahl der Gleichunhen
        self.x = np.zeros((self.n, 1), dtype=np.complex128)
        self.g = np.zeros((self.n, 1), dtype=np.complex128)
        self.A = np.zeros((self.n, self.n), dtype=np.complex128)
        self.J = np.zeros((self.n, self.n), dtype=np.complex128)
        self.b = np.zeros((self.n, 1), dtype=np.complex128)
        self.xprev = np.zeros((self.n, 1), dtype=np.complex128)
        self.tnow = 0
        self.told = 0

        # - Knoten: die Summe alle Stroeme eines Knotens sind "0" - das
        #   bedeutet, dass in Zeilen die sich auf Nodes beziehen
        #   alle Spalten die sich auf einen jeweiligen Branch beziehen
        #   mit einer "(-)1" eingetragen werden -> Definition:
        #   Startknoten haben positive Vorzeichen, Endknoten negative
        # - Zeilen die sich auf Branches beziehen besteht aus der
        #   Admittanz die mit postivem Vorzeichen in der Spalte des
        #   Startknotens und mit negativem Vorzeichen am Endknoten
        #   . Des Weiteren wird in der Spalte des jeweiligen Branches
        #   eine '-1' eingetragen
        #

        for c in components:
            c.initialSignIntoSysEquations()

    def reset(self):
        """
        method to reset the equations
        """
        self.atype = self.ATYPE_NONE

        self.n = len(self.compDict)#nnodes + nbranches  # Anzahl der Gleichunhen
        self.x = np.zeros((self.n, 1), dtype=np.complex128)
        self.g = np.zeros((self.n, 1), dtype=np.complex128)
        self.A = np.zeros((self.n, self.n), dtype=np.complex128)
        self.J = np.zeros((self.n, self.n), dtype=np.complex128)
        self.b = np.zeros((self.n, 1), dtype=np.complex128)
        self.xprev = np.zeros((self.n, 1), dtype=np.complex128)

        for c in self.components:
            c.initialSignIntoSysEquations()

    def getSolutionAt(self, componentName):
        """method to get a value out of the solution vector x

        :param componentName: name of a component or a node in the netlist
        :type componentName: string
        :return: solution
        :rtype: complex
        """
        return self.x[self.compDict.get(componentName)]

    def setSolutionAt(self,name,val):
        self.x[self.compDict.get(name)] = val

    def getPreviousSolutionAt(self, componentName):
        return self.xprev[self.compDict.get(componentName)]

    def getCompByName(self, name):
        for b in self.components:
            if b.name == name:
                    return b
            for i in b.internalComponents:
                if i.name == name:
                    return i

    def isVoltage(self, name): #else: its a current
        for b in self.components:
            for c in b.internalComponents:
                if c.name == name:
                    return False
        return True

    def setParamterForComp(self,compname,paramname,paramval):
        comp = self.getCompByName(compname)
        comp.setParameterOrVariableValue(paramname, paramval)
        self.reset()

    def setParameterForCompsList(self,setables):
        """

        :param setables: list([compname,paramname,paramval],[...]) 
        """
        for s in setables:
            comp = self.getCompByName(s[0])
            comp.setParameterOrVariableValue(s[1], s[2])

        self.reset()



