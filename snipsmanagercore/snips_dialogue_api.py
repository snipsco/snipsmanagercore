# -*-: coding utf-8 -*-
""" Helper class for dialogue api calls. """

HERMES_START_SESSION = "hermes/dialogueManager/startSession"
HERMES_END_SESSION = "hermes/dialogueManager/endSession"
HERMES_CONTINUE_SESSION = "hermes/dialogueManager/continueSession"

from tts import GTTS
import json

class SnipsDialogueAPI:

	sessionId = None
	siteId = "default"

	def __init__(self, client, tts_service_id, locale="en_US"):
		self.client = client
		self.gtts = GTTS(locale)
		self.tts_method = None

		# aliases 
		if tts_service_id is None or (type(tts_service_id) is str and tts_service_id.decode('utf-8').lower() == "snips"):
			self.tts_method = self.end_session
		elif tts_service_id is (type(tts_service_id) is str and tts_service_id.decode('utf-8').lower() == "google"):
			self.tts_method = self.google_end_session

	def speak(self, ttsContent, sessionId=None):
		if (self.tts_method is not None):
			self.tts_method(ttsContent, sessionId)


	def google_end_session(self, ttsContent, sessionId=None):
		self.gtts.speak(ttsContent)
		self.end_session(None, sessionId)

	def start_session(self, customData=None, siteId="default"):
		payload = {"siteId": siteId, "init": None, "customData": customData}
		self.client.publish(HERMES_START_SESSION, payload=json.dumps(payload), qos=0, retain=False)

	def start_action(self, ttsContent, canBeEnqueued, intentFilter=[], customData=None, siteId="default"):
		action = {
			"type": "action",
			"text": ttsContent,
			"canBeEnqueued": canBeEnqueued,
			"intentFilter": intentFilter
		}

		payload = {
			"siteId": siteId,
			"init": action,
			"customData": customData
		}

		self.client.publish(HERMES_START_SESSION, payload=json.dumps(payload), qos=0, retain=False)

	def start_notification(self, ttsContent, siteId="default", customData=None):
		action = {
			"type": "notification",
			"text": ttsContent,
		}

		payload = {
			"siteId": siteId,
			"init": action,
			"customData": customData
		}

		self.client.publish(HERMES_START_SESSION, payload=json.dumps(payload), qos=0, retain=False)

	def end_session(self, ttsContent, sessionId=None):
		if(sessionId is None and self.sessionId is not None):
			sessionId = self.sessionId

		payload = {
			"sessionId": sessionId,
			"text": ttsContent
		}
		self.client.publish(HERMES_END_SESSION, payload=json.dumps(payload), qos=0, retain=False)

	def continue_session(self, ttsContent, intentFilter=[], sessionId=None):
		if(sessionId is None and self.sessionId is not None):
			sessionId = self.sessionId

		payload = {
			"sessionId": sessionId,
			"text": ttsContent,
			"intentFilter": intentFilter
		}
		self.client.publish(HERMES_CONTINUE_SESSION, payload=json.dumps(payload), qos=0, retain=False)
