import logging

from rest_framework.views import APIView
from rest_framework.response import Response
import json


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






# --> Will return information on the Features subject
# --> We will need a DataMiningClient, used in analyst/views.py
class GetSubjectFeatures(APIView):
    def post(self, request, format=None):
        test_data = request.data['fricken_key']
        print(test_data)
        return Response({'list': 'test'})











# --> Will return information on the Sensitivities subject --> Ask Samalis
# --> We will need a DataMiningClient, used in analyst/views.py
class GetSubjectSensitivities(APIView):
    def post(self, request, format=None):
        print("Getting Subject Sensitivities!!!")
        sensitivities_client = SensitivitiesClient()

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

        # --> Call the Sensitivity Service API
        results = False
        if problem in assignation_problems:
            print("Assignation Problem")
            results = sensitivities_client.assignation_sensitivities(arch_dict_list, orbits, instruments)
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
        return Response({'list': 'test'})





# --> Will return information on the Design Space subject
# --> Call VASSAR
class GetSubjectDesignSpace(APIView):
    def post(self, request, format=None):
        return Response({'list': 'test'})




