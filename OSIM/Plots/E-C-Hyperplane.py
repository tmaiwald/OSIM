from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
import Transportstrom_Kennlinie as tp
import numpy as np

fig = plt.figure()
Ix = fig.gca(projection='3d')
dUC = fig.gca(projection='3d')
dUE = fig.gca(projection='3d')
dUB = fig.gca(projection='3d')

#Anzeigeparamter
raster = 0.01
BFIX = 0.9
CMIN = -1
CMAX = 1.2
EMIN = -1
EMAX = 1.2
diffh = 1e-10

# if b < BMAX und  C >CMIN
xE = np.arange(EMIN, EMAX, raster)
yC = np.arange(CMIN, CMAX, raster)
E, C = np.meshgrid(xE, yC)
I = np.zeros((len(yC),len(xE)))
dub = np.zeros((len(yC),len(xE)))
duc = np.zeros((len(yC),len(xE)))
due = np.zeros((len(yC),len(xE)))
dI = np.zeros(((len(yC),len(xE))))

for cidx, c in enumerate(yC):
    for eidx,e in enumerate(xE):
         current = tp._IT(BFIX, c, e)
         I[cidx][eidx] = current
         db_current = tp._IT(BFIX+diffh,c,e)
         dc_current = tp._IT(BFIX,c+diffh,e)
         de_current = tp._IT(BFIX,c,e+diffh)

         dub[cidx][eidx] = (db_current-current)/diffh  # = dI_T/dub
         duc[cidx][eidx] = (dc_current-current)/diffh   # = dI_T/duc
         due[cidx][eidx] = (de_current-current)/diffh


# ax.plot_surface(B, C, I, rstride=8, cstride=8, alpha=0.3)
Ix.plot_wireframe(E, C, I, rstride=15, cstride=3, alpha=0.3)
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
Ix.set_xlabel('EI')
Ix.set_xlim(EMIN, EMAX)
Ix.set_ylabel('CI')
Ix.set_ylim(CMIN,CMAX)
#Ix.set_ylabel('E')
#Ix.set_ylim(EMIN, EMAX)
Ix.set_zlabel('IT')
Ix.set_zlim(np.amin(I), np.amax(I))

plt.show()
