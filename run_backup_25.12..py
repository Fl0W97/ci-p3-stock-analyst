# terminal of 80 characters wide and 50 rows high

# imports the whole libaries
import gspread
import os
from prettytable import PrettyTable
import datetime
import requests
import json
import time

# make sure just to import relevant parts of the libary
from google.oauth2.service_account import Credentials
from pprint import pprint
from googleapiclient.errors import HttpError

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
profit_loss_sheet = SHEET.worksheet('profit_loss')


def clear():
    os.system("clear")


def show_portfolio():
    # Show current stock portfolio

    # Get the column headers
    header = stock_portfolio.row_values(1)
    # Get 2. row of the sheet
    shares_row = stock_portfolio.row_values(2)
    # Get 2. row of the sheet
    purchase_price = stock_portfolio.row_values(4)
    # Get 2. row of the sheet
    profit_loss = profit_loss_sheet.row_values(2)

    x = PrettyTable()

    x.field_names = [
        "stock name",
        "shares",
        "purch. price",
        "curr. price",
        "surplus total"
    ]

    for col_index in range(1, len(header) + 1):
        stock_name = header[col_index - 1]  # Get stock name from the header

        # Check if col_index - 1 is within the bounds of shares_row
        if col_index - 1 < len(shares_row):
            shares = shares_row[col_index - 1]  # Get number of shares
        else:
            shares = 0  # Default value if the share data is missing

        purchase = purchase_price[col_index - 1]  # Get purchase price

        # Get the column values from stock_daily_update
        column_values = stock_daily_update.col_values(col_index)[1:]

        # Find the last non-empty value in the column
        for value in reversed(column_values):
            if value:
                current = value
                break
        else:
            current = purchase  # no values, then purchase price is used

        calculate_profit_loss()
        profloss = profit_loss[col_index - 1]  # Get total profit or loss
        x.add_row([stock_name, shares, purchase, current, profloss])

    print(x)

    # Display the update time
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Table values based on the latest manual update. \n")


def add_stock_column():
    while True:
        new_stock_name = input("Enter the name of the new stock:\n ")

        # Check if the stock already exists
        header = stock_portfolio.row_values(1)  # Get all headers in one call
        if new_stock_name in header:
            print(f"The stock '{new_stock_name}' already exists in the portfolio.")
        else:
            break

    last_column = len(header)

    # add the new stock to all three sheets
    # Use api_call_with_retry for all update operations
    api_call_with_retry(stock_portfolio.update_cell, 1, last_column + 1, new_stock_name)
    api_call_with_retry(stock_daily_update.update_cell, 1, last_column + 1, new_stock_name)
    api_call_with_retry(profit_loss_sheet.update_cell, 1, last_column + 1, new_stock_name)
    print(f"New column for stock '{new_stock_name}' added.")

    # add number of shares in row 2 in sheet stock portfolio
    new_multiplicator = input(
        f"Enter the number of shares {new_stock_name} (integer): \n"
    )
    try:
        new_multiplicator = int(new_multiplicator)
        api_call_with_retry(stock_portfolio.update_cell, 2, last_column + 1, new_multiplicator)
        api_call_with_retry(profit_loss_sheet.update_cell, 2, last_column + 1, new_multiplicator)
        print(
            f"Number of shares of {new_stock_name} "
            f"updated to {new_multiplicator}."
        )
    except ValueError:
        print("Invalid input. Please enter a full number.")

    # add inital purchase price in row 2 in sheet stock_daily_update
    purchase_price = input(
        f"Enter the stock purchase price of {new_stock_name} "
        "(float): \n"
    )

    try:
        purchase_price = float(purchase_price)
        api_call_with_retry(stock_portfolio.update_cell, 4, last_column + 1, purchase_price)
        api_call_with_retry(stock_daily_update.update_cell, 2, last_column + 1, purchase_price)
        print(f"Purchase price of '{new_stock_name}' added.")
    except ValueError:
        print("Invalid input. Please enter a float number.")

    find_stock_symbol()
    # fill blank rows in sheet stock_daily_update
    # API_stock_daily_update()


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
        print(
            f"Stock '{stock_name}' not found."
            "Please check your spelling. Otherwise the stock is not available"
            ", have a look on the overview above."
        )


