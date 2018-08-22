import logging

# Get an instance of a logger
logger = logging.getLogger('data-mining')


from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import numpy as np
import sys,os
import json
import csv

# Print all paths included in sys.path
# from pprint import pprint as p
# p(sys.path)

from data_mining_API.api import DataMiningClient

# Create your views here.
class GetDrivingFeatures(APIView):

    def __init__(self):
        self.DataMiningClient = DataMiningClient()
        pass

    def post(self, request, format=None):
        
        try:
            # Start data mining client
            self.DataMiningClient.startConnection()
            
            # Get threshold values for the metrics
            supp = float(request.POST['supp'])
            conf = float(request.POST['conf'])
            lift = float(request.POST['lift'])
            
            # Get selected arch id's
            selected = request.POST['selected']
            selected = selected[1:-1]
            selected_arch_ids = selected.split(',')
            # Convert strings to ints
            behavioral = []
            for s in selected_arch_ids:
                behavioral.append(int(s))

            # Get non-selected arch id's
            non_selected = request.POST['non_selected']
            non_selected = non_selected[1:-1]
            non_selected_arch_ids = non_selected.split(',')
            # Convert strings to ints
            non_behavioral = []
            for s in non_selected_arch_ids:
                non_behavioral.append(int(s))

            # Load architecture data from the session info
            logger.debug(request.session)
            architectures = request.session['data']

            problem = request.POST['problem']
            inputType = request.POST['input_type']

            #########################################
            #########################################
            ### Write data file with labels

            # dir_path = "/Users/bang/workspace/featureGA/data/"
            # with open(os.path.join(dir_path,"data.csv"), "w") as file:

            #     content = []

            #     for i, arch in enumerate(architectures):
            #         line = []

            #         archID = arch['id']
            #         label = None
            #         if archID in behavioral:
            #             label = "1"
            #         else:
            #             label = "0"

            #         inputs = arch['inputs']
            #         inputString = ""
            #         for val in inputs:
            #             if val:
            #                 inputString += "1"
            #             else:
            #                 inputString += "0"

            #         line.append(str(label))
            #         line.append(inputString)
            #         content.append(",".join(line))    

            #     file.write("\n".join(content))

            #########################################
            #########################################

            drivingFeatures = self.DataMiningClient.getDrivingFeatures(problem, inputType, behavioral, non_behavioral,
                                                                       architectures, supp, conf, lift)
                
            output = drivingFeatures

            # End the connection before return statement
            self.DataMiningClient.endConnection() 
            return Response(output)
        
        except Exception as detail:
            logger.exception('Exception in getDrivingFeatures: ' + str(detail))
            self.DataMiningClient.endConnection()
            return Response('')

class getDrivingFeaturesEpsilonMOEA(APIView):

    def __init__(self):
        self.DataMiningClient = DataMiningClient()
        pass

    def post(self, request, format=None):
        
        try:
            # Start data mining client
            self.DataMiningClient.startConnection()
            
            # Get selected arch id's
            selected = request.POST['selected']
            selected = selected[1:-1]
            selected_arch_ids = selected.split(',')
            
            # Convert strings to ints
            behavioral = []
            for s in selected_arch_ids:
                behavioral.append(int(s))

            # Get non-selected arch id's
            non_selected = request.POST['non_selected']
            non_selected = non_selected[1:-1]
            non_selected_arch_ids = non_selected.split(',')
            # Convert strings to ints
            non_behavioral = []
            for s in non_selected_arch_ids:
                non_behavioral.append(int(s))

            # Load architecture data from the session info
            logger.debug(request.session)
            architectures = request.session['data']

            problem = request.POST['problem']
            inputType = request.POST['input_type']

            drivingFeatures = self.DataMiningClient.getDrivingFeaturesEpsilonMOEA(problem, inputType, behavioral, non_behavioral, architectures)
            output = drivingFeatures

            # End the connection before return statement
            self.DataMiningClient.endConnection() 
            return Response(output)
        
        except Exception as detail:
            logger.exception('Exception in getDrivingFeatures: ' + str(detail))
            self.DataMiningClient.endConnection()
            return Response('')

