# Write your code to expect a terminal of 80 characters wide and 24 rows high

# imports the whole libary
import gspread

#make sure just to import relevant parts of the libary
from google.oauth2.service_account import Credentials 
from pprint import pprint

# IAM - list of google-APIs that the program should access in order to run
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('stock_analyst')

#sales = SHEET.worksheet('sales')
#data = sales.get_all_values()
#print(data)




def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
    
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print('Data is valid!')
            break

    return sales_data

def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """

    print(values)

    try:
        [int(value) for value in values] #converts each value to an integer
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again \n")
        return False

    return True


def update_surplus_worksheet(data):
    """
    Update surplus worksheet, add new row with the list data provided.
    """
    print('Updating surplus worksheet...\n')
    surplus_worksheet = SHEET.worksheet('surplus')
    surplus_worksheet.append_row(data)
    print("surplus worksheet updated successfully.\n")


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print('Updating sales worksheet...\n')
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print("sales worksheet updated successfully.\n")


def update_worksheet(data, worksheet):
    """
    Update worksheets, add new row with the list data provided.
    """
    print(f'Updating {worksheet} worksheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet} worksheet updated successfully.')


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print('Calculating surplus data... \n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data


def get_last_5_entries_sales():
    """
    """
    sales = SHEET.worksheet('sales')

    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns


def calculate_stock_data(data):
    """
    Calculate the everage stock for each item type, adding 10%
    """
    print('Calculating stock data...\n')
    new_stock_data = []

    for colum in data:
        int_column = [int(num) in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    print(new_stock_data)


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    calculate_surplus_data(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data,'surplus')
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, 'stock')

print('Welcome to Love Sandwiches Data Automation')
main()



def show_low_performers():
    header = stock_daily_update.row_values(1)
    stocks_decreasing = []
    
    for col_index in range(1, len(header) + 1):
        column_values = stock_daily_update.col_values(col_index)[1:]  # Exclude header

        # Check if there are at least 3 values and they are all numeric
        if len(column_values) >= 3 and column_values[-1].isdigit() and column_values[-2].isdigit() and column_values[-3].isdigit():
            last_value = int(column_values[-1])
            second_last_value = int(column_values[-2])
            third_last_value = int(column_values[-3])

        # Check if the last three values are strictly increasing
            if third_last_value > second_last_value > last_value:
                stocks_decreasing.append(header[col_index - 1])
    
    return stocks_decreasing