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

#def show_low_performers():


#def show_top_performers():


#def calculate_profit_loss():


print('Welcome to Stock Analyst. Get an overview of your portoflio')

def main():
    show_portfolio()

    while True:
        print("\nOptions:")
        print("1: Delete a stock column")
        print("2: Add a new stock column")
        print("3: Adjust the multiplicator")
        print("4: Exit")

        choice = input("Choose an option (1, 2, 3, 4): ")
        
        if choice == '1':
            delete_stock_column()
        elif choice == '2':
            add_stock_column()
        elif choice == '3':
            adjust_multiplicator()
        elif choice == '4':
            break
        else:
            print("Invalid option. Please choose again.")
 
main()