class getDrivingFeaturesWithGeneralization(APIView):

    def __init__(self):
        self.DataMiningClient = DataMiningClient()
        pass

    def post(self, request, format=None):
        
        try:
            # Start data mining client
            self.DataMiningClient.startConnection()
            
            # Get selected arch id's
            selected = request.POST['selected']
            selected = selected[1:-1]
            selected_arch_ids = selected.split(',')
            
            # Convert strings to ints
            behavioral = []
            for s in selected_arch_ids:
                behavioral.append(int(s))

            # Get non-selected arch id's
            non_selected = request.POST['non_selected']
            non_selected = non_selected[1:-1]
            non_selected_arch_ids = non_selected.split(',')
            # Convert strings to ints
            non_behavioral = []
            for s in non_selected_arch_ids:
                non_behavioral.append(int(s))

            # Load architecture data from the session info
            logger.debug(request.session)
            architectures = request.session['data']

            problem = request.POST['problem']
            inputType = request.POST['input_type']

            drivingFeatures = self.DataMiningClient.getDrivingFeaturesWithGeneralization(problem, inputType, behavioral, non_behavioral, architectures)
            output = drivingFeatures

            # End the connection before return statement
            self.DataMiningClient.endConnection() 
            return Response(output)
        
        except Exception as detail:
            logger.exception('Exception in getDrivingFeatures: ' + str(detail))
            self.DataMiningClient.endConnection()
            return Response('')
        
# Create your views here.
class GetDrivingFeaturesAutomated(APIView):

    def __init__(self):
        self.DataMiningClient = DataMiningClient()
        pass

    def post(self, request, format=None):
        
        try:
            # Start data mining client
            self.DataMiningClient.startConnection()
            
            # Get threshold values for the metrics
            supp = float(request.POST['supp'])
            conf = float(request.POST['conf'])
            lift = float(request.POST['lift'])
            
            # Get selected arch id's
            selected = request.POST['selected']
            selected = selected[1:-1]
            selected_arch_ids = selected.split(',')
            # Convert strings to ints
            behavioral = []
            for s in selected_arch_ids:
                behavioral.append(int(s))

            # Get non-selected arch id's
            non_selected = request.POST['non_selected']
            non_selected = non_selected[1:-1]
            non_selected_arch_ids = non_selected.split(',')
            # Convert strings to ints
            non_behavioral = []
            for s in non_selected_arch_ids:
                non_behavioral.append(int(s))

            # Load architecture data from the session info
            logger.debug(request.session)
            architectures = request.session['data']

            problem = request.POST['problem']
            inputType = request.POST['input_type']

            drivingFeatures = self.DataMiningClient.getDrivingFeaturesAutomated(problem, inputType, behavioral, non_behavioral,
                                                                       architectures, supp, conf, lift)
                
            output = drivingFeatures

            # End the connection before return statement
            self.DataMiningClient.endConnection() 
            return Response(output)
        
        except Exception as detail:
            logger.exception('Exception in getDrivingFeatures: ' + str(detail))
            self.DataMiningClient.endConnection()
            return Response('')
        
class GetMarginalDrivingFeatures(APIView):

    def __init__(self):
        self.DataMiningClient = DataMiningClient()
        pass

    def post(self, request, format=None):
        
        try:
            # Start data mining client
            self.DataMiningClient.startConnection()
            
            # Get threshold values for the metrics
            supp = float(request.POST['supp'])
            conf = float(request.POST['conf'])
            lift = float(request.POST['lift'])
            
            # Get selected arch id's
            behavioral = json.loads(request.POST['selected'])
            non_behavioral = json.loads(request.POST['non_selected'])
                
            featureExpression = request.POST['featureExpression']      
            logicalConnective = request.POST['logical_connective']      

            # Load architecture data from the session info
            architectures = request.session['data']

            problem = request.POST['problem']
            inputType = request.POST['input_type']

            drivingFeatures = self.DataMiningClient.getMarginalDrivingFeatures(problem, inputType, behavioral,non_behavioral,architectures,
                                                                               featureExpression,logicalConnective, supp,conf,lift)            
            output = drivingFeatures

            # End the connection before return statement
            self.DataMiningClient.endConnection() 
            return Response(output)
        
        except Exception as detail:
            logger.exception('Exception in getDrivingFeatures: ' + detail)
            self.DataMiningClient.endConnection()
            return Response('')

