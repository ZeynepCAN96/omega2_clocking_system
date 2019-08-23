"""Department model"""

# User Modules
from config.database import Database

class Department:

    def __init__(self):
        #Connect to database
        database = Database()
        self.db = database.mydb

        #Create table department if doesn't exist
        self.db.cursor().execute("""CREATE TABLE if not exists department
         (
            id INT(11) NOT NULL auto_increment,
            department_name TEXT NOT NULL,
            PRIMARY KEY (id)
         )""")

        self.db.commit()
