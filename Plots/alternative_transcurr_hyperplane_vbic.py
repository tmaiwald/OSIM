from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import Simulation.Utils as u

fig = plt.figure()
Ix = fig.gca(projection='3d')
dUC = fig.gca(projection='3d')
dUE = fig.gca(projection='3d')
dUB = fig.gca(projection='3d')

vbic_is = 1  # TODO: !!
vbic_is_mm = 1  # TODO: !!!

#Anzeigeparamter
raster = 0.001
BMIN = 0.7
BSHOWMIN = BMIN
BMAX = 0.85
BSHOWMAX = BMAX #1*1.2
CMIN = -0.1
CSHOWMIN = CMIN
CSHOWMAX = 0.3
OFFSET = 0  # 0.025
EMIN = -0.05
EMAX = 0.3
PRINT = False

Nx = 1
NF = 1.014
NR = nr = 1.01
IS = eval("3.1E-17 * (Nx * 0.25) ** 1.025 * vbic_is * (1 + (vbic_is_mm - 1) / np.sqrt(Nx))")

ISSR = 1  ## TODO: Paramter von VBIC 1.2
UT = 0.026
VEF = 193
VER = 5.3
IKF = 0.009 * (Nx * 0.25)
IKR = 0.01 * (Nx * 0.25)
NKF = 0.5
diffh = 1e-10

FC = 0.97
AJE = -0.5
AJC = -0.5
AJS = -0.5
PC = 0.62
PS = 0.42
PE = 0.9
ME = 0.105
MC = 0.12
VRT = 0 # TODO: Paramter von VBIC 1.2
ART = 0.1# TODO:  Paramter von VBIC 1.2
Udlim = 1.4

def qj(V, P, M, FC, A):
    qj = 0
    if A <= 0.0:
        '''
        //
        //SPICE regional depletion capacitance model
        //
        '''
        dvh = V - FC * P
        if dvh > 0.0:
            qlo = P * (1.0 - (1.0 - FC) ** (1.0 - M)) / (1.0 - M)
            qhi = dvh * (1.0 - FC + 0.5 * M * dvh / P) / ((1.0 - FC) ** (1.0 + M))
        else:
            qlo = P * (1.0 - (1.0 - V / P) ** (1.0 - M)) / (1.0 - M)
            qhi = 0.0
        qj = qlo + qhi

    else:
        '''
        //
        //		Single piece depletion capacitance model
        //
        //		Based on c=1/(1-V/P)^M, with sqrt limiting to make it
        //		C-inf continuous (and computationally efficient), with
        //		added terms to make it monotonically increasing (which
        //		is physically incorrect, but avoids numerical problems
        //		and kinks near where the depletion and diffusion
        //		capacitances are of similar magnitude), and with appropriate
        //		offsets added to that qj(V=0)=0.
        //
        '''
        dv0 = - P * FC
        mv0 = np.sqrt(dv0 * dv0 + A)
        vl0 = 0.5 * (dv0 - mv0) + P * FC
        q0 = - P * (1.0 - vl0 / P) ** (1.0 - M) / (1.0 - M)
        dv = V - P * FC
        mv = np.sqrt(dv * dv + A)
        vl = 0.5 * (dv - mv) + P * FC
        qlo = - P * (1.0 - vl / P) ** (1.0 - M) / (1.0 - M)
        qj = qlo + (1.0 - FC) ** (- M) * (V - vl + vl0) - q0

    return qj

def q1(UBE, UBC):
    qjbc = qj(UBC, PC, MC, FC ,AJC) #TODO ei
    qjbe = qj(UBE, PE, ME, FC, AJE)
    return 1 + qjbe / VER + qjbc / VEF


def q2(Itf, Itr, IKR, IKF):
    return Itf / IKF + Itr / IKR

def qb(q1, q2, NKF):  # TODO: gibt noch eine zweite Gleichung (siehe S. 99)
    return q1 / 2 * (1 + (1 + 4 * q2) ** NKF)


def _ITF(BI, EI, CI):
     if ((BI - EI) > 0) and ((BI - CI) > 0):
        if(CI-EI < 0):
            a = IS/(NR*UT) * (u.exp(-EI,1/(NR*UT),Udlim)*BI)
            b = IS * (u.exp((BI - EI),1 /(NF * UT),Udlim) - 1.0)
            return a+b

     #print("BI: "+str(BI)+" CI: "+str(CI)+" EI: "+str(EI))
     #print("hier1 "+str(self.sys.curNewtonIteration))
     return IS * (u.exp((BI - EI),1 /(NF * UT),Udlim) - 1.0)

