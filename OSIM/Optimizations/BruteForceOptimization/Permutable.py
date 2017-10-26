
class Permutable(object):

    UNKNOWN_IDX = -1
    MAX_NNUMBER_OF_BITS = 10

    def __init__(self,optimizable,startBitIdx):

        self.optimizable = optimizable
        self._bit_idx_from = startBitIdx
        self._bit_idx_to = Permutable.UNKNOWN_IDX

        minSteps = optimizable.minStep
        if(minSteps > 2**Permutable.MAX_NNUMBER_OF_BITS):
            print("ERROR in Permutable: minSteps > 2**MAX_NNUMBER_OF_BITS")

        self.numberOfBits = 2
        i = 0
        while(i < Permutable.MAX_NNUMBER_OF_BITS):
            if(minSteps/2**i <= 1):
                self.numberOfBits = i
                break
            i+=1

        _step = (optimizable.vTo - optimizable.vFrom) / 2 ** self.numberOfBits
        self._bit_idx_to = self._bit_idx_from+self.numberOfBits-1
        self.valueList = [float(optimizable.vFrom) + float(x * _step) for x in range(0, 2 ** self.numberOfBits)]
        print("startbit: %i , endbit %i , minsteps: %i , numberofBits %i"%(self._bit_idx_from,self._bit_idx_to,minSteps,self.numberOfBits))

    def getValue(self,intPermutation):
        idx = (intPermutation >> self._bit_idx_from) & ~(0xFFFFFFFF << self.numberOfBits)
        print(idx)
        print(self.valueList)
        v = self.valueList[idx]
        return v

    def getCurOptimizable(self,intPermutation):
        self.optimizable.setValue(self.getValue(intPermutation))
        return True,self.optimizable

    def getSetableListEntry(self,intPermutation):
        pass

    def getNumberOfBits(self):
        return self.numberOfBits