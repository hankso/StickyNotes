Sticky Notes
============
Sticky notes is a cloud based notes sharing program. Create, edit and manage your small chunks of text (logs, notes, or binary data) and share it with generated QRCode. You can print and stick the QRCode to a place in case that you want to remind someone somethings.

Python server
=============

Dependencies
------------
Only `bottle <https://bottlepy.org/docs/dev/>`_ is needed other than Python built-in libraries.

:code:`sudo python -m pip install bottle`

It uses files and directories to store your data at cloud, but you can also choose SQLite database as backend. This requires one more module:

:code:`sudo python -m pip install bottle-sqlite`

Installation
------------
You can install from PyPi:

:code:`sudo python -m pip install stickynotes`

or install from source:

.. code:: bash

    git clone https://github.com/hankso/StickyNotes.git
    cd StickyNotes/src/python
    python setup.py build && sudo python setup.py install

Configuration
-------------
This program automatically loads configuration files from::

    1. /path/to/python/site-packages/stickynotes/config.[conf|ini]
    2. ./stickynotes.conf
    3. ~/.stickynotes.conf

All avaiable configure options are detaily commented in our default `config file <src/python/stickynotes/config.conf>`_.


Note
----
Template is not used to render webpage, because Python is not the only distribution in this project. C based server or GitHub Pages (which only provides pure static file hosting) may be used also.


ESP server
==========
ESP32 is a 32-bits MCU with WiFi & BT, which can be used to provide the cloud notes service by mDNS and HTTP Server on RTOS. This part is developed with `ESP-IDF <https://github.com/espressif/esp-idf>`_. See `IDF Docs <https://docs.espressif.com/projects/esp-idf>`_ for information about developing and flashing the app to an ESP32 chip/module.

How to use with ESP-IDF
-----------------------
1. Install toolchain, IDF and configure PATH etc.
2. Clone this repo as an application of IDF.
3. Configure according to chip/module hardware resources.
4. Compile and flash.

.. code:: bash
    
    git clone https://github.com/hankso/StickyNotes.git
    cd StickyNotes/src/esp32
    make flash

TODO
====
- URL marshal/obfuscate
- login for permission
- size limit
- rich feature render
- static file: mavo.io saving to GitHub
- esp32: use SPI Flash file system