class ClusterData(APIView):

    def __init__(self):
        pass

    def post(self, request, format=None):
        
        try:

            param = int(request.POST['param'])

            problem = request.POST['problem']
            inputType = request.POST['input_type']

            # Get selected arch id's
            selected = request.POST['selected']
            selected = selected[1:-1]
            selected_arch_ids = selected.split(',')
            # Convert strings to ints
            behavioral = []
            for s in selected_arch_ids:
                behavioral.append(int(s))

            # Get non-selected arch id's
            non_selected = request.POST['non_selected']
            non_selected = non_selected[1:-1]
            non_selected_arch_ids = non_selected.split(',')
            # Convert strings to ints
            non_behavioral = []
            for s in non_selected_arch_ids:
                non_behavioral.append(int(s))

            # Load architecture data from the session info
            architectures = request.session['data']

            data = []
            for arch in architectures:
                if arch['id'] in behavioral:
                    data.append(arch['outputs'])
                else:
                    pass

            id_list = behavioral

            # dir_path = os.path.dirname(os.path.realpath(__file__))
            # with open(os.path.join(dir_path,"data.csv"), "w") as file:

            #     for i, row in enumerate(data):
            #         out = []
            #         out.append(str(id_list[i]))

            #         for val in row:
            #             out.append(str(val))
            #         out = ",".join(out)
            #         file.write(out + "\n")

            from cluster import Clustering
            
            clustering = Clustering(data)

            labels = clustering.kMeans(param)

            out = {
                "id": id_list,
                "labels": labels
            }
            
            return Response(out)
        
        except Exception as detail:
            logger.exception('Exception in clustering: ' + str(detail))
            return Response('')
    

class GetCluster(APIView):

    def __init__(self):
        pass

    def post(self, request, format=None):
        try:

            dir_path = os.path.dirname(os.path.realpath(__file__))
            labels = []
            id_list = []

            with open(os.path.join(dir_path,"labels.csv"), "r") as file:

                content = file.read().split("\n")

                for row in content:
                    if row == "":
                        continue
                    elif "," in row:
                        id_list.append(row.split(",")[0])
                        labels.append(row.split(",")[1])
                    else:
                        labels.append(row)

            out = {
                "id": id_list,
                "labels": labels
            }
            return Response(out)
        
        except Exception as detail:
            logger.exception('Exception in getting cluster labels: ' + str(detail))
            return Response('')        

class ConvertToDNF(APIView):

    def __init__(self):
        self.DataMiningClient = DataMiningClient()
        pass

    def post(self, request, format=None):
        try:
            # Start data mining client
            self.DataMiningClient.startConnection()
            
            # Get the expression
            expression = request.POST['expression']
            dnf_expression = self.DataMiningClient.convertToDNF(expression)

            # End the connection before return statement
            self.DataMiningClient.endConnection() 
            return Response(dnf_expression)
        
        except Exception as detail:
            logger.exception('Exception in convertingToDNF: ' + str(detail))
            self.DataMiningClient.endConnection()
            return Response('')
        
class ConvertToCNF(APIView):

    def __init__(self):
        self.DataMiningClient = DataMiningClient()
        pass

    def post(self, request, format=None):
        try:
            # Start data mining client
            self.DataMiningClient.startConnection()
            
            # Get the expression
            expression = request.POST['expression']
            cnf_expression = self.DataMiningClient.convertToCNF(expression)

            # End the connection before return statement
            self.DataMiningClient.endConnection() 
            return Response(cnf_expression)
        
        except Exception as detail:
            logger.exception('Exception in convertingToCNF: ' + str(detail))
            self.DataMiningClient.endConnection()
            return Response('')

