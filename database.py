"""Manage database of staff"""

#Python Modules
import sqlite3
from datetime import datetime

#User Modules
from config import Config
from card import Card

class Database:

    def __init__(self):
        """Create dabatase for staff and create/connect tables"""

        #Connect to database and turn on foreign keys
        self.conn = sqlite3.connect('staff.db')
        self.conn.execute("PRAGMA foreign_keys=ON");

        #Create table departments if doesn't exist
        self.conn.execute("""CREATE TABLE if not exists department(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department_name TEXT
            )""")

        #Create table employee if doesn't exist
        self.conn.execute("""CREATE TABLE if not exists employee(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_uid TEXT,
            first_name TEXT,
            last_name TEXT,
            department_id INTEGER,
            working INTEGER,
            created_at DATE,
            updated_at DATE,
            CONSTRAINT fk_departments
                FOREIGN KEY (department_id)
                REFERENCES DEPARTMENT (id)
                ON DELETE CASCADE
            )""")

        #Create table timeclock if doesn't exist
        self.conn.execute("""CREATE TABLE if not exists timeclock(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            sent INTEGER,
            clocking_time DATE,
            CONSTRAINT fk_employees
                FOREIGN KEY (employee_id)
                REFERENCES EMPLOYEE (id)
                ON DELETE CASCADE
            )""")

        self.conn.commit()

    def create_department(self):
        """Create a new department in the database"""

        name = input("Insert a name for the department: ")
        self.conn.execute("""\
            INSERT INTO department (department_name)\
            VALUES (?)""", (name,)\
            )
        self.conn.commit()

    def create_employee(self):
        """Create a new employee in the database"""

        print("Put a card on the NFC Reader......")

        #Read card
        card = Card()
        id = card.id
        first_name = input("Insert first name: ")
        last_name = input("Insert last name: ")

        list = self.list_registers("department")
        for entry in list:
            print(" {} - {}".format(*entry))
        department = input("Insert department id: ")

        self.conn.execute("""INSERT INTO employee\
            VALUES (null,?,?,?,?,?,?,?)""",\
            (\
                id,\
                first_name,\
                last_name,\
                department,\
                0,\
                datetime.now(),\
                datetime.now(),\
            ))
        self.conn.commit()

    def delete_register(self, table_name):
        """Delete a register from the table given in the database"""

        id = input("Select the id to remove: ")
        self.conn.execute("""DELETE FROM {} WHERE id={}""".format(table_name, id))
        self.conn.commit()

    def list_registers(self, table_name):
        """Return list all registers from the table given database"""

        conn_select = self.conn.cursor()
        conn_select.execute("""SELECT * FROM {}""".format(table_name))

        return conn_select.fetchall()


def __main__():
    #create/connect Database
    db = Database()

    #menu list
    menu = {}
    menu['1']="Create Department"
    menu['2']="Delete Department"
    menu['3']="List Departments"
    menu['4']="Create Employee"
    menu['5']="Delete Employee"
    menu['6']="List Employees"
    menu['7']="Register Clocking Time"
    menu['8']="Delete Clocking Register"
    menu['9']="List Clocking Registers"
    menu['0']="Exit"

    #loop asking user for an option
    while True:
        options=menu.keys()
        for entry in options:
            print("({}) - {}".format(entry, menu[entry]))

        selection=input("Please Select:")
        if selection =='1':
            db.create_department()
        elif selection == '2':
            #print list of all departments
            list = db.list_registers("department")
            for entry in list:
                print(" {} - {}".format(*entry))
            #delete register
            db.delete_register("department")
        elif selection == '3':
            list = db.list_registers("department")
            for entry in list:
                print(" {} - {}".format(*entry))
        elif selection == '4':
            db.create_employee()
        elif selection == '5':
            #print list of all employees
            list = db.list_registers("employee")
            for entry in list:
                print(" {} - {} - {} - {} - {} - {} - {} - {}".format(*entry))
            #delete register
            db.delete_register("employee")
        elif selection == '6':
            #print list of all employees
            list = db.list_registers("employee")
            for entry in list:
                print(" {} - {} - {} - {} - {} - {} - {} - {}".format(*entry))
        elif selection == '0':
            break
        else:
            print("Unknown Option Selected!")

        input("Press enter to continue...")


if __name__ == '__main__':
    __main__()
    #db.insert('3', 'Fabian', datetime.now())
    #db.select(3)
    #print(Config.DELAY_MINUTES.value)
