
import abc

class AbstractCostFunction(object):

      def __init__(self,constraintList,**kwargs):
          self.args = kwargs
          self.absCost = 0
          self.constraintList = constraintList

      @abc.abstractmethod
      def getCost(self,circuitSysEquations,resultToFill):
          print("you should check the constraints with sysEqu.checkConstraints and "
                "raise ConstraintFailureException if necessary")



