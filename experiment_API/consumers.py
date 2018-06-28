import datetime
import json
from channels.generic.websocket import JsonWebsocketConsumer
from django.conf import settings
from importlib import import_module


class ExperimentConsumer(JsonWebsocketConsumer):
    ##### WebSocket event handlers
    def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        # Accept the connection
        self.accept()

    def receive_json(self, content, **kwargs):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """

        # Get an updated session store
        session_key = self.scope["cookies"].get(settings.SESSION_COOKIE_NAME)
        self.scope["session"] = import_module(settings.SESSION_ENGINE).SessionStore(session_key)

        if content.get('msg_type') == 'add_action':
            action = content['action']
            action['date'] = datetime.datetime.utcnow().isoformat()
            self.scope['session']['experiment']['stages'][content['stage']]['actions'].append(action)
            self.scope['session'].save()
            self.send(json.dumps(self.scope['session']['experiment']))
        elif content.get('msg_type') == 'update_state':
            self.scope['session']['experiment']['state'] = content['state']
            self.scope['session'].save()
            self.send(json.dumps(self.scope['session']['experiment']))
