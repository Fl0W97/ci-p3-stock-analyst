# Write your code to expect a terminal of 80 characters wide and 24 rows high

# imports the whole libary
import gspread
import os
from prettytable import PrettyTable

#make sure just to import relevant parts of the libary
from google.oauth2.service_account import Credentials 
from pprint import pprint

# IAM - list of google-APIs that the program should access in order to run
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

clear = lambda: os.system("clear")

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('stock_analyst')

stock_portfolio = SHEET.worksheet('stock_portfolio')
stock_daily_update = SHEET.worksheet('stock_daily_update')
profit_loss_sheet = SHEET.worksheet('profit_loss')

def show_portfolio():
    #Show current stock portfolio
    #add last update date
    header = stock_portfolio.row_values(1) # Get the column headers
    shares_row = stock_portfolio.row_values(2) # Get the second row which contains the number of shares
    x = PrettyTable()
    
    x.field_names = ["stock name", "shares"]


    for col_index in range(len(header)):
        stock_name = header[col_index -1] # Get the stock name from the header
        shares = shares_row[col_index -1] # Get the corresponding number of shares
        x.add_row([stock_name, shares])
        #print(f"Stock: {stock_name}. No. of shares {shares}")

    print(x)

def delete_stock_column():
    stock_name = input("Enter the name of the stock to delete:\n ")
    cell = stock_portfolio.find(stock_name)
    if cell:
        stock_portfolio.delete_columns(cell.col)
        print(f"Column for stock '{stock_name}' deleted.")
    else:
        print(f"Stock '{stock_name}' not found. Please check your spelling. Otherwise the stock is not available in the list, have a look on the overview above.")


def add_stock_column():
    new_stock_name = input("Enter the name of the new stock:\n ")
    last_column = len(stock_portfolio.row_values(1))
    stock_portfolio.update_cell(1, last_column + 1, new_stock_name)
    print(f"New column for stock '{new_stock_name}' added.")
    new_multiplicator = input(f"Enter the new multiplicator for {stock_name} (integer): \n")
    try:
        new_multiplicator = int(new_multiplicator)
        stock_portfolio.update_cell(2, cell.col, new_multiplicator)
        print(f"Multiplicator for stock '{stock_name}' updated to {new_multiplicator}.")
    except ValueError:
        print("Invalid input. Please enter a full number.")

def adjust_multiplicator():
    stock_name = input("Enter the name of the stock to adjust the multiplicator:\n ")
    cell = stock_portfolio.find(stock_name)
    if cell:
        new_multiplicator = input(f"Enter the new multiplicator for {stock_name} (integer):\n ")
        try:
            new_multiplicator = int(new_multiplicator)
            stock_portfolio.update_cell(2, cell.col, new_multiplicator)
            print(f"Multiplicator for stock '{stock_name}' updated to {new_multiplicator}.")
        except ValueError:
            print("Invalid input. Please enter a full number.")
    else:
        print(f"Stock '{stock_name}' not found.")


def show_top_performers():
    header = stock_daily_update.row_values(1)
    stocks_increasing = []
    
    for col_index in range(1, len(header) + 1):
        column_values = stock_daily_update.col_values(col_index)[1:]  # Exclude header
        print(f"Processing column: {header[col_index - 1]}")
        print(f"Column values: {column_values}")

        # Check if there are at least 3 values and they are all numeric
        if len(column_values) >= 3 and column_values[-1] and column_values[-2] and column_values[-3]:
            last_value = column_values[-1]
            second_last_value = column_values[-2]
            third_last_value = column_values[-3]

            # Check if the last three values
            if third_last_value < second_last_value < last_value:
                stocks_increasing.append(header[col_index - 1])
                print(f"Stock {header[col_index - 1]} is increasing.")
    
            else:
                print(f"Last three values are not increasing: {header[col_index - 1]}")
        else:
            print(f"Not enough data in column: {header[col_index - 1]}")

    return stocks_increasing
    
def show_low_performers():
    header = stock_daily_update.row_values(1)
    stocks_decreasing = []
    
    for col_index in range(1, len(header) + 1):
        column_values = stock_daily_update.col_values(col_index)[1:]  # Exclude header
        print(f"Processing column: {header[col_index - 1]}")
        print(f"Column values: {column_values}")

        # Check if there are at least 3 values
        if len(column_values) >= 3 and column_values[-1] and column_values[-2] and column_values[-3]:
            last_value = column_values[-1]
            second_last_value = column_values[-2]
            third_last_value = column_values[-3]

            # Check if the last three values are strictly increasing
            if third_last_value > second_last_value > last_value:
                stocks_decreasing.append(header[col_index - 1])
                print(f"Stock {header[col_index - 1]} is decreasing.")
    
            else:
                print(f"Last three values are not decreasing: {header[col_index - 1]}")
        else:
            print(f"Not enough data in column: {header[col_index - 1]}")

    return stocks_decreasing    

