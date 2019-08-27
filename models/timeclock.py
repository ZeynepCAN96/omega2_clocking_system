"""Timeclock model"""

# User Modules
from config.database import Database

class Timeclock:

    def __init__(self):
        #Connect to database
        database = Database()
        self.db = database.mydb

        #Create table employee if doesn't exist
        self.db.cursor().execute("""CREATE TABLE if not exists timeclock
         (
            id            INT(11) NOT NULL auto_increment,
            employee_id   INT(11) NOT NULL,
            sent          INT(11) NOT NULL,
            clocking_time DATETIME NOT NULL,
            clock_status INT(11) NOT NULL,
            PRIMARY KEY (id),
            KEY employee_id (employee_id),
            CONSTRAINT employee_id
                FOREIGN KEY (employee_id)
                REFERENCES employee (id)
                ON DELETE CASCADE
         )""")

        self.db.commit()
