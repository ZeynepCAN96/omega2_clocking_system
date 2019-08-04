"""Configuration file for Clocking System"""

#Python Modules
from enum import Enum

class Config(Enum):
    DELAY_MINUTES = 10 #DELAY FOR CLOCKING AGAIN IN SECONDS (AVOID DUPLICATE)
    OLED_EXPANSION = 1 #1 = ON OR 0 = OFF (USE OLED EXPANSION)