def adjust_multiplicator():
    stock_name = input(
        "Enter the name of the stock to adjust the number of shares:\n "
    )
    cell = stock_portfolio.find(stock_name)
    if cell:
        new_multiplicator = input(
            f"Enter the no. of shares for {stock_name} (integer):\n "
        )
        try:
            new_multiplicator = int(new_multiplicator)
            stock_portfolio.update_cell(2, cell.col, new_multiplicator)
            print(
                f"Number of shares updated to {new_multiplicator} "
                f"for {stock_name}."
            )
        except ValueError:
            print("Invalid input. Please enter a full number.")
    else:
        print(f"Stock '{stock_name}' not found.")


def show_top_performers():
    header = stock_daily_update.row_values(1)
    stocks_increasing = []

    for col_index in range(1, len(header) + 1):
        column_values = stock_daily_update.col_values(col_index)[1:]

        # Check if there are at least 3 values and they are all numeric
        if (
            len(column_values) >= 3 and
            column_values[-1] and
            column_values[-2] and
            column_values[-3]
        ):
            last_value = column_values[-1]
            second_last_value = column_values[-2]
            third_last_value = column_values[-3]

            # Check if the last three values are strictly increasing
            if (
                third_last_value < second_last_value < last_value
            ):
                stocks_increasing.append(header[col_index - 1])

        else:
            print(
                f"Not enough data provided for {header[col_index - 1]} "
                "Please add those data in the sheet manually."
            )

    return stocks_increasing


def show_low_performers():
    header = stock_daily_update.row_values(1)
    stocks_decreasing = []

    for col_index in range(1, len(header) + 1):
        column_values = stock_daily_update.col_values(col_index)[1:]

        # Check if there are at least 3 values
        if (
            len(column_values) >= 3 and
            column_values[-1] and
            column_values[-2] and
            column_values[-3]
        ):
            last_value = column_values[-1]
            second_last_value = column_values[-2]
            third_last_value = column_values[-3]

            # Check if the last three values are strictly decreasing
            if third_last_value > second_last_value > last_value:
                stocks_decreasing.append(header[col_index - 1])

        else:
            print(
                f"Not enough data provided for {header[col_index - 1]} "
                "Please add those data in the sheet manually."
            )

    return stocks_decreasing


def calculate_profit_loss():
    header = stock_daily_update.row_values(1)
    rows = stock_portfolio.get_all_values()  # Fetch all rows in one call
    purchase_price_column = rows[3]  # Row for purchase prices
    multiplicator_row = rows[1]  # Row for shares
    
    # Fetch all column values in one call
    all_column_values = stock_daily_update.get_all_values()[1:]  # Skip header row

    # List for profit and loss values
    surplus_data = []
    percentage_data = []

    for col_index in range(1, len(header) + 1):
        # Access the purchase price safely
        try:
            purchase_price = purchase_price_column[col_index - 1]
        except IndexError:
            print(f"Error: Purchase price missing for column {header[col_index - 1]}")
            continue

        # Extract the specific column values wihtout API request
        column_values = [row[col_index - 1] for row in all_column_values]  

        # Check for empty column or missing data
        if not column_values or len(column_values) < 1:
            print(f"Error: Missing/wrong data for column {header[col_index - 1]}")
            continue

        last_column_value = column_values[-1]

        try:
            first_value = float(purchase_price)
            last_value = float(last_column_value)
        except ValueError:
            print(f"Non-numeric data found in column: {header[col_index - 1]}")
            continue

        # Calculate profit/loss
        profit_loss_value = last_value - first_value
        rounded_profit_loss_value = round(profit_loss_value, 2)

        if first_value != 0:
            rounded_profit_loss_value_percentage = (last_value - first_value) / first_value * 100
        else:
            rounded_profit_loss_value_percentage = 0

        # Fetch multiplicator safely
        try:
            multiplicator = float(multiplicator_row[col_index - 1])
        except IndexError:
            print(f"Error: Number of shares missing for column {header[col_index - 1]}")
            continue

        # Calculate surplus based on multiplicator
        surplus = multiplicator * rounded_profit_loss_value

        # Append results
        surplus_data.append(surplus)
        percentage_data.append(round(rounded_profit_loss_value_percentage, 2))

        # Update Google Sheets in a single call
        profit_loss_sheet.update(range_name='2:3', values=[surplus_data, percentage_data])

    return surplus_data


