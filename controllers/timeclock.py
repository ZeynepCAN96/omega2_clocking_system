"""Controller for timeclock"""

# User Modules
from models.timeclock import Timeclock
from config.database import Database
from config.config import Config
from google_spreadsheet.gsheet import Gsheet
from omega_expansions.oled import Oled

# Python Modules
from datetime import datetime

class Timeclock_Controller:

    def __init__(self):
        #Create table timeclock
        Timeclock()

        #Connect to database
        self.database = Database()
        self.db = self.database.mydb

    def close(self):
        self.db.cursor().close()
        self.db.close()


    def register(self, uid):
        """Register clocking time for the user with card uid given"""

        conn_select = self.db.cursor()
        conn_select.execute("""SELECT id,\
            first_name,\
            last_name,\
            working,\
            updated_at,\
            last_clock_register\
            FROM employee\
            WHERE employee.card_uid = %s""",\
            (\
                uid,\
            ))

        rows = conn_select.fetchone()

        if(rows==None):
            oled_screen = Oled()
            oled_screen.msg_error("Employee not found")
            return 0

        #Calculate delay from last clocking registered
        last_clock = datetime.strptime(str(rows[4]), '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        delay = now - last_clock

        #Prevent wrong registers because of people forget to clockout

        working = rows[3]

        if((last_clock.day != now.day) and (working==1)):
            working = 0

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
        working = 0 if working else 1

        #Update working status in employees
        self.db.cursor().execute("""\
            UPDATE employee\
            SET\
            working = %s,\
            updated_at = %s,\
            last_clock_register = %s\
            WHERE id = %s""",\
            (\
                working,\
                now,\
                now,\
                rows[0]\
            ))
        self.db.commit()

        #Save clocking time
        #working 1 = clock in / working 0 = clock out
        self.db.cursor().execute("""INSERT INTO timeclock\
            VALUES (null,%s,0,%s,%s)""",\
            (\
                rows[0],\
                now,\
                working\
            ))
        self.db.commit()

        oled_screen = Oled()
        oled_screen.msg_ok("{} {}".format(rows[1], rows[2]), now)

        #Insert data in spreadsheet
        gsheet = Gsheet("{}-{} {}".format(rows[0], rows[1], rows[2]))

        #Convert last clocking into datetime object
        last_clocking = rows[5]
        if last_clocking != None:
            last_clocking = datetime.strptime(str(rows[5]), '%Y-%m-%d %H:%M:%S')

        #Insert data into spreadsheet
        gsheet.insert_clock_register(datetime.now(), last_clocking, working)

        return 1

    def print(self):
        """Print list of all clocking time in the database """

        list = self.list()
        for entry in list:
            print(" {} - {} - {}".format(entry[8], entry[2],  entry[3]),entry[11])

    def list(self):
        """Return list all clocking times from the table given database"""

        employee_table = "employee"
        timeclock_table = "timeclock"

        conn_select = self.db.cursor()
        conn_select.execute(\
            """SELECT * FROM {} INNER JOIN {}  ON {}.id={}.employee_id"""\
            .format(employee_table,\
                timeclock_table,\
                employee_table,\
                timeclock_table\
                ))

        return conn_select.fetchall()

    def delete(self):
        """Delete a entry of the table timeclock"""

        self.print()
        self.database.delete_register("timeclock")
