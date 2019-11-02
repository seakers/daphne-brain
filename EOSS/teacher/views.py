import logging

from rest_framework.views import APIView
from rest_framework.response import Response
import json
from time import sleep

import threading
from queue import Queue
from channels.layers import get_channel_layer

from EOSS.data.problem_specific import assignation_problems, partition_problems
from EOSS.vassar.api import VASSARClient
from auth_API.helpers import get_or_create_user_information
from EOSS.data.design_helpers import add_design

# --> Import VASSAR Service, Sensitivities Service
from EOSS.sensitivities.api import SensitivitiesClient
from EOSS.vassar.api import VASSARClient
from EOSS.models import EOSSContext, Design

# --> Import the user information so we can get the architectures
from auth_API.helpers import get_or_create_user_information

# --> Import the problem types
from EOSS.data.problem_specific import assignation_problems, partition_problems

from EOSS.explorer.design_space_evaluator import evaluate_design_space_level_one
from EOSS.explorer.design_space_evaluator import evaluate_design_space_level_two

from EOSS.explorer.objective_space_evaluator import teacher_evaluate_objective_space

from .teacher_agent import teacher_thread

from EOSS.models import ArchitecturesEvaluated, ArchitecturesUpdated, ArchitecturesClicked



class ClearTeacherUserData(APIView):
    def post(self, request, format=None):
        user_info = get_or_create_user_information(request.session, request.user, 'EOSS')
        ArchitecturesClicked.objects.all().filter(user_information=user_info).delete()
        ArchitecturesUpdated.objects.all().filter(user_information=user_info).delete()
        ArchitecturesEvaluated.objects.all().filter(user_information=user_info).delete()
        return Response({'list': 'test'})



class SetProactiveMode(APIView):
    # --> For each current session, we will have a teacher object as long as that session
    # has a teacher agent window open with "Proactive" set to true...
    # --> This teacher object will be a thread running a proactive teacher
    # --> Later, if the user is registered, the teacher agent will pull that user's ability parameter from a database
    teachersDict = {}

    def post(self, request, format=None):

        # --> Get Daphne user information
        user_info = get_or_create_user_information(request.session, request.user, 'EOSS')
        print("\n--> USER INFO", user_info.session, user_info.user)


        # --> Get the Problem Name
        problem = request.data['problem']

        # --> Get the channel layer
        channel_layer = get_channel_layer()

        # --> Determine the setting for Proactive Mode
        mode = request.data['proactiveMode']

        # --> Proactive Mode: enabled - create a teacher for this session
        if mode == 'enabled':
            print('--> Teacher request')
            if user_info.session not in self.teachersDict:
                print("--> Request approved for", user_info.session)
                communication_queue = Queue()
                user_thread = threading.Thread(target=teacher_thread,
                                               args=(request, communication_queue,
                                                     user_info,
                                                     channel_layer))
                user_thread.start()
                sleep(0.1)
                self.teachersDict[user_info.session] = (user_thread, communication_queue)
            else:
                print('--> Request denied, Teacher already assigned')

        # --> Proactive Mode: disabled - remove a teacher for this session
        elif mode == 'disabled':
            print('--> Teacher request')
            if user_info.session in self.teachersDict:
                print("--> Request approved")
                thread_to_join = (self.teachersDict[user_info.session])[0]
                communication_queue = (self.teachersDict[user_info.session])[1]
                communication_queue.put('stop fam')
                thread_to_join.join()
                del self.teachersDict[user_info.session]
                print("Thread Killed")
            else:
                print('--> Request denied, no teacher to return')


        print('\n')
        print("Teachers Online", self.teachersDict, "\n")
        return Response({'list': 'test'})


# --> Will return information on the Features subject
# --> We will need a DataMiningClient, used in analyst/views.py
class GetSubjectFeatures(APIView):
    def post(self, request, format=None):
        return Response({'list': 'test'})


