# -*-: coding utf-8 -*-
""" Wrapper for various TTS services (currently only Google). """

import json
import os
import time

import paho.mqtt.client as mqtt

from socket import error as socket_error
from gtts import gTTS

from .audio_player import AudioPlayer

class SnipsTTS:
    """ Snips TTS service. """

    def __init__(self, thread_handler, mqtt_hostname, mqtt_port, mqtt_topic, locale, logger=None):
        """ Initialise the service.

        :param mqtt_hostname: the MQTT broker hostname.
        :param mqtt_port: the MQTT broker port.
        :param mqtt_topic: the topic on which to post the sentence.
        :param locale: the language locale, e.g. "fr" or "en_US".
        """
        self.logger = logger
        self.locale = locale.split("_")[0]

        self.mqtt_topic = mqtt_topic
        self.mqtt_client = mqtt.Client("SnipsTTS")
        
        thread_handler.run(target=self.start_blocking, args=(mqtt_hostname, mqtt_port, ))

    def start_blocking(self, mqtt_hostname, mqtt_port, run_event):
        while True and run_event.is_set():
            try:
                self.mqtt_client.connect(mqtt_hostname, mqtt_port)
                break
            except (socket_error, Exception) as e:
                time.sleep(5)

    def speak(self, sentence):
        """ Speak a sentence using Snips TTS.

        :param sentence: the sentence to speak.
        """
        if self.mqtt_client is None:
            return

        if self.logger is not None:
            self.logger.info("Snips TTS: {}".format(sentence))
        self.mqtt_client.publish(
            self.mqtt_topic,
            payload=json.dumps({'text': sentence}),
            qos=0,
            retain=False)


class GTTS:
    """ Google TTS service. """

    def __init__(self, locale, logger=None):
        """ Initialise the service.

        :param locale: the language locale, e.g. "fr" or "en_US".
        """
        self.logger = logger
        self.locale = locale.split("_")[0]

    def speak(self, sentence):
        """ Speak a sentence using Google TTS.

        :param sentence: the sentence to speak.
        """
        snips_dir = ".snips"
        filename = "gtts.mp3"
        file_path = "{}/{}".format(snips_dir, filename)

        if not os.path.exists(snips_dir):
            os.makedirs(snips_dir)

        def delete_file():
            try:
                os.remove(file_path)
                if not os.listdir(snips_dir):
                    try:
                        os.rmdir(snips_dir)
                    except OSError:
                        pass
            except:
                pass

        if self.logger is not None:
            self.logger.info("Google TTS: {}".format(sentence))
        tts = gTTS(text=sentence, lang=self.locale)
        tts.save(file_path)
        AudioPlayer.play_async(file_path, delete_file)
