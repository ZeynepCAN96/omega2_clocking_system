import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('omega_ned.json', scope)
client = gspread.authorize(creds)

if __name__ == '__main__':
    sheet = client.open('timeclock_system').sheet1

    pp = pprint.PrettyPrinter()

    #to get all the records in the file
    #data = sheet.get_all_records()

    #to get all the values inside the file
    #data = sheet.get_all_values()

    #to get exact row values in a second row (Since 1st row is the header)
    #data = sheet.row_values(7)

    #to get all the column values in the column 'place'
    #data = sheet.col_values(1)

    #to extract a particular cell value (row, column)
    #data = sheet.cell(7, 1).value

    #pp.pprint(data)


    #Insert data into sheet
    # row = ["I'm","inserting","a","new","row","into","a,","Spreadsheet","using","Python"]
    #
    # index = 3
    # sheet.insert_row(row, index)

    sheet.update_cell(1, 1, "telemedicine_id")
