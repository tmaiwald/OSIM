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
        vbic_rbx = 1 # TODO: ?????
        vbic_re = 1 # TODO: ?????
        vbic_rcx = 1 # TODO: ?????
        vbic_cje = 1
        vbic_cje_mm = 1
        vbic_cjc = 1
        vbic_cjc_mm = 1
        vbic_cjcp = 1
        vbic_cjcp_mm = 1
        vbic_is = 1
        vbic_is_mm = 1
        vbic_re_mm =1
        vbic_rbx_mm = 1
        vbic_rcx_mm = 1

        Nx = eval(self.paramDict.get("Nx", "1"))
        self.PE = eval(self.paramDict.get("pe", "1"))
        self.PC = eval(self.paramDict.get("pc", "1"))
        self.ME = eval(self.paramDict.get("me", "1"))
        self.MC = eval(self.paramDict.get("mc", "1"))
        self.MS = eval(self.paramDict.get("ms", "1"))
        self.FC = eval(self.paramDict.get("fc", "1"))
        self.PS = eval(self.paramDict.get("ps", "1"))
        self.AJE = eval(self.paramDict.get("aje", "1"))
        self.AJS = eval(self.paramDict.get("ajs", "1"))
        self.AJC = eval(self.paramDict.get("ajc", "1"))
        self.CJE =  eval(self.paramDict.get("cje", "1"))
        self.CJC =  eval(self.paramDict.get("cjc", "1"))
        self.CJEP =  eval(self.paramDict.get("cjep", "1"))
        self.CJCP =  eval(self.paramDict.get("cjcp", "1"))
        self.WBE =  eval(self.paramDict.get("wbe", "1"))
        self.VEF = eval(self.paramDict.get("vef", "30"))
        self.VER = eval(self.paramDict.get("ver", "60"))
        self.IKF = eval(self.paramDict.get("ikf", "10e10"))
        self.IKR = eval(self.paramDict.get("ikr", "10e10"))
        self.NKF = eval(self.paramDict.get("nkf", "0.5"))
        self.NF = eval(self.paramDict.get("nf", "1"))
        self.NR = eval(self.paramDict.get("nr", "1"))
        self.IS = eval(self.paramDict.get("is", "1e-16"))
        self.UT = eval(self.paramDict.get("Ut", "0.026"))
        self.CBEO = eval(self.paramDict.get("cbeo", "0"))
        self.CBCO = eval(self.paramDict.get("cbco", "0"))
        self.CCSO = eval(self.paramDict.get("ccso", "1e-30"))

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
        self.IT = MainTransportCurrent([self.ci, self.bi, self.ei], self.myName("IT"), 0, self,dict=self.paramDict)
        # Oxid - Overlap Capacities
        self.QBEO = Capacity([self.b,self.e],self.myName("QBEO"),self.CBEO,self)
        self.QBCO = Capacity([self.b,self.e],self.myName("QBCO"),self.CBCO,self)
        self.QCSO = Capacity([self.b,self.e],self.myName("QCSO"),self.CCSO,self)

        # Stroeme Haupttransistor
        self.IBE = IBE([self.bi, self.ei], self.myName("IBE"), 0, self,dict=self.paramDict)
        self.IBC = IBC([self.bi, self.ci], self.myName("IBC"), 0, self,dict=self.paramDict)
        #self.IBEX = IBE([self.bx, self.ei], self.myName("IBEX"), 0, self, isExternal=True,dict=self.paramDict) #wird bei ihp nicht mit-simuliert
        self.IRCI = IRCI([self.cx,self.ci,self.bi],self.myName("IRCI"),0,self,dict=self.paramDict)
        #self.bypassIRCI = Resistor([self.cx, self.ci], self.myName("RByP"), 100, self)

        # Bahnwidestaende
        re = eval(self.paramDict.get("re", "1"))
        rbx = eval(self.paramDict.get("rbx", "1"))
        rcx = eval(self.paramDict.get("rcx", "1"))
        rbp = eval(self.paramDict.get("rbp", "1"))
        rs  = eval(self.paramDict.get("rs", "1"))
        rbi = eval(self.paramDict.get("rbi", "1"))

        self.RE = Resistor([self.ei, self.e], self.myName("RE"),re, self)
        self.RBX = Resistor([self.b, self.bx], self.myName("RBX"),rbx, self)
        self.RBI = RBI([self.bx, self.bi], self.myName("RBI"), rbi, self)
        #self.RBI = Resistor([self.bx, self.bi], self.myName("RBI"), rbi, self)
        self.RCX = Resistor([self.c, self.cx], self.myName("RCX"),rcx, self)
        self.RBP = Resistor([self.bp, self.cx], self.myName("RBP"), rbp, self)
        self.RS = Resistor([self.si, self.s], self.myName("RS"),rs , self)

        self.QJBEX = VBIC_DepletionCharge([self.bx, self.ei], self.myName("QJBEX"), self.CJE, self, dict= {'P':self.PE, 'M':self.ME,'F':self.FC, 'AJ' :self.AJE ,'FAK':(1-self.WBE)})
        self.QJBE = VBIC_DepletionCharge([self.bi, self.ei], self.myName("QJBE"), self.CJE,self, dict= {'P':self.PE, 'M':self.ME,'F':self.FC, 'AJ' :self.AJE,'FAK':self.WBE})
        self.QJBC = VBIC_DepletionCharge([self.bi, self.ci], self.myName("QJBC"), self.CJC,self, dict= {'P':self.PC, 'M':self.MC,'F':self.FC, 'AJ' :self.AJC})
        self.QJBCP = VBIC_DepletionCharge([self.bp, self.si], self.myName("QJBCP"), self.CJCP, self,dict= {'P':self.PS, 'M':self.MS,'F':self.FC, 'AJ' :self.AJS})
        self.QJBEP = VBIC_DepletionCharge([self.bp, self.bx], self.myName("QJBEP"), self.CJEP, self,dict= {'P':self.PC, 'M':self.MC,'F':self.FC, 'AJ' :self.AJC})

        #Diffuison Charges
        self.QDBE = QDBE([self.bi, self.ei], self.myName("QDBE"),0, self,dict=self.paramDict)
        self.QDBC = QDBC([self.bx, self.ci], self.myName("QDBC"),0, self,dict=self.paramDict)

        #Quasi-Saturation Charges
        #self.QBCX = QBC([self.bi, self.cx], self.myName("QBCX"),0, self, dict=self.paramDict)
        #self.QBCI = QBC([self.bi, self.ci], self.myName("QBCI"),0, self, dict=self.paramDict)

        ### Stroeme Parasitischer Transistor
        # Parasitischer Transistor:
        self.ICCP = ParasitTransportCurrent([self.bx, self.bp, self.si], self.myName("ICCP"), 0, self,dict=self.paramDict)
        # Dioden-aehnliche Stroeme:
        self.IBCP = IBCP([self.si, self.bp], self.myName("IBCP"), 0, self,dict=self.paramDict)
        self.IBEP = IBEP([self.bx, self.bp], self.myName("IBEP"), 0, self,dict=self.paramDict)
        #self.QDBEP = QDBEP([self.bx, self.bp], self.myName("QDBEP"), 0, self,ParasitCurSource=self.ICCP)
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

        #Diffuison Charges
        #self.QDBE = Capacity([self.bi,self.ei],self.myName("QDBE"),1e-15,self)
        #self.QDBC = Capacity([self.bx,self.ci],self.myName("QDBC"),1e-15,self)

        #Quasi-Saturation Charges
        self.QBCX = Capacity([self.bi,self.cx],self.myName("QBCX"),1e-15,self)
        self.QBCI = Capacity([self.bi,self.ci],self.myName("QBCI"),1e-15,self)


    def containsNonlinearity(self):
        return True

    def setParameterValue(self,paramName,paramVal):
        if(paramName == "Nx"):
            self.reloadParams_vbic(paramVal)
            for i in self.internalComponents:
                i.setParameterValue()

    def getTransportCurrent(self):
        return self.IT.current

    def ditr_A(self):
        return self.IT.itr[0] / (self.NR * self.UT)

    def reloadParams_vbic(self, Nx):

        self.PE = eval(self.paramDict.get("pe", "1"))
        self.PC = eval(self.paramDict.get("pc", "1"))
        self.ME = eval(self.paramDict.get("me", "1"))
        self.MC = eval(self.paramDict.get("mc", "1"))
        self.MS = eval(self.paramDict.get("ms", "1"))
        self.FC = eval(self.paramDict.get("fc", "1"))
        self.PS = eval(self.paramDict.get("ps", "1"))
        self.AJE = eval(self.paramDict.get("aje", "1"))
        self.AJS = eval(self.paramDict.get("ajs", "1"))
        self.AJC = eval(self.paramDict.get("ajc", "1"))
        self.CJE = eval(self.paramDict.get("cje", "1"))
        self.CJC = eval(self.paramDict.get("cjc", "1"))
        self.CJEP = eval(self.paramDict.get("cjep", "1"))
        self.CJCP = eval(self.paramDict.get("cjcp", "1"))
        self.WBE = eval(self.paramDict.get("wbe", "1"))
        self.VEF = eval(self.paramDict.get("vef", "30"))
        self.VER = eval(self.paramDict.get("ver", "60"))
        self.IKF = eval(self.paramDict.get("ikf", "10e10"))
        self.IKR = eval(self.paramDict.get("ikr", "10e10"))
        self.NKF = eval(self.paramDict.get("nkf", "0.5"))
        self.NF = eval(self.paramDict.get("nf", "1"))
        self.NR = eval(self.paramDict.get("nr", "1"))
        self.IS = eval(self.paramDict.get("is", "1e-16"))
        self.UT = eval(self.paramDict.get("Ut", "0.026"))
        self.CBEO = eval(self.paramDict.get("cbeo", "0"))
        self.CBCO = eval(self.paramDict.get("cbco", "0"))
        self.CCSO = eval(self.paramDict.get("ccso", "1e-30"))