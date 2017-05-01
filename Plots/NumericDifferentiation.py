
import matplotlib.pyplot as plt
import numpy as np

IS = 1e-16
UT = 0.026
R = 100
def eh(v):
    return IS * np.exp(float(v/0.026)-1)

step = 1
x  = range(0, 100, 1)
f = [eh(v/100.0) for v in x]
df = [eh(v/100.0) for v in x]
dfn = [(eh(v/100.0+1.0/100.0)-eh(v/100.0))/step for v in x]
#fehler = [df[v]-dfn[v] for v in x]
fig = plt.figure(13)

ires =[float(v)/float(R) for v in x ]

plt.plot(x, f, 'b', label="Kennlinienfeld")
plt.plot(x, ires, 'b', label="Kennlinienfeld")
#plt.plot(x, df, 'b', label="Kennlinienfeld")
#plt.plot(x, dfn, 'r', label="Kennlinienfeld")
#plt.plot(x, fehler, 'r', label="Kennlinienfeld")
plt.show()
