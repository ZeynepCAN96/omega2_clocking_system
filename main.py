"""
Constantly scan looking for presence of a tag
If a tag is found the uid is compared with a database
and the data is sent to a google spreadsheet
"""

import subprocess


#constantly scan for rfid tag presence
def __main__():
    while 1:
        cmd = "nfc-list | grep UID | sed -e 's/ //g' -e 's/^.*://'"
        uid = subprocess.check_output(cmd, shell=True).rstrip('\n')
        print(uid)

if __name__ == '__main__':
    __main__()
