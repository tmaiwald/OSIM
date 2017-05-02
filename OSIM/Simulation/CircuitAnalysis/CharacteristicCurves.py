import matplotlib.pyplot as plt
import numpy as np

from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations
from OSIM.Simulation.NRConvergenceException  import NRConvergenceException


def createCharacteristicCurves(self, voltageSourceCE, fromvalce, tovalce, stepvoltce, voltageSourceBE, fromvalbe,
                               tovalbe, stepvoltbe, listOfObservables):

    self.sys.atype = CircuitSystemEquations.ATYPE_DC

    vbes = [x * stepvoltbe for x in range(int(fromvalbe / stepvoltbe), int(tovalbe / stepvoltbe), 1)]
    vces = [x * stepvoltce for x in range(int(fromvalce / stepvoltce), int(tovalce / stepvoltce), 1)]

    observedResults = list()
    for c in range(0, len(listOfObservables)):
        observedResults.append(
            np.zeros((len(vbes), len(vces)), dtype=np.complex128))  # Loesungsverktor fuer alle Frequenzen

    for vb in vbes:
        for b in self.Bauteile:
            for c in b.internalComponents:
                if c.name == voltageSourceBE:
                    c.changeMyVoltageInSys(vb)
        for vc in vces:
            for b in self.Bauteile:
                for c in b.internalComponents:
                    if c.name == voltageSourceCE:
                        c.changeMyVoltageInSys(vc)
            try:
                self.newtonRaphson()
            except NRConvergenceException:
                print("Convergence problem at: ")
                print("VBE: %G"%(vb))
                print("VCE: %G"%(vc))
            for i in range(0, len(listOfObservables)):
                (observedResults[i])[vbes.index(vb)][vces.index(vc)] = self.sys.getSolutionAt(listOfObservables[i])[0]

    f = plt.figure(13)
    for be in vbes:
        plt.plot(vces, ((observedResults[0])[vbes.index(be)]).real, 'b', label="Kennlinienfeld")
        f.show()

    plt.show()
