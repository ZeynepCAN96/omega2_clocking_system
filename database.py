"""Manage database of staff"""

#Python Modules
import sqlite3
from datetime import datetime
import math

#User Modules
from config import Config
from card import Card
from oled import Oled

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
            card_uid TEXT UNIQUE,
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
        print("Card read successfully....")

        card_uid = card.id
        first_name = input("Insert first name: ")
        last_name = input("Insert last name: ")

        #Print department
        self.print_department()

        department = input("Insert department id: ")

        self.conn.execute("""INSERT INTO employee\
            VALUES (null,?,?,?,?,?,?,?)""",\
            (\
                card_uid,\
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
        self.conn.execute("""DELETE FROM {} WHERE id={}""".\
            format(table_name, id))
        self.conn.commit()


    def list_registers(self, table_name):
        """Return list all registers from the table given database"""

        conn_select = self.conn.cursor()
        conn_select.execute("""SELECT * FROM {}""".format(table_name))

        return conn_select.fetchall()


    def print_department(self):
        """Print list of all departments in the database """

        list = self.list_registers("department")
        for entry in list:
            print(" {} - {}".format(*entry))


    def print_employee(self):
        """Print list of all employees in the database """

        list = self.list_registers("employee")
        for entry in list:
            print(" {} - {} - {} - {} - {} - {} - {} - {}".format(*entry))

    def list_time_clocking(self, employee_table,timeclock_table):
        """Return list all clocking times from the table given database"""

        conn_select = self.conn.cursor()
        conn_select.execute(\
            """SELECT * FROM {} INNER JOIN {}  ON {}.id={}.employee_id"""\
            .format(employee_table,\
                timeclock_table,\
                employee_table,\
                timeclock_table\
                ))

        return conn_select.fetchall()

    def print_time_clocking(self):
        """Print list of all clocking time in the database """

        list = self.list_time_clocking("employee","timeclock")
        for entry in list:
            print(" {} - {} - {}".format(entry[8], entry[2],  entry[3]),entry[11])


    def register_clocking_time(self, uid):
        """Register clocking time for the user with card uid given"""

        conn_select = self.conn.cursor()
        rows = conn_select.execute("""\
            SELECT id,\
                first_name,\
                last_name,\
                working,\
                updated_at\
                FROM employee WHERE card_uid = ?""", (uid,)\
            ).fetchone()

        #Check if there is no employee with the given uid
        if(rows==None):
            oled_screen = Oled()
            oled_screen.msg_error("Employee not found")
            return 0

        #Calculate delay from last clocking registered
        last_clocking = datetime.strptime(rows[4], '%Y-%m-%d %H:%M:%S.%f')
        now = datetime.now()
        delay = now - last_clocking

        #Check delay configured for clocking again
        if(delay.seconds < Config.DELAY_SECONDS.value):
            #duplicate entry detected
            oled_screen = Oled()
            oled_screen.msg_error(\
                "You already registered your time, wait {} seconds"\
                .format(Config.DELAY_SECONDS.value-delay.seconds))

            return 0

        #Register new clocking time
        #change working status 1 -> 0 or 0 -> 1
        working = 0 if rows[3] else 1

        #Update working status in employees
        self.conn.execute("""\
            UPDATE employee\
            SET working = ?, updated_at = ?\
            WHERE id = ?""", (working, now, rows[0],)\
            )
        self.conn.commit()

        #Save clocking time
        self.conn.execute("""INSERT INTO timeclock\
            VALUES (null,?,0,?)""",\
            (\
                rows[0],\
                now,\
            ))
        self.conn.commit()

        oled_screen = Oled()
        oled_screen.msg_ok("{} {}".format(rows[1], rows[2]), now)

        return 1



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
    menu['7']="Delete Clocking Register"
    menu['8']="List Clocking Registers"
    menu['0']="Exit"

    #loop asking user for an option
    while True:
        options=menu.keys()

        #print menu
        for entry in options:
            print("({}) - {}".format(entry, menu[entry]))

        #ask user for an option
        selection=input("Please Select:")

        if selection =='1':
            db.create_department()
        elif selection == '2':
            #print list of all departments
            db.print_department()
            #delete register
            db.delete_register("department")
        elif selection == '3':
            #print list of all departments
            db.print_department()
        elif selection == '4':
            db.create_employee()
        elif selection == '5':
            #print list of all employees
            db.print_employee()
            #delete register
            db.delete_register("employee")
        elif selection == '6':
            #print list of all employees
            db.print_employee()
        elif selection == '7':
            #print list of all clococking times
            db.print_time_clocking()
            #delete register
            db.delete_register("timeclock")
        elif selection == '8':
            #print list of all clococking times
             db.print_time_clocking()
        elif selection == '0':
            break
        else:
            print("Unknown Option Selected!")

        input("Press enter to continue...")


if __name__ == '__main__':
    __main__()
