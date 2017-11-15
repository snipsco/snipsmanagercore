Snips Manager Core Utils
========================

|Build Status| |PyPI| |MIT License|

The Snips Manager core utilities for creating end-to-end assistants

Installation
------------

The skill is on `PyPI`_, so you can just install it with `pip`_:

.. code-block:: console

    $ pip install snipsfakeweather

Usage
-----

The skill presents fake weather forecasts for demo purposes.

.. code-block:: python

    from snipsfakeweather.snipsfakeweather import SnipsFakeWeather

    weather = SnipsFakeWeather() 
    weather.speak_forecast("Paris,fr")

Raspbian
^^^^^^^^

.. code-block:: console

    $ sudo apt-get install libsdl-mixer1.2
    $ sudo apt-get install swig


Copyright
---------

This skill is provided by `Snips`_ as Open Source software. See `LICENSE.txt`_ for more
information.

.. |Build Status| image:: https://travis-ci.org/snipsco/snipsmanagercore.svg
   :target: https://travis-ci.org/snipsco/snipsmanagercore
   :alt: Build Status
.. |PyPI| image:: https://img.shields.io/pypi/v/snipsmanagercore.svg
   :target: https://pypi.python.org/pypi/snipsmanagercore
   :alt: PyPI
.. |MIT License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/snipsco/snipsmanagercore/master/LICENSE.txt
   :alt: MIT License

.. _`PyPI`: https://pypi.python.org/pypi/snipsmanagercore
.. _`pip`: http://www.pip-installer.org
.. _`Snips`: https://www.snips.ai
.. _`LICENSE.txt`: https://github.com/snipsco/snipsmanagercore/blob/master/LICENSE.txt