# --> Will return information on the Design Space subject
# --> Call VASSAR
class GetSubjectDesignSpace(APIView):
    def post(self, request, format=None):
        print("Getting Subject DesignSpace!!!")

        # --> Get Daphne user information
        user_info = get_or_create_user_information(request.session, request.user, 'EOSS')

        # --> Get the Problem Name
        problem = request.data['problem']

        # --> Get the Problem Orbits
        orbits = request.data['orbits']
        orbits = orbits[1:-1]
        orbits = orbits.split(',')
        for x in range(0, len(orbits)):
            orbits[x] = (orbits[x])[1:-1]

        # --> Get the Problem Instruments
        instruments = request.data['instruments']
        instruments = instruments[1:-1]
        instruments = instruments.split(',')
        for x in range(0, len(instruments)):
            instruments[x] = (instruments[x])[1:-1]

        # --> Get all the architectures that daphne is considering right now
        arch_dict_list = []
        for arch in user_info.eosscontext.design_set.all():
            temp_dict = {'id': arch.id, 'inputs': json.loads(arch.inputs), 'outputs': json.loads(arch.outputs)}
            arch_dict_list.append(temp_dict)

        # --> Call the Design Space Evaluator Service API
        level_one_analysis = evaluate_design_space_level_one(arch_dict_list, orbits, instruments)
        level_two_analysis = evaluate_design_space_level_two(arch_dict_list, orbits, instruments)

        print("Level 1", level_one_analysis)
        for key in level_two_analysis:
            print("Level 2", level_two_analysis[key])

        return Response({'level_one_analysis': level_one_analysis, 'level_two_analysis': level_two_analysis})


# --> Will return information on the Sensitivities subject --> Ask Samalis
# --> We will need a DataMiningClient, used in analyst/views.py
class GetSubjectSensitivities(APIView):
    def post(self, request, format=None):
        print("Getting Subject Sensitivities!!!")
        sensitivities_client = SensitivitiesClient()

        # --> Get Daphne user information
        user_info = get_or_create_user_information(request.session, request.user, 'EOSS')

        # Start connection with VASSAR
        port = user_info.eosscontext.vassar_port

        # --> Get the Problem Name
        # problem = request.data['problem']
        problem = user_info.eosscontext.problem

        # --> Get the Problem Orbits
        orbits = request.data['orbits']
        orbits = orbits[1:-1]
        orbits = orbits.split(',')
        for x in range(0, len(orbits)):
            orbits[x] = (orbits[x])[1:-1]

        # --> Get the Problem Instruments
        instruments = request.data['instruments']
        instruments = instruments[1:-1]
        instruments = instruments.split(',')
        for x in range(0, len(instruments)):
            instruments[x] = (instruments[x])[1:-1]

        # --> Get all the architectures that daphne is considering right now
        arch_dict_list = []
        for arch in user_info.eosscontext.design_set.all():
            temp_dict = {'id': arch.id, 'inputs': json.loads(arch.inputs), 'outputs': json.loads(arch.outputs)}
            arch_dict_list.append(temp_dict)

        # --> Call the Sensitivity Service API
        results = False
        if problem in assignation_problems:
            print("Assignation Problem")
            results = sensitivities_client.assignation_sensitivities(arch_dict_list, orbits, instruments, port, problem)
        elif problem in partition_problems:
            print("Partition Problem")
            results = sensitivities_client.partition_sensitivities(arch_dict_list, orbits, instruments)
        else:
            raise ValueError('Unrecognized problem type: {0}'.format(problem))

        return Response(results)


# --> Will return information on the Objective Space subject
# --> Call VASSAR
class GetSubjectObjectiveSpace(APIView):
    def post(self, request, format=None):
        print("Getting Objective Space Information!!!")

        # --> Get Daphne user information
        user_info = get_or_create_user_information(request.session, request.user, 'EOSS')

        # --> Get the Problem Name
        problem = request.data['problem']

        # --> Get the Problem Orbits
        orbits = request.data['orbits']
        orbits = orbits[1:-1]
        orbits = orbits.split(',')
        for x in range(0, len(orbits)):
            orbits[x] = (orbits[x])[1:-1]

        # --> Get the Problem Instruments
        instruments = request.data['instruments']
        instruments = instruments[1:-1]
        instruments = instruments.split(',')
        for x in range(0, len(instruments)):
            instruments[x] = (instruments[x])[1:-1]

        plotData = request.data['plotData']
        plotDataJson = json.loads(plotData)

        objectiveSpaceInformation = teacher_evaluate_objective_space(plotDataJson)
        return_data = json.dumps(objectiveSpaceInformation)

        return Response(return_data)


class GetObjectiveGroupInformation(APIView):
    def post(self, request, format=None):
        print("Getting Objective Group Information!!!")

        # --> Get Daphne user information
        user_info = get_or_create_user_information(request.session, request.user, 'EOSS')

        # # --> Connect to VASSAR
        # port = user_info.eosscontext.vassar_port
        # client = VASSARClient(port)
        # client.start_connection()

        # --> Get the Problem Name
        problem = request.data['problem']

        groupData = request.data['groupData']
        groupData = json.loads(groupData)
        print(groupData)

        # --> VASSAR local search will take a list of bools

        return Response({})
