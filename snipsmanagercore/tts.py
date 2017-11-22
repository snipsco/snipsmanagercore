# # -*-: coding utf-8 -*-
# """ Wrapper for various TTS services (currently only Google). """

# import json
# import os
# import time

# import paho.mqtt.client as mqtt

# from socket import error as socket_error
# from gtts import gTTS

# from .audio_player import AudioPlayer

# class SnipsTTS:

#     MQTT_TOPIC_DIALOG = "hermes/dialogueManager/"

#     """ Snips TTS service. """

#     def __init__(self, thread_handler, mqtt_hostname, mqtt_port, locale, logger=None):
#         """ Initialise the service.

#         :param mqtt_hostname: the MQTT broker hostname.
#         :param mqtt_port: the MQTT broker port.
#         :param mqtt_topic: the topic on which to post the sentence.
#         :param locale: the language locale, e.g. "fr" or "en_US".
#         """

#         self.logger = logger
#         self.locale = locale.split("_")[0]

#         self.mqtt_topic = "hermes/dialogueManager/{}".format(dialog_action)
#         self.mqtt_client = mqtt.Client("SnipsTTS")
        
#         thread_handler.run(target=self.start_blocking, args=(mqtt_hostname, mqtt_port, ))

#     def start_blocking(self, mqtt_hostname, mqtt_port, run_event):
#         while True and run_event.is_set():
#             try:
#                 self.mqtt_client.connect(mqtt_hostname, mqtt_port)
#                 break
#             except (socket_error, Exception) as e:
#                 time.sleep(5)

#     def speak(self, sentence, session_id, dialog_action="end", site_id="default"):
#         """ Speak a sentence using Snips TTS.

#         :param sentence: the sentence to speak.
#         """
#         init = {
#             "type": "action",
#             "text": sentence,
#             "canBeEnqueued": 
#         }
#         if (dialog_action == "notification"):
#             topic = "{}/startSession".format(MQTT_TOPIC_DIALOG)
#             init = {
#                 "type": "notification",
#                 "text": sentence
#             }
#             load = {
#                 "init": init,
#                 "siteId": site_id,
#                 "customData": None
#             }
#         elif (dialog_action == "end"):
#             topic = "{}/endSession".format(MQTT_TOPIC_DIALOG)
#             load = {
#                 "sessionId": session_id,
#                 "text": sentence
#             }
#         elif (dialog_action == "continue"):
#             topic = "{}/continueSession".format(MQTT_TOPIC_DIALOG)
#             load = 

#         if self.mqtt_client is None:
#             return

#         if self.logger is not None:
#             self.logger.info("Snips TTS: {}".format(sentence))


#         self.mqtt_client.publish(
#             self.mqtt_topic,
#             payload=json.dumps({'text': sentence}),
#             qos=0,
#             retain=False)