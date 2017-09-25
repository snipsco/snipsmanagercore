Snips Skills Core Utils
=======================

|Build Status| |PyPI| |MIT License|

The Snips Skills core utilities for creating end-to-end assistants

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

Troubleshooting
---------------

The following might be needed:

OSX
^^^

.. code-block:: console

    $ brew install swig

Raspbian
^^^^^^^^

.. code-block:: console

    $ sudo apt-get install libsdl-mixer1.2
    $ sudo apt-get install swig


Copyright
---------

This skill is provided by `Snips`_ as Open Source software. See `LICENSE.txt`_ for more
information.

.. |Build Status| image:: https://travis-ci.org/snipsco/snips-skills-core.svg
   :target: https://travis-ci.org/snipsco/snips-skills-core
   :alt: Build Status
.. |PyPI| image:: https://img.shields.io/pypi/v/snipsskillscore.svg
   :target: https://pypi.python.org/pypi/snipsskillscore
   :alt: PyPI
.. |MIT License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/snipsco/snips-skills-core/master/LICENSE.txt
   :alt: MIT License

.. _`PyPI`: https://pypi.python.org/pypi/snipsskillscore
.. _`pip`: http://www.pip-installer.org
.. _`Snips`: https://www.snips.ai
.. _`LICENSE.txt`: https://github.com/snipsco/snips-skills-core/blob/master/LICENSE.txt
