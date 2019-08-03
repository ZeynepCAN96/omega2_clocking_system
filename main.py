"""
Constantly scan looking for presence of a tag
If a tag is found the uid is compared with a database
and the data is sent to a google spreadsheet
"""

import subprocess


#constantly scan for rfid tag presence
def __main__():
    count = 0
    while count < 10:
        cmd = "nfc-list | grep UID | sed -e 's/ //g' -e 's/^.*://'"
        uid = subprocess
            .run(cmd, shell=True, stdout=subprocess.PIPE)
            .stdout
            .replace('\n', '')
            .decode('ascii')

        print(uid)
        count += 1

if __name__ == '__main__':
    __main__()
