"""Controller for employees"""

#User Modules
from models.employee import Employee
from controllers.department import Department_Controller
from database import Database
from card import Card

#Python Modules
from datetime import datetime

class Employee_Controller:

    def __init__(self):
        #Create table department
        Employee()

        #Connect to database
        self.database = Database()
        self.db = self.database.mydb

    def close(self):
        self.db.cursor().close()
        self.db.close()


    def create(self):
        """Create a new employee in the database"""

        print("Put a card on the NFC Reader......")
        #Read card
        card = Card()
        print("Card read successfully....")

        card_uid = card.id
        first_name = input("Insert first name: ")
        last_name = input("Insert last name: ")

        #Print department and close the connection
        dept_controller = Department_Controller()
        dept_controller.print()

        department = input("Insert department id: ")

        self.db.cursor().execute("""INSERT INTO employee\
            VALUES (NULL,%s,%s,%s,%s,%s,%s,%s)""",\
            (\
                card_uid,\
                first_name,\
                last_name,\
                department,\
                0,\
                datetime.now(),\
                datetime.now(),\
            ))
        self.db.commit()

    def print(self):
        """Print list of all employees in the database """

        list = self.list()
        for entry in list:
            print(" {} - {} - {} - {} - {} - {} - {} - {}".format(*entry))

    def list(self):
        """Return list all registers from the table employees"""

        return self.database.list_registers("employee")

    def delete(self):
        """Delete a entry of the table employees"""

        self.print()
        self.database.delete_register("employee")