class ComputeTypicality(APIView):

    def __init__(self):
        self.DataMiningClient = DataMiningClient()
        pass

    def post(self, request, format=None):
        try:
            # Start data mining client
            self.DataMiningClient.startConnection()

            # Get selected arch id's
            inputString = request.POST['input']
            inputString = inputString[1:-1]
            inputSplit = inputString.split(',')

            # Convert strings to ints
            inputs = []
            for i in inputSplit:
                inputs.append(int(i))

            # Get the expression
            expression = request.POST['expression']
            typicality = self.DataMiningClient.computeTypicality(inputs, expression)

            # End the connection before return statement
            self.DataMiningClient.endConnection() 
            return Response(typicality)
        
        except Exception as detail:
            logger.exception('Exception in ComputeComplexity: ' + str(detail))
            self.DataMiningClient.endConnection()
            return Response('')

class ComputeComplexity(APIView):

    def __init__(self):
        self.DataMiningClient = DataMiningClient()
        pass

    def post(self, request, format=None):
        try:
            # Start data mining client
            self.DataMiningClient.startConnection()
            
            # Get the expression
            expression = request.POST['expression']
            complexity = self.DataMiningClient.computeComplexity(expression)

            # End the connection before return statement
            self.DataMiningClient.endConnection() 
            return Response(complexity)
        
        except Exception as detail:
            logger.exception('Exception in ComputeComplexity: ' + str(detail))
            self.DataMiningClient.endConnection()
            return Response('')

class ComputeComplexityOfFeatures(APIView):

    def __init__(self):
        self.DataMiningClient = DataMiningClient()
        pass

    def post(self, request, format=None):
        try:
            # Start data mining client
            self.DataMiningClient.startConnection()
            
            # Get the expression
            expressions = request.POST['expressions']
            expressions = json.loads(expressions)

            complexity = self.DataMiningClient.computeComplexityOfFeatures(expressions)

            # End the connection before return statement
            self.DataMiningClient.endConnection() 
            return Response(complexity)
        
        except Exception as detail:
            logger.exception('Exception in ComputeComplexityOfFeatures: ' + str(detail))
            self.DataMiningClient.endConnection()
            return Response('')

class GetProblemParameters(APIView):

    def __init__(self):
        self.DataMiningClient = DataMiningClient()
        pass

    def post(self, request, format=None):
        try:
            # Start data mining client
            self.DataMiningClient.startConnection()
            
            problem = request.POST['problem']
            params = self.DataMiningClient.getProblemParameters(problem)

            # End the connection before return statement
            self.DataMiningClient.endConnection() 
            return Response(params)
        
        except Exception as detail:
            logger.exception('Exception in GetProblemParameters: ' + str(detail))
            self.DataMiningClient.endConnection()
            return Response('')

class SetProblemParameters(APIView):

    def __init__(self):
        self.DataMiningClient = DataMiningClient()
        pass

    def post(self, request, format=None):
        try:
            # Start data mining client
            self.DataMiningClient.startConnection()
            
            problem = request.POST['problem']
            params = json.loads(request.POST['params'])
            self.DataMiningClient.setProblemParameters(problem, params)

            # End the connection before return statement
            self.DataMiningClient.endConnection() 
            return Response()
        
        except Exception as detail:
            logger.exception('Exception in ComputeComplexityOfFeatures: ' + str(detail))
            self.DataMiningClient.endConnection()
            return Response('')

class getTaxonomicScheme(APIView):

    def __init__(self):
        self.DataMiningClient = DataMiningClient()

    def post(self, request, format=None):
        try:
            # Start data mining client
            self.DataMiningClient.startConnection()
            
            problem = request.POST['problem']
            taxonomicScheme = self.DataMiningClient.getTaxonomicScheme(problem)

            # End the connection before return statement
            self.DataMiningClient.endConnection() 
            return Response(taxonomicScheme)
        
        except Exception as detail:
            logger.exception('Exception in ComputeComplexityOfFeatures: ' + str(detail))
            self.DataMiningClient.endConnection()
            return Response('')

def booleanArray2booleanString(booleanArray):
    leng = len(booleanArray)
    boolString = ''
    for i in range(leng):
        if booleanArray[i] == True:
            boolString += '1'
        else:
            boolString += '0'
    return boolString
