# Erstellt 12.01.2017 
#
# SingleComponent -> Netzliste : Name Startnode Endnode __Parameter
#
#
import abc

class Component(object):
    """Abstract description of a component in a circuit"""

    GMIN = 1e-9

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        self.COMPONENT_PRINT_WARNINGS = False
        self.superComponent = superComponent
        self.sys = None#CircuitSystemEquations([])
        self.pathParams = ""
        self.paramDict = dict()
        self.branches = list()
        self.nodes = nodes
        self.name = name
        self.value = complex(value)
        self.type = name[0]
        self.internalComponents = list()
        self.internalComponents.append(self)
        self.opValues = dict()
        self.bIdx = 0
        self.parseArgs(**kwargs)

        if not self.superComponent is None:
            self.updateSuperCompositeComponent()

    def assignToSystem(self, sys):
        self.sys = sys
        for c in self.internalComponents:
            c.sys = sys

    @abc.abstractmethod
    def setParameterValue(self,paramName,paramVal):
        print (self.name + ": Abstract Component: setParameterValue(...) not Implemented here")

    @abc.abstractmethod
    def setOPValues(self):
        self.opValues["value"] = self.value

    def printMyOPValues(self):
        print (self.name)
        print (self.opValues)

    @abc.abstractmethod
    def getValue(self):
        print (self.name + ": Abstract Component: getValue() not Implemented here")

    @abc.abstractmethod
    def setValue(self, value):
        print (self.name + ": Abstract Component: setValue() not Implemented here")

    def getNodes(self):
        return self.nodes

    def signIntoSysDictionary(self, compDict, sysIdx):
        sysIdx = self.registerNodes(compDict, sysIdx)
        sysIdx = self.registerBranches(compDict, sysIdx)
        return sysIdx

    def registerNodes(self, compDict, sysIdx):

        for c in self.internalComponents:
            for n in c.nodes:
                if (not compDict.has_key(n)):
                    if n is not '0':
                        compDict[n] = sysIdx
                        sysIdx += 1
        return sysIdx

    def registerBranches(self, compDict, sysIdx):
        for c in self.internalComponents:
            compDict[c.name] = sysIdx
            c.bIdx = sysIdx
            sysIdx += 1
        return sysIdx

    @abc.abstractmethod
    def doStep(self, freq_or_tau):
        """ abstract function to use in a iteration of simulations

        :param freq_or_tau: frequency or timestep value depending on simulation type
        :type freq_or_tau: float
        """
        print (self.name + ": Abstract Component: doStep() not Implemented here")

    def putA(self, A, node, myIdx, nm, mn):
        A[node, myIdx] = nm
        A[myIdx, node] = mn
        return self.sys.xprev[node]

    def putJ(self, J, m, node, mn):
        J[m, node] = mn
        return

    @abc.abstractmethod
    def getAdmittance(self, nodesFromTo, freq_or_tstep):
        print (self.name + ": Abstract Component: getAdmittance() not Implemented here")
        return 0

    def Udiff(self, twonodes):
        U1 = 0
        if twonodes[0] != '0':
            U1 = self.sys.x[self.sys.compDict.get(twonodes[0])]
        U2 = 0
        if twonodes[1] != '0':
            U2 = self.sys.x[self.sys.compDict.get(twonodes[1])]
        return U1 - U2

    def containsNonlinearity(self):
        return False  # Default, overwritten by Diode and Transistor and....

    def initialSignIntoSysEquations(self):
        for c in self.internalComponents:
            algebraicSign = 1  # Plus
            branchIdx = c.sys.compDict.get(c.name)
            for n in c.nodes:
                nodeIdx = c.sys.compDict.get(n)
                if n is not '0':
                    c.sys.A[nodeIdx, branchIdx] = algebraicSign * 1
                    c.sys.A[branchIdx, branchIdx] = -1
                    c.sys.A[branchIdx, nodeIdx] = algebraicSign * (c.getAdmittance(c.nodes, 0)+Component.GMIN)
                algebraicSign = algebraicSign * -1

    def insertAdmittanceintoSystem(self, freq):

        adm = self.getAdmittance(self.nodes, freq)+Component.GMIN
        x1v = 0
        x2v = 0
        if self.nodes[0] is not '0':
            x1v = self.putA(self.sys.A, self.sys.compDict.get(self.nodes[0]), self.bIdx, 1, adm)
        if self.nodes[1] is not '0':
            x2v = self.putA(self.sys.A, self.sys.compDict.get(self.nodes[1]), self.bIdx, -1, -adm)

        return [x1v, x2v]

    def readParams(self, filename):

        paramlist = open(filename, 'rb')
        paramDict = dict()

        for line in paramlist:
            d = line[0]
            if not d == '.' and not d == " " and not d == "\n":  # Comments start with '.'
                arr = line.split()
                key = arr[0]
                value = arr[1]
                #paramDict["".join((self.name, key))] = value
                paramDict[key] = value
        return paramDict

    def myBranchCurrent(self):
        return self.sys.x[self.bIdx]

    def getMyParameterFromDictionary(self, param, paramDict,default):
        return paramDict.get("".join((self.name, "-", param)),default)

    def updateSuperCompositeComponent(self):
        for c in self.internalComponents:
            self.superComponent.internalComponents.append(c)

    def voltageOverMe(self):
        return self.Udiff([self.nodes[0],self.nodes[1]])

    def parseArgs(self, **kwargs):
        for name, value in kwargs.items():
            if name == 'pParams':
                self.paramDict = self.readParams(value)
                self.pathParams = value
            if name == 'dict':
                self.paramDict = value

    def performCalculations(self):
        pass