def calculate_profit_loss():
    header = stock_daily_update.row_values(1)

    surplus_data = [] # List to hold the profit and loss values to be added to the new worksheet
    profit_loss_data = [] 

    for col_index in range(1, len(header) + 1):
        column_values = stock_daily_update.col_values(col_index)[1:]  # Exclude header
        first_column_value = column_values[0]
        last_column_value = column_values[-1]

        # take the last value of a column and substract the first value of the column from sheet stock_daily_update
        profit_loss_value = float(last_column_value) - float(first_column_value)
        rounded_profit_loss_value = round(profit_loss_value, 2)
        rounded_profit_loss_value_percentage = ((float(first_column_value) - float(last_column_value)) / float(first_column_value))* 100

        print(f" Processing column: {header[col_index - 1]}\n")
        print(f" First value in column {header[col_index - 1]} is: + {first_column_value}")
        print(f" Last value in column {header[col_index - 1]} is: + {last_column_value}")

        multiplicator_row = stock_portfolio.row_values(2) 

        #validation in case there is a column or value missing
        if col_index - 1 >= len(multiplicator_row):
            print(f"Error: Multiplicator missing for column {header[col_index - 1]}")
            return

        # multiply the value with the multiplicator in the second row from sheet stock_portfolio
        surplus = float(multiplicator_row[col_index - 1]) * rounded_profit_loss_value
        print(f"profit_loss is in total: {surplus}\n")
        print(f"percentage of profit_loss is in total: {int(rounded_profit_loss_value_percentage)}%\n")
        
        # Add the profit_loss_value to the list above profit_loss_data
        profit_loss_data.append(surplus)
        surplus_data.append(surplus)

    # add/update the value to the second row of sheet profit_and_loss
    profit_loss_sheet.update(f'2:2', [surplus_data])  # Update the second row with the surplus_data

    return surplus_data


#        profit_loss_total_minus_brokerfee
#        profit_loss_total_minus_brokerfee_minus_taxes #ignore free german allowance right now, maybe add later - only pay tax when surplus is positive

#        if profit_loss_total_minus_brokerfee_minus_taxes > 0:
#            print(f"Profit!")
#        else:
#            print(f"Loss!")
#       clear function each time the user selects an option / clear terminal

# def live_or_static():
#       ask the user if he wants to use the static sheet or the API sheet with automatically updated data
#       
# def health_check
#       if API sheet is accessable and working, then show the API data otherwise switch and use the static sheets
#       () 


print('Welcome to Stock Analyst. Get an overview and manage of your portfolio')
def main():
    show_portfolio()
    # add ascci art! https://www.youtube.com/watch?v=Y0QiBbI3MWs, https://www.geeksforgeeks.org/generate-simple-ascii-tables-using-prettytable-in-python/, https://github.com/ericm/stonks

    while True:
        

        print("\nOptions:")
        print("1: Delete a stock column")
        print("2: Add a new stock column")
        print("3: Adjust the multiplicator")
        print("4: Show top performer")
        print("5: Show low performer")
        print("6: Show profit and loss")
        print("7: Exit")
        #print("8: Show me a graphic from stock: ")

        choice = input("Choose an option (1, 2, 3, 4, 5, 6, 7): ")

        if choice == '1':
            clear()
            delete_stock_column()
        elif choice == '2':
            clear()
            add_stock_column()
        elif choice == '3':
            clear()
            adjust_multiplicator()
        elif choice == '4':
            clear()
            increasing_stocks = show_top_performers()
            if increasing_stocks:
                print("Top performers with increasing values:", increasing_stocks)
            else:
                print("No stocks with three times increase availabe.")
        elif choice == '5':
            clear()
            decreasing_stocks = show_low_performers()
            if decreasing_stocks:
                print("Low performers with increasing values:", decreasing_stocks)
            else:
                print("No stocks with three times decrease availabe.")
        elif choice == '6':
            clear()
            calculate_profit_loss()
        elif choice == '7':
            break
        else:
            print("Invalid option. Please choose again.")

        show_portfolio()

main()