def column_check():
    # check stock_portfolio
    header = stock_portfolio.row_values(1)
    shares = stock_portfolio.row_values(2)
    symbols = stock_portfolio.row_values(3)
    purchase_price = stock_portfolio.row_values(4)

    if len(header) == len(shares) == len(symbols) == len(purchase_price):
        return True

    else:
        print(
            "Check sheet stock_portfolio. The lenght of the rows "
            "are not equal. Data is missing. "
            "Adjust it manually in the sheet stock_portfolio"
        )
        return False

    # check stock_daily_update
    header = stock_daily_update.row_values(1)
    purchase_price = stock_daily_update.row_values(2)

    if len(header) == len(purchase_price):
        return True

    else:
        print(
            f"Check sheet stock_daily_update. The lenght of the rows "
            "are not equal. Data is missing. "
            "Adjust it manually in the sheet stock_daily_update."
        )
        return False

    # check profit_loss_sheet
    header = profit_loss_sheet.row_values(1)
    surplus = profit_loss_sheet.row_values(2)

    if len(header) == len(surplus):
        return True

    else:
        print(
            f"Check sheet profit_loss. The lenght of the rows "
            "are not equal. Data is missing. "
            "Adjust it manually in the sheet profit_loss."
        )
        return False


def provide_updated_data():
    # show relevant data for stock_daily_update in the terminal
    symbol = stock_portfolio.row_values(3)  # Get the abbrevation of the stocks

    for col_index in range(len(symbol)):

        stock_name_symbol = symbol[col_index]  # Get one abbr. for each column
        url = (
            f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&'
            f'symbol={stock_name_symbol}&apikey='
            f'{os.environ.get("alphaventage-api")}'
        )
        r = requests.get(url)
        data = r.json()

        # Check if 'Time Series (Daily)' key exists in the JSON response
        if 'Time Series (Daily)' in data:
            time_series = data['Time Series (Daily)']
            dates = list(time_series.keys())
            dates.sort(reverse=True)

            if len(dates) > 1:
                second_date = dates[1]
                second_date_data = time_series[second_date]
                desired_value = second_date_data['4. close']

                print(
                    f"The latest price from {stock_name_symbol} is: "
                    f"{float(desired_value):.2f}. "
                    "You can add it to the last column of "
                    "googlesheet 'stock_daily_update'."
                )

            else:
                print(f"Not enough data points for {stock_name_symbol}.")

        else:
            print(
                f"for {stock_name_symbol}. "
                "Standard API rate limit is 25 requests per day. "
                "Check the prices here: https://finance.yahoo.com/quote/MSFT/history/"
            )


