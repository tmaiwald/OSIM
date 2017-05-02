#!/usr/bin/python
from OSIM.Modeling.CircuitSystemEquations import CircuitSystemEquations
from OSIM.Simulation.CircuitAnalysis.CircuitAnalyser import CircuitAnalyser
from OSIM.Simulation.NetToComp import NetToComp

circuit = 'TransistorTB.net'
#circuit = '__Circuits/TransistorInversTB.net'
#circuit = '__Circuits/twoTrans.net'
#circuit = '__Circuits/DiodeTB.net'
#circuit = '__Circuits/AmplifierTB2.net'
#circuit = '__Circuits/AmplifierTB.net'
#circuit = '__Circuits/lowpassTB.net'
#circuit = '__Circuits/CapacityTB.net'
#circuit = '__Circuits/SParameterTB.net'
#circuit = '__Circuits/TransAnalysisTB.net'
#circuit = '__Circuits/TransTransistorAnalysisTB.net'
#circuit = '__Circuits/LoBuffer.net'
#circuit = '__Circuits/Diffamp.net'

seq = CircuitSystemEquations(NetToComp(circuit).getComponents())
ca = CircuitAnalyser(seq)
#CharactersiticCurves(seq).createCharacteristicCurves('V2',-0.7, 1.3, 0.005,'P1V',1, 1.2 , 0.1, ["Q1IT"])
ca.plot_lin(ca.getDCParamSweep('V2',0,1.3,0.005,["Q1IT"],'P1V',[0.9]))

#CircuitAnalysis(seq).calcDCOperatingPoint()
#ACAnalysis(seq).show(3, 11, 10, "OUT", 'P1V')
#SParameterAnalysis(seq).show(8, 12, 10)
#DCAnalysis(seq).show('V1', -1, 2, 0.01, ["D1", "1"])
#TransAnalysis(seq).show(0, 1e-10, 1e-13, ["OUT", "Q1IT"], "Q1IT")
