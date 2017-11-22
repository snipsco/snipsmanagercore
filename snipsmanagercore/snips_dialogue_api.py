# -*-: coding utf-8 -*-
""" Helper class for dialogue api calls. """

HERMES_START_SESSION = "hermes/dialogueManager/startSession"
HERMES_END_SESSION = "hermes/dialogueManager/endSession"
HERMES_CONTINUE_SESSION = "hermes/dialogueManager/continueSession"

class SnipsDialogueAPI:

	def __init__(self, client):
		self.client = client

	def start_session(self, customData=None, siteId="default"):
		payload = {"siteId": siteId, "init": None, "customData": customData}
		self.client.publish(HERMES_START_SESSION, payload=payload, qos=0, retain=False)

	def start_action(self, ttsContent, canBeEnqueued, intentFilter, customData=None, siteId="default"):
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

		self.client.publish(HERMES_START_SESSION, payload=payload, qos=0, retain=False)

	def start_notification(self, ttsContent, siteId = "default", customData=None):
		action = {
			"type": "notification",
			"text": ttsContent,
		}

		payload = {
			"siteId": siteId,
			"init": action,
			"customData": customData
		}

		self.client.publish(HERMES_START_SESSION, payload=payload, qos=0, retain=False)

	def end_session(self, sessionId, ttsContent):
		payload = {
			"sessionId": sessionId,
			"text": ttsContent,
		}

		self.client.publish(HERMES_END_SESSION, payload=payload, qos=0, retain=False)

	def continue_session(self, sessionId, ttsContent, intentFilter):
		payload = {
			"sessionId": sessionId,
			"text": ttsContent,
			"intentFilter": intentFilter
		}
		self.client.publish(HERMES_CONTINUE_SESSION, payload=payload, qos=0, retain=False)

	# aliases 
	tts = end_session
	speak = end_session
