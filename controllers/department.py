"""Controller for deparment"""

#User Modules
from models.department import Department
from config.database import Database

class Department_Controller:

    def __init__(self):
        #Create table department
        Department()

        #Connect to database
        self.database = Database()
        self.db = self.database.mydb

    def close(self):
        self.db.cursor().close()
        self.db.close()


    def create(self):
        """Create a new department in the database"""

        name = input("Insert a name for the department: ")
        self.db.cursor().execute("""\
            INSERT INTO department (department_name)\
            VALUES (%s)""",\
            (\
                name,\
            ))
        self.db.commit()

    def print(self):
        """Print list of all departments in the database """

        list = self.list()
        for entry in list:
            print(" {} - {}".format(*entry))

    def list(self):
        """Return list all registers from the table deparment"""

        return self.database.list_registers("department")

    def delete(self):
        """Delete a entry of the table departments"""

        self.print()
        self.database.delete_register("department")

    def update(self):
        """Update department name"""

        self.print()
        id = int(input("Select the id to update: "))

        #Ask user for new department name
        dept_name = input("New department name: ")

        self.db.cursor().execute("""UPDATE department
            SET    department_name = %s
            WHERE  department.id = %s""",\
            (\
                dept_name,\
                id\
            ))
        self.db.commit()
