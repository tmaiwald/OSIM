import numpy as np

from Simulation.NRConvergenceException import NRConvergenceException

cimport numpy as np

def nonlin(sys):
    for b in sys.components:
        if b.containsNonlinearity():
            b.doStep(0)
    return [sys.J,sys.g,sys.b]


def newtonRaphson(sys):
     res = cyNewtonRaphson(sys,sys.A,sys.b,sys.g,sys.J,sys.x) 
     print("hier")
     sys.A = res[0]
     sys.J = res[1] 
     sys.x = res[2] 
     print(res[2])


def cyNewtonRaphson(sys,np.ndarray[np.complex_t, ndim=2] A,
    np.ndarray[np.complex_t, ndim=2] b,
    np.ndarray[np.complex_t, ndim=2] g,
    np.ndarray[np.complex_t, ndim=2] J,
    np.ndarray[np.complex_t, ndim=2] x):
    
    cdef np.ndarray[np.complex_t, ndim=2] xvorher = np.zeros([x.shape[0],x.shape[1]], dtype=np.complex)
    cdef float eps = 1e-6  # Abbruchkriterium
    cdef int imax = 100  # maximale Iterationszahl "sollte mit jeder Iteration eine Stelle nach dem Komma genauer werden[UEBERPRUEFE !]"
    cdef int i = 0  # Iterationsnummer
    cdef int ungenau = 1
    cdef int wenig_iterationen = 1

    while (ungenau == 1 and wenig_iterationen == 1):
        xvorher = x
        i += 1

        [J,g,b] = nonlin(sys)

        x = np.linalg.solve(A + J,np.dot(J,x)- g + b)
       
        '''
        #if(self.doSubiterations):
        #    self.subNewtonRaphson(xvorher)
        '''

        dif = np.amax(np.absolute(x-xvorher))
        if(i < imax):       
            wenig_iterationen = 1 
        else:
            wenig_iterationen = 0
        if(dif > eps): #and(d > eps)
            ungenau = 1
        else: 
            ungenau = 0
        if i == imax:
            print ("Newton-Raphson convergence failure")
            raise NRConvergenceException()

    return [A,J,x,b,g]
