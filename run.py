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
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('stock_analyst')

stock_portfolio = SHEET.worksheet('stock_portfolio')
stock_daily_update = SHEET.worksheet('stock_daily_update')

def show_portfolio():
    data = stock_portfolio.get_all_values()
    print(data)


def delete_stock_column():
    stock_name = input("Enter the name of the stock to delete: ")
    cell = stock_portfolio.find(stock_name)
    if cell:
        stock_portfolio.delete_columns(cell.col)
        print(f"Column for stock '{stock_name}' deleted.")
    else:
        print(f"Stock '{stock_name}' not found. Please check your spelling. Otherwise the stock is not available in the list, have a look on the overview above.")


def add_stock_column():
    new_stock_name = input("Enter the name of the new stock: ")
    last_column = len(stock_portfolio.row_values(1))
    stock_portfolio.update_cell(1, last_column + 1, new_stock_name)
    print(f"New column for stock '{new_stock_name}' added.")
    new_multiplicator = input(f"Enter the new multiplicator for {stock_name} (integer): ")
    try:
        new_multiplicator = int(new_multiplicator)
        stock_portfolio.update_cell(2, cell.col, new_multiplicator)
        print(f"Multiplicator for stock '{stock_name}' updated to {new_multiplicator}.")
    except ValueError:
        print("Invalid input. Please enter a full number.")

def adjust_multiplicator():
    stock_name = input("Enter the name of the stock to adjust the multiplicator: ")
    cell = stock_portfolio.find(stock_name)
    if cell:
        new_multiplicator = input(f"Enter the new multiplicator for {stock_name} (integer): ")
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
        if len(column_values) >= 3 and column_values[-1] and column_values[-2] and column_values[-3]: # If there are non-numeric values in the columns, isdigit() will fail
            last_value = column_values[-1]
            second_last_value = column_values[-2]
            third_last_value = column_values[-3]

            # Check if the last three values are strictly increasing
            if third_last_value < second_last_value < last_value:
                stocks_increasing.append(header[col_index - 1])
                print(f"Stock {header[col_index - 1]} is increasing.")
    
            else:
                print(f"Last three values are not increasing: {header[col_index - 1]}")
        else:
            print(f"Not enough data in column: {header[col_index - 1]}")

    return stocks_increasing
    
#def show_low_performers(): similar to show_top_performer
#def calculate_profit_loss():


print('Welcome to Stock Analyst. Get an overview of your portfolio')

def main():
    show_portfolio()

    while True:
        print("\nOptions:")
        print("1: Delete a stock column")
        print("2: Add a new stock column")
        print("3: Adjust the multiplicator")
        print("4: Show top performer")
        print("5: Show low performer")
        print("6: Exit")

        choice = input("Choose an option (1, 2, 3, 4, 5, 6): ")
        
        if choice == '1':
            delete_stock_column()
        elif choice == '2':
            add_stock_column()
        elif choice == '3':
            adjust_multiplicator()
        elif choice == '4':
            increasing_stocks = show_top_performers()
            if increasing_stocks:
                print("Top performers with increasing values:", increasing_stocks) # why the loop runs 2 times?!
            else:
                print("No stocks with three times increase availabe.")
        elif choice == '5':
            decreasing_stocks = show_low_performers()
            if decreasing_stocks:
                print(data)
            else:
                print("No stocks with three times decreasing values found.")
        elif choice == '6':
            break
        else:
            print("Invalid option. Please choose again.")

        stocks_increasing = show_top_performers()
        #print("Top performers with increasing values:", stocks_increasing)

main()