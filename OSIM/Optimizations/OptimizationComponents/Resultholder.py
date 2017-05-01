class Resultholder(object):

    def __init__(self,numberOfResults):
        self.numberOfResults = numberOfResults
        self.results = list()

    def add(self,result):
        self.results.append(result)
        self._sortResults()
        if(len(self.results) > self.numberOfResults):
            del self.results[-1]

    def getResults(self):
        return self.results

    def _sortResults(self):
        self.results = sorted(self.results,cmp=lambda x,y:cmp(x.getCost(), y.getCost()))

    def _getKey(self,result):
        return result.getCost()
