# Erstellt 12.01.2017
#
# NPN Transistor -> Netzliste : Name Basis Emitter Collector __Parameter
#
'''
from http://www.designers-guide.org/VBIC/release1.1.5/vbic1.1.5_pseudoCode.html
// -----------------------------------------------------------------------------
// |                                                                           |
// | BE/BC extrinsic         o s                                   o c         |
// | overlap capacitances    |                                     |           |
// | not shown               |                                     |           |
// |                        (v) Irs                               (v) Ircx     |
// |                         |                                     |           |
// |                         |                                     |           |
// |                ---------o---- si                              |           |
// |                |        |   |                                 |           |
// |                |      + |   |                                 |           |
// |                |   Qbcp =  (v) Ibcp                           |           |
// |                |      - |   |                                 |           |
// |                |        |   |                                 |           |
// |          Iccp (^)    bp o---+----(<-)----+--------------------o cx        |
// |                |        |   |    Irbp    |                    |           |
// |                |      - |   |            |                    |           |
// |                |   Qbep =  (^) Ibep      |                   (v) Irci     |
// |                |      + |   |            |                    |           |
// |                |        |   |            |                    |           |
// |                ---------+----            |       ----+--------o ci        |
// |                         |                |       |   |        |           |
// |                         |              - |       |   | -      |           |
// |                         |           Qbcx =  Ibc (^)  = Qbc    |           |
// |                         |              + | -Igc  |   | +      |           |
// |                       bx|                |       |   |        |           |
// |          b o----(->)----o---+----(->)----+-------+---o bi    (v) Itzf|Itxf|
// |                 Irbx    |   |     Irbi           |   |        |  -Itzr    |
// |                         |   | +                  |   | +      |           |
// |                   Ibex (v)  = Qbex          Ibe (v)  = Qbe    |           |
// |  Thermal Network        |   | -                  |   | -      |           |
// |           dt            |   |                    |   |        |           |
// |  ---------o---------    ----+--------------------+---+--------o ei        |
// |  |        |        |                                          |           |
// |  |        |        | +                                        |           |
// | (^) Ith  (v) Irth  = Qcth                                    (^) Ire      |
// |  |        |        | -                                        |           |
// |  |        |        |                                          |           |
// |  ---------o---------                                          o e         |
// |           tl                                                              |
// |                                                                           |
// |  Excess Phase Network                                                     |
// |           xf1                                                             |
// |  ---------o----(=>)----o xf2                                              |
// |  |        |    Flxf    |                                                  |
// |  |        | +          |                                                  |
// | (^) Itzf  = Qcxf      (v) Itxf                                            |
// |  |        | -          |                                                  |
// |  |        |            |                                                  |
// |  ---------o-------------                                                  |
// |          gnd                                                              |
// |                                                                           |
// ---------------------------------------------------------------------------
'''
from OSIM.Modeling.AbstractComponents.CompositeComponent import CompositeComponent
from OSIM.Modeling.Components.Capacity import Capacity
from OSIM.Modeling.Components.NPN_Vertical_Bipolar_Intercompany_Model.VBIC_Charges.VBIC_DiffusionCharges import *
from OSIM.Modeling.Components.NPN_Vertical_Bipolar_Intercompany_Model.VBIC_Charges.VBIC_QuasiSaturationCharges import QBC
from OSIM.Modeling.Components.NPN_Vertical_Bipolar_Intercompany_Model.VBIC_Currents.IBC import IBC
from OSIM.Modeling.Components.NPN_Vertical_Bipolar_Intercompany_Model.VBIC_Currents.IBE import IBE
from OSIM.Modeling.Components.NPN_Vertical_Bipolar_Intercompany_Model.VBIC_Currents.IRCI import IRCI
from OSIM.Modeling.Components.NPN_Vertical_Bipolar_Intercompany_Model.VBIC_Resistors.RBI import RBI
from OSIM.Modeling.Components.NPN_Vertical_Bipolar_Intercompany_Model.VBIC_Currents.VBIC_TransportCurrent import MainTransportCurrent
from OSIM.Modeling.Components.NPN_Vertical_Bipolar_Intercompany_Model.VBIC_ParasitPNP.IBCP import IBCP
from OSIM.Modeling.Components.NPN_Vertical_Bipolar_Intercompany_Model.VBIC_ParasitPNP.IBEP import IBEP
from OSIM.Modeling.Components.NPN_Vertical_Bipolar_Intercompany_Model.VBIC_ParasitPNP.VBIC_ParasitTransportCurrent import ParasitTransportCurrent
from OSIM.Modeling.Components.Resistor import Resistor
from VBIC_Charges.VBIC_DepletionCharge import VBIC_DepletionCharge

