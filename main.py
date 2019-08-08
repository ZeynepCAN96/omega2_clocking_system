"""
Constantly scan looking for presence of a tag
If a tag is found the uid is compared with a database
and the data is sent to a google spreadsheet
"""
#08/08/2019 version

#User Modules
from card import Card
from database import Database
from config import Config

#constantly scan for rfid tag presence
def __main__():
    """Open nfc reader continusly until a card is read"""

    db = Database()

    while True:
        #Read card, the constructor will search for a card until it gets one
        card = Card()

        #break the loop if the card presented is the one configured to stop it
        if(card.id == Config.ID_STOP_SYSTEM.value):
            break

        db.register_clocking_time(card.id)


if __name__ == '__main__':
    __main__()
