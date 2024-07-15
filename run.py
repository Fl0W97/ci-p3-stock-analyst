# Write your code to expect a terminal of 80 characters wide and 50 rows high

# imports the whole libary
import gspread
import os
from prettytable import PrettyTable
import datetime
import requests
import json

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
    #Correct profit_loss result
    header = stock_portfolio.row_values(1) # Get the column headers
    shares_row = stock_portfolio.row_values(2) # Get the second row which contains the number of shares
    purchase_price = stock_daily_update.row_values(2)
    profit_loss = profit_loss_sheet.row_values(2)

    total_rows = len(stock_daily_update.get_all_values())
    current_price = stock_daily_update.row_values(total_rows)

    x = PrettyTable()
    
    x.field_names = ["stock name", "shares", "purch. price", "curr. price", "surplus total"]


    for col_index in range(len(header)):
        stock_name = header[col_index -1] # Get the stock name from the header
        shares = shares_row[col_index -1] # Get the corresponding number of shares
        purchase = purchase_price[col_index -1]  # Get the purchase price
        current = current_price[col_index -1]  # Get the current price
        profloss = profit_loss[col_index -1] # Get the total profit or loss
        x.add_row([stock_name, shares, purchase, current, profloss])

    print(x)

    # Display the update time
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Update completed at: {update_time}\n")


def add_stock_column():
    while True:
        new_stock_name = input("Enter the name of the new stock:\n ")

        # Check if the stock already exists
        cell = stock_portfolio.find(new_stock_name)
        if cell is not None:
            print(f"The stock '{new_stock_name}' already exists in the portfolio.")
        else:
            break

    last_column = len(stock_portfolio.row_values(1))

    # Add the new stock to all three sheets
    stock_portfolio.update_cell(1, last_column + 1, new_stock_name)
    stock_daily_update.update_cell(1, last_column + 1, new_stock_name)
    profit_loss_sheet.update_cell(1, last_column + 1, new_stock_name)
    print(f"New column for stock '{new_stock_name}' added.")

    # Add number of shares in row 2 in sheet stock portfolio
    new_multiplicator = input(f"Enter the number of shares {new_stock_name} (integer): \n")
    try:
        new_multiplicator = int(new_multiplicator)
        stock_portfolio.update_cell(2, last_column + 1, new_multiplicator)
        profit_loss_sheet.update_cell(2, last_column + 1, new_multiplicator)
        print(f"Number of shares of '{new_stock_name}' updated to {new_multiplicator}.")
        find_stock_symbol()
    except ValueError:
        print("Invalid input. Please enter a full number.")

    #Add inital purchase price in row 2 in sheet stoy daily update
    purchase_price = input(f"Enter the stock purchase price of {new_stock_name} (float): \n")
    try:
        purchase_price = float(purchase_price)
        stock_daily_update.update_cell(2, last_column + 1, purchase_price)
        print(f"Purchase price of '{new_stock_name}' added.")
    except ValueError:
        print("Invalid input. Please enter a float number.")

    find_stock_symbol()


def delete_stock_column():
    # delete stock name, header and column on all sheets
    stock_name = input("Enter the name of the stock you want to delete:\n ")
    cell = stock_portfolio.find(stock_name)
    cell1 = stock_daily_update.find(stock_name)
    cell2 = profit_loss_sheet.find(stock_name)
    if cell:
        stock_portfolio.delete_columns(cell.col)
        stock_daily_update.delete_columns(cell1.col)
        profit_loss_sheet.delete_columns(cell2.col)
        print(f"Column for stock '{stock_name}' deleted.")
    else:
        print(f"Stock '{stock_name}' not found. Please check your spelling. Otherwise the stock is not available in the list, have a look on the overview above.")


def adjust_multiplicator():
    stock_name = input("Enter the name of the stock to adjust the number of shares:\n ")
    cell = stock_portfolio.find(stock_name)
    if cell:
        new_multiplicator = input(f"Enter the new multiplicator for {stock_name} (integer):\n ")
        try:
            new_multiplicator = int(new_multiplicator)
            stock_portfolio.update_cell(2, cell.col, new_multiplicator)
            print(f"Number of shares updated to {new_multiplicator} for {stock_name}.")
        except ValueError:
            print("Invalid input. Please enter a full number.")
    else:
        print(f"Stock '{stock_name}' not found.")


def show_top_performers():
    #connect to API
    header = stock_daily_update.row_values(1)
    stocks_increasing = []
    
    for col_index in range(1, len(header) + 1):
        column_values = stock_daily_update.col_values(col_index)[1:]  # Exclude header
