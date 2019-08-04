"""
Constantly scan looking for presence of a tag
If a tag is found the uid is compared with a database
and the data is sent to a google spreadsheet
"""

#Python Modules
import json

#User Modules
from card import Card
from database import Database

#constantly scan for rfid tag presence
def __main__():
    """Open nfc reader continusly untill a card is read"""

    # while True:
    #     #Read card, the constructor will search for a card until it gets one
    #     card = Card()
    #     print(card.id)
    #
    #     break

    db = Database()
    staff = db.register_clocking_time('0409bf32ed4c81')



    #print(staff['working'])




if __name__ == '__main__':
    __main__()