def _ITR( BI, EI, CI):

    if ((BI - EI) > 0) and ((BI - CI) > 0):
        if(CI-EI < 0):
            start =  IS * (u.exp((BI - 0),1 /(NR * UT),Udlim) - 1.0)
            m = IS/(NR*UT) * (u.exp(-EI,1/(NR*UT),Udlim)
                *BI - u.exp(BI,1/(NR*UT),Udlim))
            return start + m*CI
        if(CI-EI > 0):
            pass
    #print("BI: "+str(BI)+" CI: "+str(CI)+" EI: "+str(EI))
    #print("hier2 "+str(self.sys.curNewtonIteration))
    return IS * (u.exp((BI - CI),1 /(NR * UT),Udlim) - 1.0)

def _ITF_r(B,E):
    return IS * (u.exp((B - E),1 /(NF * UT),Udlim) - 1.0)

def _ITR_r(B,E):
    return IS * (u.exp((B - E),1 /(NR * UT),Udlim) - 1.0)

def tI_T(B,C,E):

    q_1 = q1(B-E,B-C)
    Itr = _ITR(B,E,C)
    Itf = _ITF(B,E,C)
    q_2 = q2(Itf,Itr,IKR,IKF)
    q_b = qb(q_1,q_2,NKF)

    n = 0

    if ((B > E) and ( B > C)):
            if(C < E):
                q1_r = q1(B-E, B-E)
                q2_r = q2(_ITF_r(B,E),_ITR_r(B,E),IKR,IKF)
                q_b = qb(q1_r,q2_r,NKF)
                n = 1
            if(C > E):
                n = 2
    if(PRINT):
        if(n == 0):
            print("nicht uebersteuert")
        if(n == 1):
            print("normal uebersteurt: B:%G, C:%G, E:%G"%(B,C,E))
        if(n == 2):
            print("invers uebersteuert: B:%G, C:%G, E:%G"%(B,C,E))

    return (Itf-Itr)/q_b


# if b < BMAX und  C >CMIN
xB = np.arange(BSHOWMIN, BMAX, raster)
yC = np.arange(CMIN, CSHOWMAX, raster)
B, C = np.meshgrid(xB, yC)
I = np.zeros((len(yC),len(xB)))
dub = np.zeros((len(yC),len(xB)))
duc = np.zeros((len(yC),len(xB)))
due = np.zeros((len(yC),len(xB)))
dI = np.zeros(((len(yC),len(xB))))
for cidx, c in enumerate(yC):
    for bidx,b in enumerate(xB):
         current = tI_T(b, c, 0)
         I[cidx][bidx] = current
         db_current = tI_T(b+diffh,c,0)
         dc_current = tI_T(b,c+diffh,0)
         de_current = tI_T(b,c,0+diffh)

         dub[cidx][bidx] = (db_current-current)/diffh  # = dI_T/dub
         duc[cidx][bidx] = (dc_current-current)/diffh   # = dI_T/duc
         due[cidx][bidx] = (de_current-current)/diffh


# ax.plot_surface(B, C, I, rstride=8, cstride=8, alpha=0.3)
Ix.plot_wireframe(B, C, I, rstride=15, cstride=3, alpha=0.3)
#b = dUB.plot_wireframe(B,C,dub,rstride=15, cstride=3, alpha=0.3)
#c = dUC.plot_wireframe(B,C,duc,rstride=15, cstride=3, alpha=0.3)
#e = dUE.plot_wireframe(B,C,due,rstride=15, cstride=3, alpha=0.3)
#ax.plot_wireframe(B, C, dI, rstride=15, cstride=3, alpha=0.3)

#cset = ax.contour(B, C, I, zdir='x', offset=BMAX, cmap=cm.coolwarm)
#cset = ax.contour(bB, bC, bI, zdir='y', offset=0.3, cmap=cm.coolwarm)
#cset = ax.contour(B, C, I, zdir='y', offset=1, cmap=cm.coolwarm)
'''
dUC.set_xlabel('B')
dUC.set_ylabel('C')
dUC.set_zlabel('duc')


dUB.set_xlabel('B')
dUB.set_ylabel('C')
dUB.set_zlabel('dub')

dUE.set_xlabel('B')
dUE.set_ylabel('C')
dUE.set_zlabel('due')
'''
Ix.set_xlabel('B')
Ix.set_xlim(BSHOWMIN, BSHOWMAX)
Ix.set_ylabel('C')
Ix.set_ylim(CMIN,CSHOWMAX)
#Ix.set_ylabel('E')
#Ix.set_ylim(EMIN, EMAX)
Ix.set_zlabel('I')
Ix.set_zlim(np.amin(I), np.amax(I))

plt.show()
