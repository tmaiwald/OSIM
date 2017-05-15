
class Optimizable(object):

    def __init__(self,comp_names_list,paramname,valfrom,valto,**kwargs):
        self.names = comp_names_list
        self.paramname = paramname
        self.minStep = 2 #default
        self.vFrom = valfrom
        self.vTo = valto
        self.val = 0

        for name, value in kwargs.items():
            if name == 'minSteps':
               self.minStep = value

    def setValue(self, v):
        self.val = v

    def getRangeBegin(self):
        return self.vFrom

    def getRangeEnd(self):
        return self.vTo

    def getValue(self):
        return self.val

    def getOptimizableComponentNames(self):
        return self.names

    def toString(self):
        stri = ""
        for n in self.names:
            stri = stri+" "+n

        return (stri+" at %s"%(str(self.val)))

    def getParamName(self):
        return self.paramname

    @staticmethod
    def getSetableList(olist):
        setableList = list()

        for o in olist:
            for n in o.getOptimizableComponentNames():
                """compname, paramname, paramval"""
                n = [n, o.getParamName(), o.getValue()]
                setableList.append(n)

        return setableList
