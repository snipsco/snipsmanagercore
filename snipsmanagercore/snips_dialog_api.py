# -*-: coding utf-8 -*-
""" Helper class for dialogue api calls. """

HERMES_START_SESSION = "hermes/dialogueManager/startSession"
HERMES_END_SESSION = "hermes/dialogueManager/endSession"
HERMES_CONTINUE_SESSION = "hermes/dialogueManager/continueSession"

from tts import GTTS
import json


class SnipsDialogAPI:

    def __init__(self, client, tts_service_id, locale="en_US"):
        self.client = client
        self.gtts = GTTS(locale)
        self.tts_method = None

        # aliases
        if tts_service_id is None or (
                type(tts_service_id) is str and tts_service_id.decode('utf-8').lower() == "snips"):
            self.tts_method = self.end_session
        elif (type(tts_service_id) is str and tts_service_id.decode('utf-8').lower() == "google"):
            self.tts_method = self.google_end_session

    def speak(self, tts_content, session_id=None):
        if (self.tts_method is not None):
            self.tts_method(tts_content, session_id)

    def google_end_session(self, tts_content, session_id=None):
        self.gtts.speak(tts_content)
        self.end_session(None, session_id)

    def start_session(self, custom_data=None, site_id="default"):
        payload = {"siteId": site_id, "init": None, "customData": custom_data}
        self.client.publish(HERMES_START_SESSION, payload=json.dumps(payload), qos=0, retain=False)

    def start_action(self, tts_content, can_be_enqueued, intent_filter=[], custom_data=None, site_id="default"):
        action = {
            "type": "action",
            "text": tts_content,
            "canBeEnqueued": can_be_enqueued,
            "intentFilter": intent_filter
        }

        payload = {
            "siteId": site_id,
            "init": action,
            "customData": custom_data
        }

        self.client.publish(HERMES_START_SESSION, payload=json.dumps(payload), qos=0, retain=False)

    def start_notification(self, tts_content, site_id="default", custom_data=None):
        action = {
            "type": "notification",
            "text": tts_content,
        }

        payload = {
            "siteId": site_id,
            "init": action,
            "customData": custom_data
        }

        self.client.publish(HERMES_START_SESSION, payload=json.dumps(payload), qos=0, retain=False)

    def end_session(self, tts_content, session_id):
        if session_id is None:
            raise SessionIdError

        payload = {
            "sessionId": session_id,
            "text": tts_content
        }
        self.client.publish(HERMES_END_SESSION, payload=json.dumps(payload), qos=0, retain=False)

    def continue_session(self, tts_content, session_id, intent_filter=[]):
        if session_id is None:
            raise SessionIdError

        payload = {
            "sessionId": session_id,
            "text": tts_content,
            "intentFilter": intent_filter
        }
        self.client.publish(HERMES_CONTINUE_SESSION, payload=json.dumps(payload), qos=0, retain=False)

class DialogError(Exception):
    pass

class SessionIdError(DialogError):
    pass