def find_stock_symbol():
    # define stock name. Use it for the API request
    header = stock_portfolio.row_values(1)
    new_stock_name = header[-1]

    # API request URL
    url = (
        'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords='
        f'{new_stock_name}&apikey={os.environ.get("alphaventage-api")}'
    )

    r = requests.get(url)
    data = r.json()

    # Check if the API request was successful
    if r.status_code == 200:
        print("Connection to the API was successful.")

        # inform the user
        print(
            f"Here are different stock symbols of {new_stock_name}. "
            "Choose one exact stock symbol to proceed."
        )

        # Check if 'bestMatches' key exists in the JSON response
        if 'bestMatches' in data:
            best_matches = data['bestMatches']

            # Extract symbols and names
            symbols_and_names = [
                (match['1. symbol'], match['2. name'])
                for match in best_matches
            ]

            # Print the symbols and names
            for symbol, name in symbols_and_names:
                print(f"Symbol: {symbol}, Name: {name}")
        else:
            print(
                "Conenction to the API was not successful. "
                "Enter the symbol manually or wait "
                "until the connection is established again. "
            )

        # update the stock portfolio sheet
        third_row = stock_portfolio.row_values(3)
        last_column = len(third_row) + 1

        # input a new stock symbol from the user
        new_stock_name_symbol = input("Enter the symbol of the new stock:\n ")

        # update the sheet with the new stock name and symbol in third row
        stock_portfolio.update_cell(3, last_column, new_stock_name_symbol)

        print(f"Symbol for {new_stock_name} is added.")

    else:
        print(
            f"Failed to retrieve data from API: {r.status_code}. "
            "Please add it manually."
        )


def api_call_with_retry(api_method, *args, **kwargs):
    """
    This function wraps an API call with retry logic.
    It will retry up to  times in case of a 500 or 503 error
    or any other recoverable error.
    """
    max_retries = 5
    backoff_factor = 2  # Exponential backoff factor
    attempt = 0
    
    while attempt < max_retries:
        try:
            # Call the actual Google API method
            return api_method(*args, **kwargs)
        
        except HttpError as error:
            # Retry only on certain HTTP errors (500 and 503)
            if error.resp.status in [500, 503]:
                attempt += 1
                wait_time = backoff_factor ** attempt  # Exponential backoff
                print(f"Retrying... Attempt {attempt}/{max_retries}. Waiting {wait_time} seconds.")
                time.sleep(wait_time)
            else:
                # If the error is not recoverable (other status codes), raise it
                print(f"API call failed with error: {error}")
                raise
        except Exception as e:
            # Catch any other exceptions (e.g., network-related errors)
            print(f"An unexpected error occurred: {e}")
            raise
        
    # If we reached here, all attempts failed
    print(f"Failed after {max_retries} attempts.")
    raise Exception("API call failed after multiple attempts.")


print('Welcome to Stock Analyst. Get an overview and manage your portfolio\n')


def main():

    # column_check()

    while True:

        show_portfolio()
        print("\nOptions:")
        print("1: Add a new stock")
        print("2: Delete a stock")
        print("3: Adjust the number of shares")
        print("4: Show current top performer")
        print("5: Show current low performer")
        print("6: Show latest stock prices")
        print("7: Exit")

        choice = input("Choose an option (1, 2, 3, 4, 5, 6, 7): ")

        if choice == '1':
            add_stock_column()
            time.sleep(5)
            clear()
        elif choice == '2':
            delete_stock_column()
            time.sleep(5)
            clear()
        elif choice == '3':
            adjust_multiplicator()
            time.sleep(5)
            clear()
        elif choice == '4':
            increasing_stocks = show_top_performers()
            if increasing_stocks:
                print(
                    "Current top performer(s) of the last three days: ",
                    ", ".join(increasing_stocks)
                )
            else:
                print("No stocks with three times increase availabe.")
            time.sleep(10)
            clear()
        elif choice == '5':
            decreasing_stocks = show_low_performers()
            if decreasing_stocks:
                print(
                    "Current low performer(s) of last three days: ",
                    ", ".join(decreasing_stocks)
                )
            else:
                print("No stocks with three times decrease availabe.")
            time.sleep(10)
            clear()
        elif choice == '6':
            provide_updated_data()
            time.sleep(20)
            clear()
        elif choice == '7':
            break
        else:
            print("Invalid option. Please choose again.")


main()
