

import os
import numpy as np

def exp(e, efak, Udlim):
    """Create a triangle with sides of lengths `a`, `b`, and `c`.

    Raises `ValueError` if the three length values provided cannot
    actually form a triangle.
    """

    if e > Udlim:
        max = np.exp(Udlim * efak)
        m = max*efak
        return max + m*(e-Udlim)
    else:
        return np.exp(e * efak)


def dexp(e, efak, Udlim):
    """Create a triangle with sides of lengths `a`, `b`, and `c`.

    Raises `ValueError` if the three length values provided cannot
    actually form a triangle.
    """

    if e > Udlim:
        return efak * np.exp(Udlim * efak)

    return efak * np.exp(e * efak)


def getDirectory():
    """Create a triangle with sides of lengths `a`, `b`, and `c`.

    Raises `ValueError` if the three length values provided cannot
    actually form a triangle.
    """
    return os.path.dirname(os.path.abspath(__file__))


def getTwoCombList(numberOfElements):

    idx = 0
    ret = None
    combNumber = np.fa
    while idx < combNumber:
        pass


    return []

def resToPGFPlotFile(res,filename):
   filenm = "".join([filename,".txt"])
   f = open(filenm, 'w')

   data = res[0]
   for i in range(data.shape[1]):
       f.write("(")
       for d in range(data.shape[0]-1):
           f.write(str(data[d][i]))
           f.write(",")

       f.write(str(data[data.shape[0]-1][i]))
       f.write(")\n")

   f.close()