'''
TODO: AVALANCHE EFFEKT bei IBC!!!!!!!!!!!!!!!!!!!!!!!!!!!!
'''

class NPN_VBIC(CompositeComponent):
    def __init__(self, nodes, name, value, superComponent, **kwargs):
        super(NPN_VBIC, self).__init__(nodes, name, value, superComponent, **kwargs)

        '''
        Parameter
        '''

        for name, value in kwargs.items():
            if name == 'addargs':
                addargs = value
                for k in addargs:
                    if k in self.variableDict:
                        self.variableDict[k] = addargs[k]

        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec (variableExpr)

        self.NR = eval(self.paramDict.get("nr", "1"))
        self.UT = eval(self.paramDict.get("ut", "0.026"))

        '''
        Knoten
        '''
        # external nodes
        self.b = self.nodes[1]
        self.c = self.nodes[0]
        self.e = self.nodes[2]
        self.s = "SUB"

        # internal nodes
        self.bi = self.myName("bi")
        self.bx = self.myName("bx")
        self.bp = self.myName("bp")
        self.ci = self.myName("ci")
        self.ei = self.myName("ei")
        self.cx = self.myName("cx")
        self.si = self.myName("si")

        # excess phase
        #self.xf1 = self.myName("xf1")
        #self.xf2 = self.myName("xf2")

        '''
        Bauteile
        '''
        # Transportstromquelle Haupttransistor
        #self.IT = MainTransportCurrent([self.c, self.b, self.e], self.myName("IT"), 0, self)
        self.IT = MainTransportCurrent([self.ci, self.bi, self.ei], self.myName("IT"), 0, self,paramdict=self.paramDict,variabledict=self.variableDict)
        # Oxid - Overlap Capacities
        self.QBEO = Capacity([self.b,self.e],self.myName("QBEO"),eval(self.paramDict.get("cbeo", "0")),self)
        self.QBCO = Capacity([self.b,self.e],self.myName("QBCO"),eval(self.paramDict.get("cbco", "0")),self)
        self.QCSO = Capacity([self.b,self.e],self.myName("QCSO"),eval(self.paramDict.get("ccso", "1e-30")),self)

        # Stroeme Haupttransistor
        self.IBE = IBE([self.bi, self.ei], self.myName("IBE"), 0, self,paramdict=self.paramDict,variabledict=self.variableDict)
        self.IBC = IBC([self.bi, self.ci], self.myName("IBC"), 0, self,paramdict=self.paramDict,variabledict=self.variableDict)
        #self.IBEX = IBE([self.bx, self.ei], self.myName("IBEX"), 0, self, isExternal=True,dict=self.paramDict) #wird bei ihp nicht mit-simuliert
        #self.IRCI = IRCI([self.cx,self.ci,self.bi],self.myName("IRCI"),0,self,paramdict=self.paramDict,variabledict=self.variableDict)
        self.bypassIRCI = Resistor([self.cx, self.ci], self.myName("RByP"), 100, self)

        # Bahnwidestaende
        re = eval(self.paramDict.get("re", "5.3"))
        rbx = eval(self.paramDict.get("rbx", "8"))
        rcx = eval(self.paramDict.get("rcx", "6.5"))
        rbp = eval(self.paramDict.get("rbp", "10"))
        rs = eval(self.paramDict.get("rs", "50"))
        rbi = eval(self.paramDict.get("rbi", "20"))

        self.RE = Resistor([self.ei, self.e], self.myName("RE"),re, self)
        self.RBX = Resistor([self.b, self.bx], self.myName("RBX"),rbx, self)
        #self.RBI = RBI([self.bx, self.bi], self.myName("RBI"), 0, self,paramdict=self.paramDict,variabledict=self.variableDict)
        self.RBI = Resistor([self.bx, self.bi], self.myName("RBI"), rbi, self)
        self.RCX = Resistor([self.c, self.cx], self.myName("RCX"),rcx, self)
        self.RBP = Resistor([self.bp, self.cx], self.myName("RBP"), rbp, self)
        self.RS = Resistor([self.si, self.s], self.myName("RS"),rs , self)

        # Depletion Charges
        self.PE = eval(self.paramDict.get("pe", "0.9"))
        self.PC = eval(self.paramDict.get("pc", "0.9"))
        self.ME = eval(self.paramDict.get("me", "0.105"))
        self.MC = eval(self.paramDict.get("mc", "0.105"))
        self.MS = eval(self.paramDict.get("ms", "0.105"))
        self.FC = eval(self.paramDict.get("fc", "0.97"))
        self.PS = eval(self.paramDict.get("ps", "0.97"))
        self.AJE = eval(self.paramDict.get("aje", "-0.5"))
        self.AJS = eval(self.paramDict.get("ajs", "-0.5"))
        self.AJC = eval(self.paramDict.get("ajc", "-0.5"))
        self.WBE = eval(self.paramDict.get("wbe", "1"))
        self.CJE = eval(self.paramDict.get("cje", "9.7E-15"))
        self.CJC = eval(self.paramDict.get("cjc", "8E-16"))
        self.CJCP = eval(self.paramDict.get("cjcp", "8E-15"))*0.3
        self.CJEP = eval(self.paramDict.get("cjep", "4.2E-15"))*0.3

        #self.QJBEX = VBIC_DepletionCharge([self.bx, self.ei], self.myName("QJBEX"), 0, self,paramdict= {'CJx':self.CJE,'P':self.PE, 'M':self.ME,'F':self.FC, 'AJ' :self.AJE ,'FAK':(1-self.WBE)})
        self.QJBE = VBIC_DepletionCharge([self.bi, self.ei], self.myName("QJBE"),  0,self, paramdict= {'CJx':self.CJE, 'P':self.PE, 'M':self.ME,'F':self.FC, 'AJ' :self.AJE,'FAK':self.WBE})
        self.QJBC = VBIC_DepletionCharge([self.bi, self.ci], self.myName("QJBC"), 0,self, paramdict= {'CJx':self.CJC,'P':self.PC, 'M':self.MC,'F':self.FC, 'AJ' :self.AJC})
        self.QJBCP = VBIC_DepletionCharge([self.bp, self.si], self.myName("QJBCP"), 0, self,paramdict= {'CJx':self.CJCP,'P':self.PC, 'M':self.MS,'F':self.FC, 'AJ' :self.AJS})
        self.QJBEP = VBIC_DepletionCharge([self.bp, self.bx], self.myName("QJBEP"), 0, self,paramdict= {'CJx':self.CJEP,'P':self.PS, 'M':self.MC,'F':self.FC, 'AJ' :self.AJC})

        #Diffuison Charges
        self.QDBE = QDBE([self.bi, self.ei], self.myName("QDBE"),0, self,paramdict=self.paramDict,variabledict=self.variableDict)
        self.QDBC = QDBC([self.bx, self.ci], self.myName("QDBC"),0, self,paramdict=self.paramDict,variabledict=self.variableDict)

        #Quasi-Saturation Charges
        #self.QBCX = QBC([self.bi, self.cx], self.myName("QBCX"),0, self, paramdict=self.paramDict)
        #self.QBCI = QBC([self.bi, self.ci], self.myName("QBCI"),0, self, paramdict=self.paramDict)

        ### Stroeme Parasitischer Transistor
        # Parasitischer Transistor:
        self.ICCP = ParasitTransportCurrent([self.bx, self.bp, self.si], self.myName("ICCP"), 0, self,paramdict=self.paramDict,variabledict=self.variableDict)
        # Dioden-aehnliche Stroeme:
        self.IBCP = IBCP([self.si, self.bp], self.myName("IBCP"), 0, self,paramdict=self.paramDict,variabledict=self.variableDict)
        self.IBEP = IBEP([self.bx, self.bp], self.myName("IBEP"), 0, self,paramdict=self.paramDict,variabledict=self.variableDict)

        #self.QDBEP = QDBEP([self.bx, self.bp], self.myName("QDBEP"), 0, self,ParasitCurSource=self.ICCP,paramdict=self.paramDict,variabledict=self.variableDict)
        '''
        Hilfswiderstaende:
        '''
        self.RH1 = Resistor([self.b, self.c], self.myName("RH1"),1e12, self)
        self.RH2 = Resistor([self.b, self.e], self.myName("RH2"),1e12, self)
        self.RH3 = Resistor([self.bp, self.bx], self.myName("RH3"),1e12, self)
        self.RH4 = Resistor([self.bp, self.si], self.myName("RH4"),1e12, self)

        '''ideale Ersatzkapazitaeten'''
        #self.QJBEX = Capacity([self.bx,self.ei],self.myName("QJBEX"),1e-15,self)
        #self.QJBE = Capacity([self.bi,self.ei],self.myName("QJBE"),1e-15,self)
        #self.QJBC = Capacity([self.bi,self.ci],self.myName("QJBC"),1e-15,self)
        #self.QJBCP = Capacity([self.bp,self.si],self.myName("QJBCP"),1e-15,self)
        #self.QJBEP = Capacity([self.bp,self.bx],self.myName("QJBEP"),1e-15,self)
        self.QDBEP = Capacity([self.bx, self.ci], self.myName("QDBEP"), 0.5e-15, self)

        #Diffuison Charges
        #self.QDBE = Capacity([self.bi,self.ei],self.myName("QDBE"),1e-15,self)
        #self.QDBC = Capacity([self.bx,self.ci],self.myName("QDBC"),1e-15,self)

        #Quasi-Saturation Charges
        self.QBCX = Capacity([self.bi,self.cx],self.myName("QBCX"),1e-18,self)
        self.QBCI = Capacity([self.bi,self.ci],self.myName("QBCI"),1e-18,self)


    def containsNonlinearity(self):
        return True

    def setParameterOrVariableValue(self, name, value):
        if(name in self.variableDict.keys()):
            self.variableDict[name] = str(value)
            self.reloadParams()

    def getTransportCurrent(self):
        return self.IT.current

    def ditr_A(self):
        return self.IT.itr/(self.NR * self.UT)

    def reloadParams(self):
        for v in self.variableDict:
            variableExpr = "".join((v, "=", self.variableDict[v]))
            exec(variableExpr)

        self.PE = eval(self.paramDict.get("pe", "0.9"))
        self.PC = eval(self.paramDict.get("pc", "0.9"))
        self.ME = eval(self.paramDict.get("me", "0.105"))
        self.MC = eval(self.paramDict.get("mc", "0.105"))
        self.MS = eval(self.paramDict.get("ms", "0.105"))
        self.FC = eval(self.paramDict.get("fc", "0.97"))
        self.PS = eval(self.paramDict.get("ps", "0.97"))
        self.AJE = eval(self.paramDict.get("aje", "-0.5"))
        self.AJS = eval(self.paramDict.get("ajs", "-0.5"))
        self.AJC = eval(self.paramDict.get("ajc", "-0.5"))
        self.WBE = eval(self.paramDict.get("wbe", "1"))
        self.CJE = eval(self.paramDict.get("cje", "9.7E-15"))
        self.CJC = eval(self.paramDict.get("cjc", "8E-16"))
        self.CJCP = eval(self.paramDict.get("cjcp", "8E-15"))*0.3
        self.CJEP = eval(self.paramDict.get("cjep", "4.2E-15"))*0.3

        #self.QJBEX.setNewParamsAndVariablesDicts({'P': self.PE, 'M': self.ME, 'F': self.FC, 'AJ': self.AJE,
        #                                        'FAK': (1 - self.WBE)},dict())
        self.QJBE.setNewParamsAndVariablesDicts({'CJx':self.CJE,'P': self.PE, 'M': self.ME, 'F': self.FC, 'AJ': self.AJE,
                                               'FAK': self.WBE},dict())
        self.QJBC.setNewParamsAndVariablesDicts({'CJx':self.CJE,'P': self.PC, 'M': self.MC, 'F': self.FC, 'AJ': self.AJC},dict())
        #self.QJBCP.setNewParamsAndVariablesDicts({'CJx':self.CJCP,'P': self.PS, 'M': self.MS, 'F': self.FC, 'AJ': self.AJS},dict())
        #self.QJBEP.setNewParamsAndVariablesDicts({'CJx':self.CJEP,'P': self.PC, 'M': self.MC, 'F': self.FC, 'AJ': self.AJC},dict())

        # Diffuison Charges
        self.QDBE.setNewParamsAndVariablesDicts(self.paramDict,self.variableDict)
        self.QDBC.setNewParamsAndVariablesDicts(self.paramDict,self.variableDict)

        re = eval(self.paramDict.get("re", "5.3"))
        rbx = eval(self.paramDict.get("rbx", "8"))
        rcx = eval(self.paramDict.get("rcx", "6.5"))
        rbp = eval(self.paramDict.get("rbp", "10"))
        rs = eval(self.paramDict.get("rs", "50"))
        rbi = eval(self.paramDict.get("rbi", "20"))

        self.RE.setParameterOrVariableValue("R",re)
        self.RBX .setParameterOrVariableValue("R", rbx)
        #self.RBI = Resistor([self.bx, self.bi], self.myName("RBI"), rbi, self)
        self.RCX.setParameterOrVariableValue("R",rcx)
        self.RBP.setParameterOrVariableValue("R",rbp)
        self.RS.setParameterOrVariableValue("R",rs)
        #self.RBI.setParameterOrVariableValue("R",rbi)

        # Stroeme Haupttransistor
        self.IT.setNewParamsAndVariablesDicts(self.paramDict,self.variableDict)
        self.IBE.setNewParamsAndVariablesDicts(self.paramDict,self.variableDict)
        self.IBC.setNewParamsAndVariablesDicts(self.paramDict,self.variableDict)
        # self.IBEX = IBE([self.bx, self.ei], self.myName("IBEX"), 0, self, isExternal=True,dict=self.paramDict) #wird bei ihp nicht mit-simuliert
        #self.IRCI.setNewParamsAndVariablesDicts(self.paramDict,self.variableDict)

        ### Stroeme Parasitischer Transistor
        # Parasitischer Transistor:
        self.ICCP.setNewParamsAndVariablesDicts(self.paramDict,self.variableDict)
        # Dioden-aehnliche Stroeme:
        self.IBCP.setNewParamsAndVariablesDicts(self.paramDict,self.variableDict)
        self.IBEP.setNewParamsAndVariablesDicts(self.paramDict,self.variableDict)
        # self.QDBEP = QDBEP([self.bx, self.bp], self.myName("QDBEP"), 0, self,ParasitCurSource=self.ICCP)

        # Quasi-Saturation Charges
        # self.QBCX.setNewParamsAndVariablesDicts(self.paramDict,self.variableDict)
        # self.QBCI.setNewParamsAndVariablesDicts(self.paramDict,self.variableDict)
