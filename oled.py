"""Manage OLED expansion
    RUN following commands in order to use it
    opkg update
    opkg install python3-light
    opkg install python3-oled-exp
"""

#Python Modules
import time as t

#OMEGA Modules
from OmegaExpansion import oledExp

#User Modules
from config import Config

class Oled():

    def __init__(self):
        #check if oled is configured in config.py
        self.oled_active = Config.OLED_EXPANSION.value

        if(self.oled_active):
            #Initialize the OLED Display
            oledExp.driverInit()

            #Turn on the screen
            oledExp.setDisplayPower(1)

    def msg_ok(self, name, time):
        #check if a oled is active
        if(self.oled_active):
            #display ok image and show it for 2 seconds
            oledExp.drawFromFile(Config.OK_IMG.value)
            t.sleep(2)
            oledExp.clear()

            #write message and show it for 3 seconds
            oledExp.write("Name: {} - Clocking Time: {}".format(name, time))
            t.sleep(3)
            oledExp.clear()

            ##Turn off the screen
            oledExp.setDisplayPower(0)

    def msg_error(self, message):
        #check if a oled is active
        if(self.oled_active):
            #display ok image and show it for 2 seconds
            oledExp.drawFromFile(Config.ERROR_IMG.value)
            t.sleep(2)
            oledExp.clear()

            #write message and show it for 3 seconds
            oledExp.write(message)
            t.sleep(3)
            oledExp.clear()

            ##Turn off the screen
            oledExp.setDisplayPower(0)
