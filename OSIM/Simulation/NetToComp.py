"""Use the triangle class to represent triangles."""

import re
from OSIM.Modeling.Components.Capacity import Capacity
from OSIM.Modeling.Components.CurrentSource import CurrentSource
from OSIM.Modeling.Components.Diode import Diode
from OSIM.Modeling.Components.Inductance import Inductance
from OSIM.Modeling.Components.Port import Port
from OSIM.Modeling.Components.Resistor import Resistor
import os

import Utils as u
from OSIM.Modeling.Components.NPN_Vertical_Bipolar_Intercompany_Model.NPN_VBIC import NPN_VBIC

class NetToComp(object):
    """Beispielkommentar"""

    def __init__(self, filename):
        """

        :param filename:
        :type filename:
        """

        projRootFold = u.getDirectory()
        print()
        netListFile = os.path.join(os.path.abspath('../..'), '__Diverse Schaltungen',filename)#"".join((projRootFold,"/__Circuits/",filename))

        self.spice_netlist = open(netListFile, 'rb')

        self.components = []

        comments = self.getCommentsFromNetlist(netListFile)

        for line in self.spice_netlist:
            d = line[0]
            if d in ['R', 'V', 'C', 'L', 'D', 'Q', 'I', 'K','P']:
                arr = line.split()
                nodefrom = arr[1]
                nodeto = arr[2]
                name = arr[0]
                value = arr[3]

                if d == 'R':
                    r = Resistor([nodefrom, nodeto], name, value, None)
                    self.components.append(r)
                elif d == 'V':
                    #r = VoltageSource([nodefrom, nodeto], name, value, None)
                    args = self.stringArrToDict(arr[4:])
                    args = self.parseCommentsToArgs(args,comments,name)
                    r = Port([nodefrom, nodeto], name, value, None, dict=args)
                    self.components.append(r)
                elif d == 'I':
                    r = CurrentSource([nodefrom, nodeto], name, value, None)
                    self.components.append(r)
                elif d == 'L':
                    l = Inductance([nodefrom, nodeto], name, value, None)
                    self.components.append(l)
                elif d == 'C':
                    c = Capacity([nodefrom, nodeto], name, value, None)
                    self.components.append(c)
                elif d == 'D':
                    path = "".join((projRootFold,"/__Parameter/Diode_std.comp"))
                    c = Diode([nodefrom, nodeto], name, 0,None, pParams=path)
                    self.components.append(c)
                elif d == 'Q':
                    #npn = NPNTransistor_SGP([arr[1], arr[2], arr[3]], name, arr[4], None, pParams="__Parameter/NPN_Gummel_BC547B.comp")
                    #npn = NPNEasy_SGP([arr[1], arr[2], arr[3]], name, arr[4])
                    path = os.path.join(os.path.abspath('../..'), '__Parameter/NPN_VBIC_npn13G2.comp')
                    npn = NPN_VBIC([arr[1], arr[2], arr[3], '0'], name, arr[4], None, pParams=path)
                    self.components.append(npn)
                elif d == 'K':
                    k = VoltageDependentCurrentSource([nodefrom, nodeto], name, value, None)
                    self.components.append(k)
                elif d == 'P':
                    #nodes, name, voltage, seriesImpedance
                    args = self.stringArrToDict(arr[4:])
                    k = Port([nodefrom, nodeto], name, value, None, dict=args)
                    self.components.append(k)

    def getComponents(self):
        """Create a triangle with sides of lengths `a`, `b`, and `c`.

        Raises `ValueError` if the three length values provided cannot
        actually form a triangle.
        """

        return self.components

    def parseCommentsToArgs(self,args,commentList,name):

        for c in commentList:
            name_args = (c.split(":"))
            n2 = (name_args[0])[2:]
            if(n2 == name):
                arges = re.split(';|\n',name_args[1])
                for a in arges:
                    if(len(a) > 2):
                       param_val = a.split("=")
                       args[param_val[0]]=param_val[1]

        return args


    def getCommentsFromNetlist(self,netListFile):
        """Create a triangle with sides of lengths `a`, `b`, and `c`.

        Raises `ValueError` if the three length values provided cannot
        actually form a triangle.
        """

        comments =[]
        with open(netListFile) as file_:
            for line in file_:
                d = line[0]
                if d == "*":
                    comments.append(line)
        return comments



    @staticmethod
    def readParams(filename, name):
        """Create a triangle with sides of lengths `a`, `b`, and `c`.

        Raises `ValueError` if the three length values provided cannot
        actually form a triangle.
        """

        paramlist = open(filename, 'rb')
        paramDict = dict()

        for line in paramlist:
            d = line[0]
            if not d == '.' and not d == " " and not d == "\n":  # Comments start with '.'
                arr = line.split()
                key = arr[0]
                value = arr[1]
                paramDict["".join((name, "-", key))] = value
        return paramDict

    def stringArrToDict(self, strArr):
        """Create a triangle with sides of lengths `a`, `b`, and `c`.

        Raises `ValueError` if the three length values provided cannot
        actually form a triangle.
        """
        args ={}
        for s in strArr:
            if('=' in s):
                key,value =s.split('=',1)
                args[key]=value
        return args

