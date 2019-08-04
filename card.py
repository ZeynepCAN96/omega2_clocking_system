"""General card class to get the ID of it"""

#Python Modules
import subprocess

class Card():

    def __init__(self):
        self.id = 0

        while self.id == 0:
            cmd = "nfc-list | grep UID | sed -e 's/ //g' -e 's/^.*://'"
            uid = subprocess\
                .run(cmd, shell=True, stdout=subprocess.PIPE)\
                .stdout\
                .decode('ascii')\
                .replace('\n', '')

            #save card uid in id when a card is read
            self.id = uid if uid != '' else 0
