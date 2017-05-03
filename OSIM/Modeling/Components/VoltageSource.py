import numpy as np

from OSIM.Modeling.AbstractComponents.SingleComponent import SingleComponent
from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations as ce


class VoltageSource(SingleComponent):

    TFUNC_NONE              = "NONE"
    TFUNC_SIN               = "SIN"
    TFUNC_PULSE             = "PULSE"
    TFUNC_RAND_BIT_PATTERN  = "RAND_BIT"

    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(VoltageSource, self).__init__(nodes, name, value, superComponent, **kwargs)
        '''
        Default values:
        '''
        self.parseArgs(**kwargs)

        self.t_func = self.paramDict.get("FUNC",VoltageSource.TFUNC_NONE)

        self.delay = eval(self.paramDict.get("D","0"))
        self.DCOffset = eval(self.paramDict.get("DC","0"))

        '''AC-Parameter'''
        self.sin_phase = eval(self.paramDict.get("P", "0"))
        self.sin_amplitude = eval(self.paramDict.get("AC", "0"))
        self.sin_damping_factor = eval(self.paramDict.get("DAMP", "0"))
        self.sin_freq = eval(self.paramDict.get("F", "0"))


        '''Pulse-Parameter'''
        self.p_period = eval(self.paramDict.get("TP","0"))
        self.p_trise = eval(self.paramDict.get("TR","0.001"))
        self.p_tfall = eval(self.paramDict.get("TF","0.001"))
        self.p_t_on = eval(self.paramDict.get("TON","0.001"))
        self.p_t_off = eval(self.paramDict.get("TOFF","0.001"))
        self.p_valOn = eval(self.paramDict.get("VON","0.001"))
        self.p_valOff = eval(self.paramDict.get("VOFF","0.001"))

        if(self.p_period == 0):
            self.p_period = self.p_trise+self.p_t_on+self.p_t_off+self.p_trise

    def setValue(self,volt):
        self.value = volt
        myIdx = np.int(self.sys.compDict.get(self.name))
        self.sys.b[myIdx] = volt

    def changeMyVoltageInSys(self, volt):
        self.setValue(volt)

    def doStep(self, freq_or_tau):

        if self.sys.atype == ce.ATYPE_TRAN:
            if self.t_func == VoltageSource.TFUNC_NONE:
                return
            if self.t_func == VoltageSource.TFUNC_SIN:

                if(not self.sin_phase == 0):
                    self.delay = 1/self.sin_freq * self.sin_phase / 360
                t = self.sys.tnow
                voltage = self.DCOffset + self.sin_amplitude * np.sin(2 * np.pi * self.sin_freq * (t - self.delay))\
                                        *np.exp(-(t - self.delay) * self.sin_damping_factor)
                self.changeMyVoltageInSys(voltage)

            if self.t_func == VoltageSource.TFUNC_PULSE:

                voltage = self.p_valOff
                t_norm= (self.sys.tnow-self.delay)/self.p_period
                t_phase = (t_norm-np.floor(t_norm))*self.p_period

                if t_phase < self.p_trise:    # rising edge
                    voltage = self.p_valOff+(self.p_valOn-self.p_valOff)*t_phase/self.p_trise
                    self.changeMyVoltageInSys(voltage)
                    return

                if t_phase <= self.p_trise + self.p_t_on:
                    self.changeMyVoltageInSys(self.p_valOn)
                    return

                if t_phase < self.p_trise + self.p_t_on + self.p_tfall:
                    voltage = self.p_valOn +(self.p_valOff-self.p_valOn)*(t_phase-self.p_trise-self.p_t_on)/self.p_tfall
                    self.changeMyVoltageInSys(voltage)
                    return
                self.changeMyVoltageInSys(voltage)
                return

            if self.t_func == VoltageSource.TFUNC_RAND_BIT_PATTERN:
                print ("Voltage Source - Warning: not implemented !!")
        if self.sys.atype in [ce.ATYPE_AC,ce.ATYPE_DC]:
            return

    def initialSignIntoSysEquations(self): #TODO use function from Component.py
        algebraicSign = 1# Plus
        branchIdx = self.sys.compDict.get(self.name)
        for n in self.nodes:
            nodeIdx    = self.sys.compDict.get(n)
            if n is not '0':
                self.sys.A[nodeIdx, branchIdx] = algebraicSign*1
                self.sys.A[branchIdx, nodeIdx] = algebraicSign
                self.sys.b[branchIdx] = self.value
            algebraicSign = algebraicSign*-1

    def getAdmittance(self, nodesFromTo, freq_or_tstep):
        return complex("inf")
