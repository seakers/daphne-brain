import logging
import os
import json
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from auth_API.helpers import get_or_create_user_information
from daphne_API.models import ExperimentStage


# Get an instance of a logger
logger = logging.getLogger('experiment')


def stage_type(id, stage_num):
    if id % 2 == 0:
        if stage_num == 0:
            return 'daphne_assistant'
        else:
            return 'daphne_peer'
    else:
        if stage_num == 0:
            return 'daphne_peer'
        else:
            return 'daphne_assistant'


# Create your views here.
class StartExperiment(APIView):

    def get(self, request, format=None):

        # Check for experiments folder
        results_dir = './experiment_API/results'
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Obtain ID number
        new_id = len(os.listdir(results_dir))

        # Create File so ID does not get repeated
        open(os.path.join(results_dir, str(new_id) + '.json'), 'w')

        # Save experiment start info
        user_info = get_or_create_user_information(request.session, request.user, 'EOSS')
        experiment_context = user_info.eosscontext.experimentcontext

        experiment_context.experiment_id = new_id

        # Specific to current experiment
        ExperimentStage.objects.create(experimentcontext=experiment_context, type=stage_type(new_id, 0))
        ExperimentStage.objects.create(experimentcontext=experiment_context, type=stage_type(new_id, 1))

        # Save experiment started on database
        experiment_context.is_running = True

        experiment_context.save()

        # Prepare return for client
        experiment_stages = []
        for stage in experiment_context.experimentstage_set.all():
            experiment_stages.append(stage.type)

        return Response(experiment_stages)


class StartStage(APIView):

    def get(self, request, stage, format=None):
        user_info = get_or_create_user_information(request.session, request.user, 'EOSS')
        experiment_context = user_info.eosscontext.experimentcontext
        experiment_stage = experiment_context.experimentstage_set.all()[stage]
        experiment_stage.start_date = datetime.datetime.utcnow()
        experiment_stage.save()

        return Response({
            'start_date': experiment_stage.start_date
        })


class FinishStage(APIView):

    def get(self, request, stage, format=None):
        user_info = get_or_create_user_information(request.session, request.user, 'EOSS')
        experiment_context = user_info.eosscontext.experimentcontext
        experiment_stage = experiment_context.experimentstage_set.all()[stage]
        experiment_stage.end_date = datetime.datetime.utcnow()
        experiment_stage.end_state = experiment_context.current_state
        experiment_stage.save()

        return Response({
            'end_date': experiment_stage.end_date
        })


class ReloadExperiment(APIView):

    def get(self, request, format=None):
        user_info = get_or_create_user_information(request.session, request.user, 'EOSS')
        experiment_context = user_info.eosscontext.experimentcontext

        if experiment_context.is_running:
            return Response({ 'is_running': True, 'experiment_data': json.loads(experiment_context.current_state) })
        else:
            return Response({ 'is_running': False })
        
        
class FinishExperiment(APIView):

    def get(self, request, format=None):
        user_info = get_or_create_user_information(request.session, request.user, 'EOSS')
        experiment_context = user_info.eosscontext.experimentcontext

        # Save experiment results to file
        with open('./experiment_API/results/' + str(experiment_context.experiment_id) + '.json', 'w') as f:
            json_experiment = {
                "experiment_id": experiment_context.experiment_id,
                "current_state": experiment_context.current_state,
                "stages": []
            }
            for stage in experiment_context.experimentstage_set.all():
                json_stage = {
                    "type": stage.type,
                    "start_date": stage.start_date,
                    "end_date": stage.end_date,
                    "end_state": stage.end_state,
                    "actions": []
                }
                for action in stage.experimentaction_set.all():
                    json_action = {
                        "action": action.action,
                        "date": action.date
                    }
                    json_stage["actions"].append(json_action)
                json_experiment["stages"].append(json_stage)
            json.dump(json_experiment, f)

        experiment_context.delete()

        return Response('Experiment finished correctly!')
