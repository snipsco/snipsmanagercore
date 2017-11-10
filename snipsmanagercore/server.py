# -*-: coding utf-8 -*-
""" Snips core server. """

import json
import time
import re

from socket import error as socket_error

import paho.mqtt.client as mqtt

from .thread_handler import ThreadHandler
from .intent_parser import IntentParser
from .state_handler import StateHandler, State
from .tts import SnipsTTS, GTTS

HOTWORD_DETECTED_RE = re.compile("^hermes\/hotword(\/[a-zA-Z0-9]+)*\/detected$")

class Server():
    """ Snips core server. """

    def __init__(self,
                 mqtt_hostname,
                 mqtt_port,
                 tts_service_id,
                 locale,
                 registry,
                 handle_intent,
                 handle_start_listening = None,
                 handle_done_listening = None,
                 logger=None):
        """ Initialisation.

        :param config: a YAML configuration.
        :param assistant: the client assistant class, holding the
                          intent handler and intents registry.
        """
        self.logger = logger
        self.registry = registry
        self.handle_intent = handle_intent
        self.handle_start_listening = handle_start_listening
        self.handle_done_listening = handle_done_listening
        self.thread_handler = ThreadHandler()
        self.state_handler = StateHandler(self.thread_handler)

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.mqtt_hostname = mqtt_hostname
        self.mqtt_port = mqtt_port

        if tts_service_id == "google":
            self.tts_service = GTTS(locale, logger=self.logger)
        else:
            self.tts_service = SnipsTTS(
                self.thread_handler,
                mqtt_hostname,
                mqtt_port,
                "hermes/tts/say",
                locale,
                logger=self.logger)

        self.first_hotword_detected = False

    def start(self):
        """ Start the MQTT client. """
        self.thread_handler.run(target=self.start_blocking)
        self.thread_handler.start_run_loop()

    def start_blocking(self, run_event):
        """ Start the MQTT client, as a blocking method.

        :param run_event: a run event object provided by the thread handler.
        """
        topics = [("hermes/intent/#",0), ("hermes/hotword/#", 0), ("hermes/asr/#", 0), ("snipsmanager/#", 0)]

        self.log_info("Connecting to {} on port {}".format(self.mqtt_hostname, str(self.mqtt_port)))

        retry = 0
        while True and run_event.is_set():
            try:
                self.log_info("Trying to connect to {}".format(self.mqtt_hostname))
                self.client.connect(self.mqtt_hostname, self.mqtt_port, 60)
                break
            except (socket_error, Exception) as e:
                self.log_info("MQTT error {}".format(e))
                time.sleep(5 + int(retry / 5))
                retry = retry + 1
        self.client.subscribe(topics)
        while run_event.is_set():
            try:
                self.client.loop()
            except AttributeError as e:
                self.log_info("Error in mqtt run loop {}".format(e))
                time.sleep(1)

    # pylint: disable=unused-argument,no-self-use
    def on_connect(self, client, userdata, flags, result_code):
        """ Callback when the MQTT client is connected.

        :param client: the client being connected.
        :param userdata: unused.
        :param flags: unused.
        :param result_code: result code.
        """
        self.log_info("Connected with result code {}".format(result_code))
        self.state_handler.set_state(State.welcome)

    # pylint: disable=unused-argument
    def on_disconnect(self, client, userdata, result_code):
        """ Callback when the MQTT client is disconnected. In this case,
            the server waits five seconds before trying to reconnected.

        :param client: the client being disconnected.
        :param userdata: unused.
        :param result_code: result code.
        """
        self.log_info("Disconnected with result code " + str(result_code))
        self.state_handler.set_state(State.goodbye)
        time.sleep(5)
        self.thread_handler.run(target=self.start_blocking)

    # pylint: disable=unused-argument
    def on_message(self, client, userdata, msg):
        """ Callback when the MQTT client received a new message.

        :param client: the MQTT client.
        :param userdata: unused.
        :param msg: the MQTT message.
        """
        self.log_info("New message on topic {}".format(msg.topic))
        self.log_debug("Payload {}".format(msg.payload))
        if msg.payload is None or len(msg.payload) == 0:
            pass
        if msg.topic is not None and msg.topic.startswith("hermes/intent/") and msg.payload:
            payload = json.loads(msg.payload.decode('utf-8'))
            intent = IntentParser.parse(payload, self.registry.intent_classes)
            self.log_debug("Parsed intent: {}".format(intent))
            if intent is not None and self.handle_intent is not None:
                self.log_debug("New intent: {}".format(str(intent.intentName)))
                self.handle_intent(intent, payload)
        elif msg.topic is not None and msg == "hermes/hotword/toggleOn":
            self.state_handler.set_state(State.hotword_toggle_on)
        elif HOTWORD_DETECTED_RE.match(msg.topic):
            if not self.first_hotword_detected:
                self.client.publish(
                    "hermes/feedback/sound/toggleOff", payload=None, qos=0, retain=False)
                self.first_hotword_detected = True
            self.state_handler.set_state(State.hotword_detected)
            if self.handle_start_listening is not None:
                self.handle_start_listening()
        elif msg.topic == "hermes/asr/startListening":
            self.state_handler.set_state(State.asr_start_listening)
        elif msg.topic == "hermes/asr/textCaptured":
            self.state_handler.set_state(State.asr_text_captured)
            if self.handle_done_listening is not None:
                self.handle_done_listening()
        elif msg.topic == "snipsmanager/setSnipsfile" and msg.payload:
            self.state_handler.set_state(State.asr_text_captured)

    def log_info(self, message):
        if self.logger is not None:
            self.logger.info(message)

    def log_debug(self, message):
        if self.logger is not None:
            self.logger.debug(message)

    def log_error(self, message):
        if self.logger is not None:
            self.logger.error(message)
