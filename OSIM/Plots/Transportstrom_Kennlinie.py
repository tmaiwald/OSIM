import numpy as np
import Simulation.Utils as u

vbic_is = 1  # TODO: !!
vbic_is_mm = 1  # TODO: !!!

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
Udlim = 1000

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

linearisieren = True

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

def _q1(UBE, UBC):
    qjbc = qj(UBC, PC, MC, FC ,AJC)
    qjbe = qj(UBE, PE, ME, FC, AJE)
    return 1 + qjbe / VER + qjbc / VEF


def _q2(Itf, Itr, IKR, IKF):
    return Itf / IKF + Itr / IKR

def _qb(B,C,E,Itf,Itr):  # TODO: gibt noch eine zweite Gleichung (siehe S. 99)

    if(linearisieren):
        if(C < 0):
            C = 0
            Itr = _ITR(B,C)


        if(E < 0):
            E = 0
            Itf = _ITF(B,E)


    q1 = _q1(B-E,B-C)
    q2 = _q2(Itf,Itr,IKR,IKF)

    return q1 / 2 * (1 + (1 + 4 * q2) ** NKF)


def _ITF(BI, EI):
        lim = 100
        if(linearisieren):
            if(BI < 1.6):
                lim = BI
            else:
                lim = 1.6

        return IS * (u.exp(BI - EI,1/(NF * UT),lim) - 1.0)

def _ITR(BI,CI):

        lim = 100
        if(linearisieren):
            if(BI < 1.6):
                lim = BI
            else:
                lim = 1.6

        return IS *ISSR * (u.exp(BI - CI,1/(NR * UT),lim) - 1.0)


def _IT(BI,CI,EI):

        #if(EI < 0 and CI < 0):

        #    r_itf = _ITF(BI, 0)
        #    r_itr = _ITR(BI, 0)

        #else:
            itf = _ITF(BI, EI)
            itr = _ITR(BI, CI)
            q_b =  _qb(BI,CI,EI,itf,itr)
            return (itf -itr)/q_b
