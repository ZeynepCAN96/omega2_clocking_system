"""General card class to get the ID of it"""

#Python Modules
import subprocess

class Card():

    def __init__(self):
        #set id = 0 just for keep the loop
        self.id = 0

        #loop until a card is readed
        while self.id == 0:
            cmd = "nfc-list | grep UID | sed -e 's/ //g' -e 's/^.*://'"
            uid = subprocess\
                .run(cmd, shell=True, stdout=subprocess.PIPE)\
                .stdout\
                .decode('ascii')\
                .replace('\n', '')

            #save card uid in id when a card is read
            self.id = uid if uid != '' else 0
