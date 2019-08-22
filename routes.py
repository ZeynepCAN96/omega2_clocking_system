"""Manage all the routes of the system"""

# User Modules
from database import Database
from controllers.department import Department_Controller
from controllers.employee import Employee_Controller
from controllers.timeclock import Timeclock_Controller

class Routes:

    def __init__(self):
        self.dept_controller = Department_Controller()
        self.emp_controller = Employee_Controller()
        self.timecl_controller = Timeclock_Controller()

    # Department Routes
    def create_department(self):
        self.dept_controller.create()

    def print_department(self):
        self.dept_controller.print()

    def delete_department(self):
        self.dept_controller.delete()

    # Employee Routes
    def create_employee(self):
        self.emp_controller.create()

    def print_employee(self):
        self.emp_controller.print()

    def delete_employee(self):
        self.emp_controller.delete()

    # Timeclock Routes
    def register_timeclock(self):
        self.timecl_controller.register()

    def print_timeclock(self):
        self.timecl_controller.print()

    def delete_timeclock(self):
        self.timecl_controller.delete()
