"""Menu for manage the database"""

# User Modules
from routes import Routes

if __name__ == '__main__':

    #Routes with all the end points of the program
    routes = Routes()

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
    menu['9']="Update Employee's Card"
    menu['10']="Update Employee's Name"
    menu['11']="Update Department Name"
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
            #Create a new department
            routes.create_department()
        elif selection == '2':
            #delete register from department
            routes.delete_department()
        elif selection == '3':
            #print list of all departments
            routes.print_department()
        elif selection == '4':
            #Create a new employee
            routes.create_employee()
        elif selection == '5':
            #delete register from employee
            routes.delete_employee()
        elif selection == '6':
            #print list of all employees
            routes.print_employee()
        elif selection == '7':
            #delete register
            routes.delete_timeclock()
        elif selection == '8':
            #print list of all clocking times
            routes.print_timeclock()
        elif selection == '9':
            #Update employee's card
            routes.update_employee_uid()
        elif selection == '10':
            #Update employee's name
            routes.update_employee_name()
        elif selection == '11':
            #Update department name
            routes.update_department()
        elif selection == '0':
            break
        else:
            print("Unknown Option Selected!")

        input("Press enter to continue...")
