"""Employee model"""

# User Modules
from config.database import Database

class Employee:

    def __init__(self):
        #Connect to database
        database = Database()
        self.db = database.mydb

        #Create table employee if doesn't exist
        self.db.cursor().execute("""CREATE TABLE if not exists employee
             (
                id INT(11) NOT NULL auto_increment,
                card_uid TEXT NOT NULL ,
                first_name TEXT NOT NULL ,
                last_name TEXT NOT NULL ,
                department_id INT(11) NOT NULL ,
                working      INT(11) NOT NULL ,
                created_at   DATETIME NOT NULL ,
                updated_at   DATETIME NOT NULL ,
                last_clock_register   DATETIME NULL ,
                UNIQUE card_uid (card_uid(11)) ,
                PRIMARY KEY (id),
                KEY department_id (department_id),
                CONSTRAINT department_id
                    FOREIGN KEY (department_id)
                    REFERENCES department (id)
                    ON DELETE CASCADE
             )""")

        self.db.commit()
