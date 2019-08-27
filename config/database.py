"""Manage database of staff"""

# Python Modules
import mysql.connector

# User Modules
from config.config import Config

class Database:

    def __init__(self):
        """Create dabatase for staff and create/connect tables"""

        #Create connection to database
        self.mydb = mysql.connector.connect(
            host=Config.HOST.value,
            port=Config.PORT.value,
            user=Config.USER.value,
            passwd=Config.PASSWD.value,
            database=Config.DATABASE.value,
        )

    def delete_register(self, table_name):
        """Delete a register from the table given in the database"""

        id = int(input("Select the id to remove: "))
        self.mydb.cursor().execute("""DELETE FROM {} WHERE id=%s"""\
            .format(table_name),\
            (\
                id,\
            ))
        self.mydb.commit()


    def list_registers(self, table_name):
        """Return list all registers from the table given database"""

        conn_select = self.mydb.cursor()
        conn_select.execute("""SELECT * FROM {}""".format(table_name))

        return conn_select.fetchall()