#        print(f"Processing column: {header[col_index - 1]}")
#        print(f"Column values: {column_values}")

        # Check if there are at least 3 values and they are all numeric
        if len(column_values) >= 3 and column_values[-1] and column_values[-2] and column_values[-3]:
            last_value = column_values[-1]
            second_last_value = column_values[-2]
            third_last_value = column_values[-3]

            # Check if the last three values
            if third_last_value < second_last_value < last_value:
                stocks_increasing.append(header[col_index - 1])
#                print(f"Stock {header[col_index - 1]} is increasing.")
    
#            else:
#                print(f"Last three values are not increasing: {header[col_index - 1]}")
        else:
            print(f"Not enough data in column: {header[col_index - 1]}")

    return stocks_increasing


def show_low_performers():
    #connect to API
    header = stock_daily_update.row_values(1)
    stocks_decreasing = []
    
    for col_index in range(1, len(header) + 1):
        column_values = stock_daily_update.col_values(col_index)[1:]  # Exclude header
#        print(f"Processing column: {header[col_index - 1]}")
#        print(f"Column values: {column_values}")

        # Check if there are at least 3 values
        if len(column_values) >= 3 and column_values[-1] and column_values[-2] and column_values[-3]:
            last_value = column_values[-1]
            second_last_value = column_values[-2]
            third_last_value = column_values[-3]

            # Check if the last three values are strictly increasing
            if third_last_value > second_last_value > last_value:
                stocks_decreasing.append(header[col_index - 1])
#                print(f"Stock {header[col_index - 1]} is decreasing.")
    
#            else:
#                print(f"Last three values are not decreasing: {header[col_index - 1]}")
        else:
            print(f"Not enough data in column: {header[col_index - 1]}")

    return stocks_decreasing    


def calculate_profit_loss(): # ERROR!
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


def column_check():
    #check stock_portfolio
    header = stock_portfolio.row_values(1)
    shares = stock_portfolio.row_values(2)
    symbols = stock_portfolio.row_values(3)  
    
    if len(header) == len(shares) == len(symbols):
        print("stock_portfolio is correctly filled out.")

    else: 
        print(f"Check sheet stock_portfolio. The lenght of the rows are not equal.")

    #check stock_daily_update
    header = stock_daily_update.row_values(1)
    purchase_price = stock_daily_update.row_values(2)
    price1 = stock_daily_update.row_values(3)
    price2 = stock_daily_update.row_values(3)
    price3 = stock_daily_update.row_values(3)

    if len(header) == len(shares) & len(symbols):
        print("stock_daily_update is correctly filled out.")

    else: 
        print(f"Check sheet stock_daily_update. The lenght of the rows are not equal.")
    
    #check profit_loss_sheet
    header = profit_loss_sheet.row_values(1)
    surplus = profit_loss_sheet.row_values(2)

    if len(header) == len(shares) == len(symbols):
        print("profit_loss_sheet is correctly filled out.")

    else: 
        print(f"Check sheet profit_loss. The lenght of the rows are not equal.")

# work in process
def API_stock_daily_update():
    # Update last three rows of sheet stock_daily_update
    symbol = stock_portfolio.row_values(3) # Get the abbrevation of the stocks

    for col_index in range(len(symbol)):
        stock_name_symbol = symbol[col_index] # Get one abbrevation for each column        
        
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_name_symbol}&apikey=HULMNKWD3NVXSA0D'

        # Request data from the API
        r = requests.get(url)
            
        # Check if the request was successful
        if r.status_code == 200:
            data = r.json()

            # Check if 'Time Series (Daily)' key exists in the JSON response
            if 'Time Series (Daily)' in data:
                time_series = data['Time Series (Daily)']

                # Get the relevant dates from the stock_daily_update sheet (column 5, rows 2-4)
                dates = stock_daily_update.col_values(5)[1:4]
                
                # Extract the close values for these dates
                close_values = []
                for date in dates:
                    if date in time_series:
                        close_values.append(time_series[date]['4. close'])
                    else:
                        close_values.append('N/A')  # Handle the case where the date is not in the API response
                
                # Update the corresponding cells in stock_daily_update
                for i, value in enumerate(close_values):
                        stock_daily_update.update_cell(i + 2, col_index + 1, value)
            else:
                print(f"Error: 'Time Series (Daily)' not found for {stock_name_symbol}")

        else:
            print(f"Failed to retrieve data: {r.status_code}. Since the API doesn't provide data, the sheet stock_daily_update is not updated. You have to do it manually. The data are provided here: https://finance.yahoo.com/quote/MSFT/history/")


