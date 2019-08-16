# Omega2_clocking_system

# What is this ?

- Clocking system is a simple Python project intended to keep a check-in time and check-out time of employees in a school.
- While creating the project, we use Omega2 + device with  RFID and NFC expansion.
- We consult with Onion Omega2 documentation.

See   https://docs.onion.io/omega2-docs/

- This is in development.

# Requirements

You need Python 3 to run clocking system.

To install Python3, start by updating your package manager:

` opkg update`

the full version of python3:

`opkg install python3`

See https://docs.onion.io/omega2-docs/installing-and-using-python.html


**Contents**

.. contents::

# How to use this ?


Quick Start
-------------
Get your Omega2 + up and running by following the [Omega2 + getting started guide](https://docs.onion.io/omega2-docs/first-time-setup.html).


The official Python package manager, pip, is the standard way of installing Python modules on a system.

We’ll need to first install pip on the Omega:

`opkg update`

`opkg install python-pip`




User Setting
-------------

To stop the system , you'll first need to set up a tag for it in settings :

`ID_STOP_SYSTEM = "b5c6e7bb"` *-Card id to stop the system*

To avoid the duplicate , you'll need to use delay :

`DELAY_SECONDS = 30`*-Delay for clocking again in seconds*

To use Oled expansion , It should be 1 (ON) :

`OLED_EXPANSION = 1`*-1 = ON or 0 = OFF*






Working With RFID & NFC Expansion
-------------

The NFC & RFID Expansion brings contact-less RFID and NFC communication to the Omega ecosystem.

See  https://docs.onion.io/omega2-docs/using-rfid-nfc-expansion.html




### Installation

----

To use your RFID & NFC Expansion, you’ll first need to initialize the device:

` opkg update`

` opkg install nfc-exp`


### Scanning RFID/NFC Tags

To scan an RFID/NFC Tag, you can use the `nfc-list` utility.




### Using Mifare Ultralight Cards

`nfc-mfultralight` program is used to configure the ` Mifare Ultralight `type cards. You can read from the tag and write to it.

In order to scan the tag and store it to a file, please run the following command:

` nfc-mfultralight r mycardUltra.mfd`

To view the content of the file, use xxd utility by using the following command:

`xxd mycardUltra.mfd`


# Testing

The basic ways to run tests:

1.Switch to Onion Omega2 screen in the terminal.
2.Run the `python3 main.py`
3.Read the card to RFID expansion
4.Run the `python3 database.py`

See [Running and Writing Tests](https://devguide.python.org/runtests/) for more on running tests.

# Built With

- [Atom](https://atom.io) *- Used to edit the code*
- [DB Browser for SQLite](https://sqlitebrowser.org) *- Used to generate the database*

# License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/Panchop10/omega2_clocking_system/blob/test/LICENSE) file for details
