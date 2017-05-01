from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

fig = plt.figure()
ax = fig.gca(projection='3d')

BMAX = 0.9
CMIN = 0.0
IS = 7*10**-15
UT = 0.026
OFFSET =0# 0.025

# if b < BMAX und  C >CMIN
B = np.arange(0.8, BMAX+OFFSET, 0.0005)
C = np.arange(CMIN-OFFSET, 0.3, 0.0005)
B, C = np.meshgrid(B, C)
I = IS*(np.exp((B)/UT)-np.exp((B-C)/UT))

# if b > BMAX und  C >CMIN
bB = np.arange(BMAX,1,0.0005)
bC = np.arange(CMIN,0.3,0.0025)
bB, bC = np.meshgrid(bB, bC)
i = IS*(np.exp((BMAX)/UT)-np.exp((BMAX-bC)/UT)) 
bI = i + i/UT* (bB-BMAX)

# if b < BMAX und  C  < CMIN
cB = np.arange(0.8,BMAX,0.0005)
cC = np.arange(-0.1,CMIN,0.0025)
cB, cC = np.meshgrid(cB, cC)
cI = IS*(np.exp(cB/UT)-np.exp((cB-CMIN)/UT)) + IS/UT*np.exp((cB-CMIN)/UT) * (cC-CMIN)

# if b > BMAX und C < CMIN
nB = np.arange(BMAX,1.0,0.0005)
nC = np.arange(-0.1,CMIN,0.0025)
nB, nC = np.meshgrid(nB, nC)
start = IS*(np.exp((BMAX)/UT)-np.exp((BMAX-CMIN)/UT)) + IS/UT*(np.exp(BMAX/UT)-np.exp((BMAX-CMIN)/UT)) * (nB-BMAX)
nI = start + IS/UT*np.exp((BMAX-CMIN)/UT) * (nC-CMIN)


#ax.plot_surface(B, C, I, rstride=8, cstride=8, alpha=0.3)
ax.plot_wireframe(B, C, I, rstride=15, cstride=3, alpha=0.1)
ax.plot_wireframe(bB,bC,bI, rstride=5, cstride=5, alpha=0.4)
ax.plot_wireframe(cB,cC,cI, rstride=5, cstride=5, alpha=0.4)
ax.plot_wireframe(nB,nC,nI, rstride=5, cstride=5, alpha=0.4)

cset = ax.contour(B, C, I, zdir='y', offset=0.3, cmap=cm.coolwarm)
cset = ax.contour(bB, bC, bI, zdir='y', offset=0.3, cmap=cm.coolwarm)
cset = ax.contour(B, C, I, zdir='y', offset=1, cmap=cm.coolwarm)

ax.set_xlabel('B')
ax.set_xlim(0.8, 1)
ax.set_ylabel('C')
ax.set_ylim(-0.1, 0.3)
ax.set_zlabel('I')
ax.set_zlim(-30, 40)

plt.show()