def provide_updated_data():
    #Show relevant data for stock_daily_update in the terminal
    symbol = stock_portfolio.row_values(3) # Get the abbrevation of the stocks
    
    for col_index in range(len(symbol)):

        stock_name_symbol = symbol[col_index] # Get one abbrevation for each column        
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_name_symbol}&apikey=HULMNKWD3NVXSA0D'

        r = requests.get(url)
        data = r.json()

        # Check if 'Time Series (Daily)' key exists in the JSON response
        if 'Time Series (Daily)' in data:
            time_series = data['Time Series (Daily)']
            dates = list(time_series.keys())
            dates.sort(reverse=True)
        
            second_date = dates[1]
            second_date_data = time_series[second_date]
            desired_value = second_date_data['4. close']

            print(f" The latest price from {stock_name_symbol} is: (desired_value). You can add it to the last column of googlesheet 'stock_daily_update'.") # (desired value, ist it the variable which is diplayed at the end? - TEST)
        else:
            print(f" Currently, there are no live data available for {stock_name_symbol}. Standard API rate limit is 25 requests per day.")


def find_stock_symbol():
    # Use an f-string to insert the new_stock_name into the URL
    url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=IBM&apikey=HULMNKWD3NVXSA0D'
    r = requests.get(url)

    # Check if the API request was successful
    if r.status_code == 200:
        print("Conenction to the API was successful.")

        # find a symbol for the stock name and use it for the API request
        header = stock_portfolio.row_values(1)
        new_stock_name = header[-1]
        print(f"Here are different stock symbols of {new_stock_name}. Choose one exact stock symbol to procced.")
    
        # Use an f-string to insert the new_stock_name into the URL
        url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={new_stock_name}&apikey=HULMNKWD3NVXSA0D'
        r = requests.get(url)
        data = r.json()
 
        # Check if 'bestMatches' key exists in the JSON response
        if 'bestMatches' in data:
            best_matches = data['bestMatches']

            # Extract symbols and names
            symbols_and_names = [(match['1. symbol'], match['2. name']) for match in best_matches]

            # Print the symbols and names
            for symbol, name in symbols_and_names:
                print(f"Symbol: {symbol}, Name: {name}\n")
        else:
            print("No 'bestMatches' found in the response.")

        # Update the stock portfolio sheet
        third_row = stock_portfolio.row_values(3)
        last_column = len(third_row) +1

        #input a new stock symbol from the user
        new_stock_name_symbol = input("Enter the symbol of the new stock:\n ")

        # Update the sheet with the new stock name and symbol in third row
        stock_portfolio.update_cell(3, last_column, new_stock_name_symbol)
    
    else:
        print(f"Failed to retrieve data: {r.status_code}. Since the API don't provides data sheet the stock symbol is not updated.")


print('Welcome to Stock Analyst. Get an overview and manage your portfolio\n')
def main():
    
    show_portfolio()
    # add ascci art! https://www.youtube.com/watch?v=Y0QiBbI3MWs, https://www.geeksforgeeks.org/generate-simple-ascii-tables-using-prettytable-in-python/, https://github.com/ericm/stonks

    column_check()

    while True:
        
        print("\nOptions:")
        print("1: Add a new stock")
        print("2: Delete a stock")
        print("3: Adjust the number of shares")
        print("4: Show current top performer")
        print("5: Show current low performer")
        print("6: Show profit and loss")
        print("7: Show latest stock prices")
        print("8: Exit")

        choice = input("Choose an option (1, 2, 3, 4, 5, 6, 7, 8): ")

        if choice == '1':
            clear()
            show_portfolio()
            add_stock_column()
            show_portfolio()
        elif choice == '2':
            clear()
            show_portfolio()
            delete_stock_column()
            show_portfolio()
        elif choice == '3':
            clear()
            show_portfolio()
            adjust_multiplicator()
            show_portfolio()
        elif choice == '4':
            clear()
            show_portfolio()
            increasing_stocks = show_top_performers()
            if increasing_stocks:
                print("Current top performers with last three days increasing values:", increasing_stocks)
            else:
                print("No stocks with three times increase availabe.")
        elif choice == '5':
            clear()
            show_portfolio()
            decreasing_stocks = show_low_performers()
            if decreasing_stocks:
                print("Current low performers with last three days decreasing values:", decreasing_stocks)
            else:
                print("No stocks with three times decrease availabe.")
        elif choice == '6':
            clear()
            show_portfolio()
            calculate_profit_loss()
        elif choice == '7':
            clear()
            show_portfolio()
            provide_updated_data()
        elif choice == '8':
            break
        else:
            print("Invalid option. Please choose again.")

main()