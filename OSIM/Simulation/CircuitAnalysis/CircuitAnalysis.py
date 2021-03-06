from __future__ import print_function
from copy import deepcopy
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as AA
from scipy.sparse import csr_matrix

from scipy.sparse.linalg import spsolve
import scipy as np
from mpl_toolkits.axes_grid1 import host_subplot
from numba import jit

UNIT_CURRENT  = 0
UNIT_VOLTAGE  = 1
UNIT_MAG_20DB = 2
UNIT_MAG_10DB = 3


DEBUG = False
PLOT = False

class CircuitAnalysis(object):

    MAX_NEWTON_ITERATIONS = 100

    def __init__(self, sysEquations):
        #print("TODO: bei doStep Uebergabeparameter abschaffen "+
        #      "- frequenz bzw zeit sollten in sys gespeichert werden")
        self.sys = deepcopy(sysEquations)
        self.Bauteile = self.sys.components
        self.doSubiterations = True
        self.vzero = np.zeros_like(self.sys.x)
        self.d_old = 10000

    @staticmethod
    def nonlin(sys):
        for b in sys.components:
            if b.containsNonlinearity():
                b.doStep(0)

    def show(self):
        self.sys.reset()

    @staticmethod
    @jit(nogil=True)
    def subNewtonRaphson(xvorher,sys,d_old,move_old,Vmax):
        '''
        ### Schrittweitenreduktion:
        ### f(x) = A*x+g-b= 0
        ##1) ist |f(x+1)| nicht kleiner als |f(x)| subiterationen durchfuehren bis
        ## Verfahren divergiert also wenn wenn es sich mit einer interation von der Nullstelle entfernt
        ## Abstand zu Nullstelle laesst sich mit Hilfe der euklidischen Distanz im n-dimensionalen Raum bestimmen
        '''

        fxp1 = sys.A.dot(sys.x)+sys.g-sys.b

        d = np.linalg.norm(fxp1)
        if(DEBUG):
            print("   1) d = %G"%(d))

        max_sub_i = 20
        x_work = np.copy(sys.x)
        move_vec = xvorher - sys.x
        move_len = np.linalg.norm(move_vec)
        subi = 0

        if(d < d_old):
            return move_len,d

        while(subi < max_sub_i):
            #print("SNR: %i" % (subi))
            fxp1 = sys.A.dot(x_work)+sys.g-sys.b
            d = np.linalg.norm(fxp1)
            max = np.amax(np.absolute(x_work))

            move_len = (np.linalg.norm(xvorher-x_work))

            if d < d_old:  #and move_len <= 2*move_old:#and max <= Vmax:
                sys.x = np.copy(x_work)
                if(DEBUG):
                    print("   Success after %i subiterations!!!"%(subi))
                    print("   subi: %i move_len: %G, move_old %G"%(subi,move_len, move_old))
                return move_len,d
            else:
                move_vec = 1.0/2.0*move_vec
                estx = xvorher+move_vec
                sys.x = estx
                CircuitAnalysis.nonlin(sys)

                #if sys.A.shape[0] > 300:
                    ##SparseMatrixCalculations
                if sys.n > 1000:
                    A = sys.A + sys.J
                    b = sys.J.dot(estx) - sys.g + sys.b
                    x_work = spsolve(A, b, permc_spec="NATURAL")
                else:
                    x_work = np.linalg.solve(sys.A + sys.J, np.dot(sys.J, estx) - sys.g + sys.b)

                subi += 1

        sys.x = xvorher-move_vec
        return move_old,d

    @staticmethod
    @jit(nogil=True)
    def newtonRaphson(sys):
        eps = 1e-9  # Abbruchkriterium
        relDif = np.amax(np.absolute(sys.b))*eps
        imax = CircuitAnalysis.MAX_NEWTON_ITERATIONS
        i = 0  # Iterationsnummer
        ungenau = True
        wenig_iterationen = True
        d = 10
        movelen = 10
        sys.curNewtonIteration = 0
        x_backup = np.copy(sys.x)

        Vmax = np.amax(np.absolute(sys.b))

        while (ungenau and wenig_iterationen):

            xvorher = sys.x
            i += 1
            sys.curNewtonIteration = i

            CircuitAnalysis.nonlin(sys)

            if(sys.n > 1000):
                A = sys.A + sys.J
                b = sys.J.dot(sys.x) - sys.g + sys.b
                sys.x = spsolve(A, b,permc_spec="NATURAL")
            else:
                sys.x = np.linalg.solve(sys.A + sys.J,np.dot(sys.J,sys.x)-sys.g+sys.b)

            movelen,d = CircuitAnalysis.subNewtonRaphson(xvorher,sys,d,movelen,Vmax)

            dif = np.amax(np.absolute(sys.x-xvorher))
            wenig_iterationen = (i < imax)
            ungenau =  d > relDif or (dif > relDif) #eps)# and (d > eps)

            #print("NR: %i"%(i))
            if( i > 50):
                print("Newton: Iteration: "+str(i)+"     ",end='\r')
            if i == imax:
                sys.x = np.copy(x_backup)
                print ("Newton-Raphson convergence failure")
                #raise NRConvergenceException()

        print("                                                              ", end='\r')
        return [sys.A,sys.x,sys.J,i]

    def plot(self, xArray, solutionndArray, obsNames):

        host = host_subplot(111, axes_class=AA.Axes)
        host.set_ylabel("Voltage")
        par = host.twinx()
        par.set_ylabel("Current")

        xmin = xArray[0]
        xmax = xArray[len(xArray) - 1]
        o = (xmax-xmin)*0.01
        host.set_xlim(xmin-o, xmax+o)

        ymax_cur = 0
        ymin_cur = 0
        ymax_vol = 0
        ymin_vol = 0

        for idx,o in enumerate(obsNames):
            ymax =  np.amax(solutionndArray[:,idx])
            ymin =  np.amin(solutionndArray[:,idx])
            if(self.sys.isVoltage(o)):
                if ymax > ymax_vol:
                    ymax_vol = ymax
                if ymin < ymin_vol:
                    ymin_vol = ymin
                p2, = host.plot(xArray, solutionndArray[:,idx] ,label=o+" [V]")
            else:
                if ymax > ymax_cur:
                    ymax_cur = ymax
                if ymin < ymin_cur:
                    ymin_cur = ymin
                p2, = par.plot(xArray, solutionndArray[:,idx], label=o+" [A]")

        offset_cur = (ymax_cur-ymin_cur)*0.1
        par.set_ylim(ymin_cur-offset_cur,ymax_cur+offset_cur)

        offset_vol = (ymax_vol-ymin_vol)*0.1
        host.set_ylim(ymin_vol-offset_vol,ymax_vol+offset_vol)
        host.legend()

        plt.draw()
        plt.show()

    @staticmethod
    def plotNewtonStats(movelens,its,functionValues,max_vals,max_names,difs,numOfIts):

        i = []
        for s in range(its.shape[0]):
            if not functionValues[s] == 0:
                i.append(int(its[s]))
        #print("movelens:")
        #print(movelens)
        plt.plot(i,np.split(movelens,[len(i),movelens.shape[0]-len(i)])[0])
        plt.title("movelens")
        plt.show()
        plt.plot(i,np.split(functionValues,[len(i),movelens.shape[0]-len(i)])[0])
        plt.title("funtion values")
        plt.show()
        plt.plot(i,np.split(max_vals,[len(i),movelens.shape[0]-len(i)])[0])
        plt.title("maxvals")
        plt.show()
        #print("names:")
        #print(max_names)
        #print("difs:")
        #print(difs)
        plt.plot(i,np.split(difs,[len(i),movelens.shape[0]-len(i)])[0])
        plt.title("difs")
        plt.show()

def debugNewton(sys,d,i,movelen):

    print("Distanz: %G"%(d))
    print("Schrittweite: %G"%(movelen))
    print("Iteratrion %i"%(i))
    a = np.argmax(np.absolute(sys.x))
    print("max Index %i"%(a))
    print("max Wert: "+str(sys.x[a]))
    for k in sys.compDict:
        if(sys.compDict[k] == a):
            print ("Name: %s"%(k))
            if(not sys.isVoltage(k)):
                c = sys.getCompByName(k)
                valfrom = sys.getSolutionAt(c.nodes[0])
                valto = sys.getSolutionAt(c.nodes[1])
                print("from: %s , to: %s"%(str(valfrom),str(valto)))

    #x = raw_input()
    #if(x == "y"):
    #    print(sys.compDict)
    #    print(sys.x)


