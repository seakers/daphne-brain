#!/usr/bin/env python

import sys,os
import glob

sys.path.append(os.path.dirname(__file__))

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from data_mining_API.interface import interface as DataMiningInterface
from data_mining_API.interface.ttypes import BinaryInputArchitecture, DiscreteInputArchitecture, Feature


from config.loader import ConfigurationLoader
config = ConfigurationLoader().load()


class DataMiningClient():
    
    def __init__(self):
        
        port = config['data-mining']['port']

        # Make socket
        self.transport = TSocket.TSocket('localhost', port)
    
        # Buffering is critical. Raw sockets are very slow
        self.transport = TTransport.TBufferedTransport(self.transport)
    
        # Wrap in a protocol
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        
        # Create a client to use the protocol encoder
        self.client = DataMiningInterface.Client(self.protocol)
        
    
    def startConnection(self):
        # Connect
        self.transport.open()

    
    def endConnection(self):
        # Close
        self.transport.close()
        
    def ping(self):
        self.client.ping()
        print('ping()')
        
    def getDrivingFeatures(self, problem, inputType, behavioral, non_behavioral, all_archs, supp, conf, lift):
        # try:
        print('getDrivingFeatures')
        print('b_length:{0}, nb_length:{1}, narchs:{2}'.format(len(behavioral),len(non_behavioral),len(all_archs)))
        
        archs_formatted = []
        if inputType == "binary":
            for arch in all_archs:
                archs_formatted.append(BinaryInputArchitecture(arch['id'],arch['inputs'],arch['outputs']))
            drivingFeatures_formatted = self.client.getDrivingFeaturesBinary(problem, behavioral, non_behavioral, archs_formatted, supp, conf, lift)

        elif inputType == "discrete":
            for arch in all_archs:
                inputs = []
                for i in arch['inputs']:
                    inputs.append(int(i))
                archs_formatted.append(DiscreteInputArchitecture(arch['id'], inputs, arch['outputs']))
            drivingFeatures_formatted = self.client.getDrivingFeaturesDiscrete(problem, behavioral, non_behavioral, archs_formatted, supp, conf, lift)

        drivingFeatures = []
        for df in drivingFeatures_formatted:
            drivingFeatures.append({'id':df.id,'name':df.name,'expression':df.expression,'metrics':df.metrics, 'complexity':df.complexity})

        # except Exception as e:
        #     print("Exc in getDrivingFeatures: " + str(e))

        return drivingFeatures

    def getDrivingFeaturesEpsilonMOEA(self, problem, inputType, behavioral, non_behavioral, all_archs):
        # try:
        print('getDrivingFeatures')
        print('b_length:{0}, nb_length:{1}, narchs:{2}'.format(len(behavioral),len(non_behavioral),len(all_archs)))
        
        archs_formatted = []
        if inputType == "binary":
            for arch in all_archs:
                archs_formatted.append(BinaryInputArchitecture(arch['id'],arch['inputs'],arch['outputs']))
            drivingFeatures_formatted = self.client.getDrivingFeaturesEpsilonMOEABinary(problem, behavioral, non_behavioral, archs_formatted)

        elif inputType == "discrete":
            for arch in all_archs:
                inputs = []
                for i in arch['inputs']:
                    inputs.append(int(i))
                archs_formatted.append(DiscreteInputArchitecture(arch['id'], inputs, arch['outputs']))
            drivingFeatures_formatted = self.client.getDrivingFeaturesEpsilonMOEADiscrete(problem, behavioral, non_behavioral, archs_formatted)

        drivingFeatures = []
        for df in drivingFeatures_formatted:
            drivingFeatures.append({'id':df.id,'name':df.name,'expression':df.expression,'metrics':df.metrics})

        return drivingFeatures
    
    def getDrivingFeaturesAutomated(self, problem, inputType, behavioral, non_behavioral, all_archs, supp, conf, lift):
        # try:
        print('getDrivingFeatures')
        print('b_length:{0}, nb_length:{1}, narchs:{2}'.format(len(behavioral),len(non_behavioral),len(all_archs)))
        
        archs_formatted = []
        if inputType == "binary":
            for arch in all_archs:
                archs_formatted.append(BinaryInputArchitecture(arch['id'],arch['inputs'],arch['outputs']))
            drivingFeatures_formatted = self.client.runAutomatedLocalSearchBinary(problem, behavioral, non_behavioral, archs_formatted, supp, conf, lift)

        elif inputType == "discrete":
            for arch in all_archs:
                inputs = []
                for i in arch['inputs']:
                    inputs.append(int(i))
                archs_formatted.append(DiscreteInputArchitecture(arch['id'], inputs, arch['outputs']))
            drivingFeatures_formatted = self.client.runAutomatedLocalSearchDiscrete(problem, behavioral, non_behavioral, archs_formatted, supp, conf, lift)

        drivingFeatures = []
        for df in drivingFeatures_formatted:
            drivingFeatures.append({'id':df.id,'name':df.name,'expression':df.expression,'metrics':df.metrics, 'complexity':df.complexity})

        # except Exception as e:
        #     print("Exc in getDrivingFeatures: " + str(e))

        return drivingFeatures
        
    def getMarginalDrivingFeatures(self, problem, inputType, behavioral, non_behavioral, all_archs, featureExpression,logicalConnective, supp, conf, lift):
        try:
            print('getMarginalDrivingFeatures')
            print('b_length:{0}, nb_length:{1}, narchs:{2}'.format(len(behavioral),len(non_behavioral),len(all_archs)))
            
            archs_formatted = []
            if inputType == "binary":
                for arch in all_archs:
                    archs_formatted.append(BinaryInputArchitecture(arch['id'],arch['inputs'],arch['outputs']))
                drivingFeatures_formatted = self.client.getMarginalDrivingFeaturesBinary(problem, behavioral, non_behavioral, archs_formatted, 
                                                                           featureExpression, logicalConnective, supp, conf, lift)

            elif inputType == "discrete":
                for arch in all_archs:
                    inputs = []
                    for i in arch['inputs']:
                        inputs.append(int(i))
                    archs_formatted.append(DiscreteInputArchitecture(arch['id'], inputs, arch['outputs']))
                drivingFeatures_formatted = self.client.getMarginalDrivingFeaturesDiscrete(problem, behavioral, non_behavioral, archs_formatted, 
                                                                           featureExpression, logicalConnective, supp, conf, lift)
                        
            drivingFeatures = []
            
            for df in drivingFeatures_formatted:
                drivingFeatures.append({'id':df.id,'name':df.name,'expression':df.expression,'metrics':df.metrics, 'complexity':df.complexity})
                
        except Exception as e:
            print('Exc in calling getMarginalDrivingFeatures(): '+str(e))

        return drivingFeatures

    def convertToDNF(self, expression):
        try:
            dnf_expression = self.client.convertToDNF(expression)
        except Exception as e:
            print('Exc in calling convertToDNF(): '+str(e))

        return dnf_expression

    def convertToCNF(self, expression):
        try:
            cnf_expression = self.client.convertToCNF(expression)
        except Exception as e:
            print('Exc in calling convertToCNF(): '+str(e))

        return cnf_expression

    def computeTypicality(self, inputs, expression):
        try:
            arch_formatted = BinaryInputArchitecture(0, inputs, [])
            typicality = self.client.computeAlgebraicTypicality(arch_formatted, expression)

        except Exception as e:
            print('Exc in calling computeComplexity(): '+str(e))

        return typicality

    def computeComplexity(self, expression):
        try:
            complexity = self.client.computeComplexity(expression)
        except Exception as e:
            print('Exc in calling computeComplexity(): '+str(e))

        return complexity

    def computeComplexityOfFeatures(self, expressions):
        try:
            complexity_values = self.client.computeComplexityOfFeatures(expressions)
        except Exception as e:
            print('Exc in calling computeComplexityOfFeatures(): '+str(e))

        return complexity_values

