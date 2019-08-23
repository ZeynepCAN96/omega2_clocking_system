"""Class to manage google spreadsheet"""

# Python Modules
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# User Modules
from config.config import Config

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    Config.KEY_FILE.value,
    scope
)
client = gspread.authorize(creds)

class Gsheet:

    def __init__(self, wsheet_name):

        #Open the spreadsheet
        spreadsheet = client.open(Config.SPREADSHEET_NAME.value)

        #Select a worksheet
        try:
            #Try to open a worksheet
            self.s = spreadsheet.worksheet(wsheet_name)

        except gspread.exceptions.WorksheetNotFound:
            #Create a new worksheet if wasn't found
            spreadsheet.add_worksheet(
                title=wsheet_name,
                rows="100",
                cols="10"
            )

            #Select the worksheet
            self.s = spreadsheet.worksheet(wsheet_name)
            self.s.update_cell(1, 1, wsheet_name)

    def get_last_row(self, col):
        """Returns the number of the last row of a specific column"""

        return len(self.s.col_values(col))

    def get_last_col(self, row):
        """Returns the number of the last column of a specific row"""

        return len(self.s.row_values(row))

    def insert_clock_register(self, new_reg, last_clock_register, in_or_out):
        """
        Insert new clock register
        in_or_out = 1 means that is clockin
        in_or_out = 0 means that is clockout
        """
        #Get last written row
        last_row = self.get_last_row(1)

        #check if last clocking was month before and set create_header to 1
        create_header = 0

        if last_clock_register != None:
            month_new_reg = new_reg.month
            month_last_reg = last_clock_register.month

            if month_new_reg != month_last_reg:
                create_header = 1

        #create header if last clock register is none o month before
        if last_clock_register == None or create_header:
            self.s.update_cell(last_row+2, 1, new_reg.strftime("%B"))
            self.s.update_cell(last_row+2, 5, "Total Worked")
            self.s.update_cell(last_row+2, 6, "00:00:00")
            self.s.update_cell(last_row+3, 1, "In")
            self.s.update_cell(last_row+3, 2, "Out")
            self.s.update_cell(last_row+3, 3, "Total")
            self.s.update_cell(last_row+3, 5, "Day")
            self.s.update_cell(last_row+3, 6, "Daily Total Hours")

        if in_or_out:
            #Registering clocking
            last_row = self.get_last_row(1)+1
            self.s.update_cell(last_row, 1, str(new_reg))
        else:
            #Registering clockout
            last_row = self.get_last_row(1)
            self.s.update_cell(last_row, 2, str(new_reg))
            hours_worked = self.calculate_hours_worked()
            self.calculate_total_per_day(datetime.now(), hours_worked)

    def calculate_total_per_day(self, today, worked_time):
        today = today.strftime("%d-%m-%Y")

        try:
            #Try to find a cell with today date in total worked hours
            cell = self.s.find(today)

            #get the value of time and we conver it to datetime
            time = self.s.cell(cell.row, cell.col+1).value
            time = datetime.strptime(time, '%H:%M:%S')

            #calculate new worked time
            new_worked_time = time + worked_time
            new_worked_time = new_worked_time.strftime('%H:%M:%S')


            #save the new info in the row
            self.s.update_cell(cell.row, cell.col+1, str(new_worked_time))

        except gspread.exceptions.CellNotFound:
            #If the cell wasn't found we create a new day
            #and we put the worked time
            last_row = self.get_last_row(5) + 1
            self.s.update_cell(last_row, 5, today)
            self.s.update_cell(last_row, 6, str(worked_time))

        #add worked hours to the daily total
        self.add_total_worked_hours(worked_time)

    def calculate_hours_worked(self):
        """
        Calculate delta between clockin and
        clockout and write it on the sheet
        """

        last_row = self.get_last_row(1)
        clockin = self.s.cell(last_row, 1).value
        clockout = self.s.cell(last_row, 2).value
        clockin = datetime.strptime(clockin, '%Y-%m-%d %H:%M:%S')
        clockout = datetime.strptime(clockout, '%Y-%m-%d %H:%M:%S')
        self.s.update_cell(last_row, 3, str(clockout-clockin))

        return clockout-clockin

    def add_total_worked_hours(self, worked_time):
        """Add worked hours to the total of the month"""

        #Get last cell which says "Total Worked"
        t_cell = self.s.findall("Total Worked")[-1]

        total_hours = self.s.cell(t_cell.row, t_cell.col+1).value
        total_hours = datetime.strptime(total_hours, '%H:%M:%S')

        #calculate new worked time
        new_worked_time = total_hours + worked_time
        new_worked_time = new_worked_time.strftime('%H:%M:%S')

        #save the new info in the row
        self.s.update_cell(t_cell.row, t_cell.col+1, str(new_worked_time))
