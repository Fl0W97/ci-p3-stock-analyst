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
profit_loss_sheet = SHEET.worksheet('profit_loss')


def clear():
    os.system("clear")


def show_portfolio():
    # Show current stock portfolio

    # Get the column headers
    header = stock_portfolio.row_values(1)
    # Get 2. row of the sheet
    shares_row = stock_portfolio.row_values(2)
    # Get 4. row of the sheet
    purchase_price = stock_portfolio.row_values(4)
    # Get 3. row of the sheet
    profit_loss_percentage = profit_loss_sheet.row_values(3)
    # Get 2. row of the sheet
    profit_loss = profit_loss_sheet.row_values(2)
    # Get 5. row of sheet
    current_price = stock_portfolio.row_values(5)

    x = PrettyTable()

    x.field_names = [
        "stock name",
        "shares",
        "purch. price",
        "current price",
        "surplus p.",
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

        current = current_price[col_index - 1]  # Get current price

        calculate_profit_loss()
        profloss = profit_loss[col_index - 1]  # Get total profit or loss
        profloss_percentage = profit_loss_percentage[col_index - 1]  # Get profit or loss percentage

        x.add_row([stock_name, shares, purchase, current, profloss_percentage, profloss])

    print(x)

    # Display the update time
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Table values based on the latest manual update. \n")


def add_stock_column():
    while True:
        new_stock_name = get_valid_input("Enter the name of the new stock:\n ", input_type=str)

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
    api_call_with_retry(profit_loss_sheet.update_cell, 1, last_column + 1, new_stock_name)
    print(f"New column for stock '{new_stock_name}' added.")

    # add number of shares in row 2 in sheet stock portfolio
    new_multiplicator = get_valid_input(
        f"Enter the number of shares {new_stock_name} (integer): \n", input_type=int
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
    purchase_price = get_valid_input(
        f"Enter the stock purchase price of {new_stock_name} "
        "(float): \n", input_type=float
    )

    try:
        purchase_price = float(purchase_price)
        api_call_with_retry(stock_portfolio.update_cell, 4, last_column + 1, purchase_price)
        print(f"Purchase price of '{new_stock_name}' added.")
    except ValueError:
        print("Invalid input. Please enter a float number.")

    # add current price
    api_call_with_retry(stock_portfolio.update_cell, 5, last_column + 1, purchase_price)

    find_stock_symbol()


def delete_stock_column():
    # delete stock name, header and column on all sheets
    stock_name = input("Enter the name of the stock you want to delete:\n ")
    cell = stock_portfolio.find(stock_name)
    cell2 = profit_loss_sheet.find(stock_name)
    if cell:
        stock_portfolio.delete_columns(cell.col)
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


def calculate_profit_loss():
    header = stock_portfolio.row_values(1)  # Get the column headers
    rows = stock_portfolio.get_all_values()  # Fetch all rows in one call
    purchase_price_column = rows[3]  # Row for purchase prices
    current_price_column = rows[4] # Row for current prices
    multiplicator_row = rows[1]  # Row for shares
    
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

        # Access the current price safely
        try:
            current_price = current_price_column[col_index - 1]
        except IndexError:
            print(f"Error: Purchase price missing for column {header[col_index - 1]}")
            continue


        try:
            first_value = float(purchase_price)
            last_value = float(current_price)
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
    # show data stock in the terminal
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
                )

            else:
                print(f"Not enough data points for {stock_name_symbol}.")

        else:
            print(
                f"for {stock_name_symbol}. "
                "Standard API rate limit is 25 requests per day. "
                "Check the prices here: https://finance.yahoo.com/quote/MSFT/history/"
            )


def add_updated_data():
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


                # Update the sheet with the new stock price
                # Adjust col_index to 1-based index for update_cell
                api_call_with_retry(stock_portfolio.update_cell, 5, col_index + 1, desired_value)
                print(
                    f"The latest price from {stock_name_symbol} is updated."
                    f"{float(desired_value):.2f}. "
                    "is added to googlesheet."
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


def get_valid_input(prompt, input_type=str, valid_range=None):
    """
    Repeatedly requests input from the user until valid input is provided.
    :param prompt: The message to display to the user
    :param input_type: The type of input expected (str, int, float)
    :param valid_range: Optional tuple (min, max) for numerical inputs to check against
    :return: Valid user input of the requested type
    """
    while True:
        user_input = input(prompt).strip()  # Strip to avoid issues with leading/trailing spaces

        if input_type == str:
            if user_input:  # Check if the string is not empty
                return user_input
            else:
                print("Input cannot be empty. Please try again.")

        elif input_type == int:
            try:
                value = int(user_input)
                if valid_range and (value < valid_range[0] or value > valid_range[1]):
                    print(f"Please enter an integer between {valid_range[0]} and {valid_range[1]}.")
                else:
                    return value
            except ValueError:
                print("Invalid input. Please enter an integer.")

        elif input_type == float:
            try:
                value = float(user_input)
                if valid_range and (value < valid_range[0] or value > valid_range[1]):
                    print(f"Please enter a float between {valid_range[0]} and {valid_range[1]}.")
                else:
                    return value
            except ValueError:
                print("Invalid input. Please enter a float.")

        else:
            print(f"Unsupported input type {input_type}.")


print('Welcome to Stock Analyst. Get an overview and manage your portfolio\n')


def main():

    # column_check()

    while True:

        show_portfolio()
        print("\nOptions:")
        print("1: Add a new stock")
        print("2: Delete a stock")
        print("3: Adjust the number of shares")
        print("4: Show latest stock prices")
        print("5: Add latest stock prices")
        print("6: Exit")

        choice = input("Choose an option (1, 2, 3, 4, 5, 6): ")

        if choice == '1':
            add_stock_column()
            time.sleep(2)
            clear()
        elif choice == '2':
            delete_stock_column()
            time.sleep(2)
            clear()
        elif choice == '3':
            adjust_multiplicator()
            time.sleep(2)
            clear()
        elif choice == '4':
            provide_updated_data()
            time.sleep(15)
            clear()
        elif choice == '5':
            add_updated_data()
            time.sleep(5)
            clear()
        elif choice == '6':
            break
        else:
            print("Invalid option. Please choose again.")


main()
