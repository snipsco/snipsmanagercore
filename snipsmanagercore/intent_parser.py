# -*-: coding utf-8 -*-
""" Helper class for parsing intents. """

from dateutil.parser import parse

from snipsmanagercore.instant_time import InstantTime
from snipsmanagercore.time_interval import TimeInterval


class IntentParser:
    """ Helper class for parsing intents. """

    @staticmethod
    def parse(payload, candidate_classes):
        """ Parse a json response into an intent.

        :param payload: a JSON object representing an intent.
        :param candidate_classes: a list of classes representing various
                                  intents, each having their own `parse`
                                  method to attempt parsing the JSON object
                                  into the given intent class.
        :return: An object version of the intent if one of the candidate
                 classes managed to parse it, or None.
        """
        for cls in candidate_classes:
            intent = cls.parse(payload)
            if intent:
                return intent
        return None

    @staticmethod
    def get_intent_name(payload):
        """ Return the simple intent name. An intent has the form:

           {
               "input": "turn the lights green",
               "intent": {
                   "intentName": "user_BJW0GIoCx__Lights",
                   ...
               },
               "slots": [...]
           }

           and this function extracts the last part of the intent
           name ("Lights"), i.e. removing the user id.

        :param payload: the intent, in JSON format.
        :return: the simpe intent name.
        """
        if 'intent' in payload and 'intentName' in payload['intent']:
            return payload['intent']['intentName'].split('__')[-1]
        return None

    @staticmethod
    def get_slot_value(payload, slot_name):
        """ Return the parsed value of a slot. An intent has the form:

            {
                "text": "brew me a cappuccino with 3 sugars tomorrow",
                "slots": [
                    {"value": {"slotName": "coffee_type", "value": "cappuccino"}},
                    ...
                ]
            }

            This function extracts a slot value given its slot name, and parses
            it into a Python object if applicable (e.g. for dates).

            Slots can be of various forms, the simplest being just:

            {"slotName": "coffee_sugar_amout", "value": "3"}

            More complex examples are date times, where we distinguish between
            instant times, or intervals. Thus, a slot:

            {
              "slotName": "weatherForecastStartDatetime",
              "value": {
                "kind": "InstantTime",
                "value": {
                  "value": "2017-07-14 00:00:00 +00:00",
                  "grain": "Day",
                  "precision": "Exact"
                }
              }
            }

            will be extracted as an `InstantTime` object, with datetime parsed
            and granularity set.

            Another example is a time interval:

            {
              "slotName": "weatherForecastStartDatetime",
              "value": {
                "kind": "TimeInterval",
                "value": {
                  "from": "2017-07-14 12:00:00 +00:00",
                  "to": "2017-07-14 19:00:00 +00:00"
                }
              },
            }

            which will be extracted as a TimeInterval object.

        :param payload: the intent, in JSON format.
        :return: the parsed value, as described above.
        """

        if not 'slots' in payload:
            return None

        slot = None
        for candidate in payload['slots']:
            if 'slotName' in candidate and candidate['slotName'] == slot_name:
                slot = candidate
                break

        if not slot:
            return None

        kind = IntentParser.get_dict_value(slot, ['value', 'kind'])
        if kind == "InstantTime":
            return IntentParser.parse_instant_time(slot)
        elif kind == "TimeInterval":
            return IntentParser.parse_time_interval(slot)

        return IntentParser.get_dict_value(slot, ['value', 'value', 'value']) \
            or IntentParser.get_dict_value(slot, ['value', 'value'])

    @staticmethod
    def parse_instant_time(slot):
        """ Parse a slot into an InstantTime object.

        Sample response:

        {
          "entity": "snips/datetime",
          "range": {
            "end": 36,
            "start": 28
          },
          "rawValue": "tomorrow",
          "slotName": "weatherForecastStartDatetime",
          "value": {
            "grain": "Day",
            "kind": "InstantTime",
            "precision": "Exact",
            "value": "2017-09-15 00:00:00 +00:00"
          }
        }

        :param slot: a intent slot.
        :return: a parsed InstantTime object, or None.
        """
        date = IntentParser.get_dict_value(slot, ['value', 'value'])
        if not date:
            return None
        date = parse(date)
        if not date:
            return None
        grain = InstantTime.parse_grain(
            IntentParser.get_dict_value(slot,
                                        ['value', 'grain']))
        return InstantTime(date, grain)

    @staticmethod
    def parse_time_interval(slot):
        """ Parse a slot into a TimeInterval object.

        Sample response:

        {
          "entity": "snips/datetime",
          "range": {
            "end": 42,
            "start": 13
          },
          "rawValue": "between tomorrow and saturday",
          "slotName": "weatherForecastStartDatetime",
          "value": {
            "from": "2017-09-15 00:00:00 +00:00",
            "kind": "TimeInterval",
            "to": "2017-09-17 00:00:00 +00:00"
          }
        }

        :param slot: a intent slot.
        :return: a parsed TimeInterval object, or None.
        """
        start = IntentParser.get_dict_value(
            slot, ['value', 'from'])
        end = IntentParser.get_dict_value(slot, ['value', 'to'])
        if not start or not end:
            return None
        start = parse(start)
        end = parse(end)
        if not start or not end:
            return None
        return TimeInterval(start, end)

    @staticmethod
    def get_dict_value(dictionary, path):
        """ Safely get the value of a dictionary given a key path. For
            instance, for the dictionary `{ 'a': { 'b': 1 } }`, the value at
            key path ['a'] is { 'b': 1 }, at key path ['a', 'b'] is 1, at
            key path ['a', 'b', 'c'] is None.

        :param dictionary: a dictionary.
        :param path: the key path.
        :return: The value of d at the given key path, or None if the key
                 path does not exist.
        """
        if len(path) == 0:
            return None
        temp_dictionary = dictionary
        try:
            for k in path:
                temp_dictionary = temp_dictionary[k]
            return temp_dictionary
        except (KeyError, TypeError):
            pass
        return None
