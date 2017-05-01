from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

fig = plt.figure()
ax = fig.gca(projection='3d')

vbic_is = 1  # TODO: !!
vbic_is_mm = 1  # TODO: !!!

#Anzeigeparamter
raster = 0.001
BMIN = 0.7
BSHOWMIN = BMIN
BMAX = 1
BSHOWMAX = 1.05 #1*1.2
CMIN = -0.03
CSHOWMIN = -0.12
CSHOWMAX = 0.4
OFFSET = 0  # 0.025

Nx = 2
NF = 1.014
NR = nr = 1.01
IS = eval("3.1E-17 * (Nx * 0.25) ** 1.025 * vbic_is * (1 + (vbic_is_mm - 1) / np.sqrt(Nx))")

ISSR = 1  ## TODO: Paramter von VBIC 1.2
UT = 0.026
VEF = 189
VER = 5.3
IKF = 0.009 * (Nx * 0.25)
IKR = 0.01 * (Nx * 0.25)
NKF = 0.5
diffh = 0.000001

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
E = 0 # Bezugsspannung am Emitter


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

def I_T(B,C,E):
    q_1 = q1(B-E,B-C)
    Itf = IS * (np.exp((B-E)/(NF*UT)) - 1.0)
    Itr = IS * (np.exp((B-C)/(NR*UT)) - 1.0)
    q_2 = q2(Itf,Itr,IKR,IKF)
    q_b = qb(q_1,q_2,NKF)
    return (Itf-Itr)/q_b

# if b < BMAX und  C >CMIN
xB = np.arange(BSHOWMIN, BMAX, raster)
yC = np.arange(CMIN, CSHOWMAX, raster)
B, C = np.meshgrid(xB, yC)
I = np.zeros((len(yC),len(xB)))
for cidx, c in enumerate(yC):
    for bidx,b in enumerate(xB):
        I[cidx][bidx] = I_T(b,c,E)

# if b > BMAX und  C >CMIN
bb = np.arange(BMAX, BSHOWMAX, raster)
bc = np.arange(CMIN, CSHOWMAX, raster)
bB, bC = np.meshgrid(bb, bc)
bI = np.zeros((len(bc),len(bb)))
for cidx, c in enumerate(bc):
    mr = (I_T(BMAX+diffh,c,E)-I_T(BMAX,c,E))/diffh
    ir = I_T(BMAX,c,E)
    for bidx,b in enumerate(bb):
        bI[cidx][bidx] = ir+mr*(b-BMAX)

#i = IS * (np.exp((BMAX) / UT) - np.exp((BMAX - bC) / UT))
#bI = i + i / UT * (bB - BMAX)

# if b < BMAX und  C  < CMIN
cb = np.arange(BSHOWMIN, BMAX, raster)
cc = np.arange(CSHOWMIN, CMIN, raster)
cB, cC = np.meshgrid(cb, cc)
cI = np.zeros((len(cc),len(cb)))
for bidx,b in enumerate(cb):
    mr = (I_T(b,CMIN,E)-I_T(b,CMIN-diffh,E))/diffh
    ir = I_T(b,CMIN,E)
    for cidx, c in enumerate(cc):
        cI[cidx][bidx] = ir+mr*(c-CMIN)

# if b > BMAX und C < CMIN
eb = np.arange(BMAX, BSHOWMAX ,raster)
ec = np.arange(CSHOWMIN, CMIN , raster)
eB, eC = np.meshgrid(eb, ec)
eI = np.zeros((len(ec),len(eb)))
mc = (I_T(BMAX,CMIN,E)-I_T(BMAX,CMIN-diffh, E))/diffh
mb = (I_T(BMAX+diffh,CMIN,E)-I_T(BMAX,CMIN, E))/diffh

for bidx,b in enumerate(eb):
    start = I_T(BMAX,CMIN,E) +  mb*(b-BMAX)
    for cidx, c in enumerate(ec):
       eI[cidx][bidx] = start  + mc*(c-CMIN)

# ax.plot_surface(B, C, I, rstride=8, cstride=8, alpha=0.3)
ax.plot_wireframe(B, C, I, rstride=15, cstride=3, alpha=0.3)
ax.plot_wireframe(bB, bC, bI, rstride=5, cstride=5, alpha=0.3)
ax.plot_wireframe(cB, cC, cI, rstride=5, cstride=5, alpha=0.3)
ax.plot_wireframe(eB, eC, eI, rstride=5, cstride=5, alpha=0.4)

#cset = ax.contour(B, C, I, zdir='x', offset=BMAX, cmap=cm.coolwarm)
#cset = ax.contour(bB, bC, bI, zdir='y', offset=0.3, cmap=cm.coolwarm)
#cset = ax.contour(B, C, I, zdir='y', offset=1, cmap=cm.coolwarm)

ax.set_xlabel('B')
ax.set_xlim(BSHOWMIN, BSHOWMAX)
ax.set_ylabel('C')
ax.set_ylim(CSHOWMIN, CSHOWMAX)
ax.set_zlabel('I')
ax.set_zlim(np.amin(eI), np.amax(bI))

plt.show()
