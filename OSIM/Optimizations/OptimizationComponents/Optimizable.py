
class Optimizable(object):

    def __init__(self,names_list,valfrom,valto):
        self.names = names_list
        self.vFrom = valfrom
        self.vTo = valto
        self.val = 0

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


