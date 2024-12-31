# terminal of 80 characters wide and 50 rows high

# imports the whole libaries
import gspread
import os
from prettytable import PrettyTable
import datetime
import requests
import json

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


# Show current stock portfolio
def show_portfolio():
    # calculate surplus
    calculate_profit_loss()

    # Retrieve all relevant rows from both sheets
    stock_data = stock_portfolio.get_all_values()  # Get all rows from stock portfolio
    profit_loss_data = profit_loss_sheet.get_all_values()  # Get all rows from profit/loss sheet

    # Extract relevant data from tables above
    header = stock_data[0]  # stock name, row 1
    shares_row = stock_data[1]  # stock shares, row 2
    purchase_price = stock_data[3]  # stock pu price, row 4
    current_price = stock_data[3]  # stock cu price, row 5
    profit_loss_percentage = profit_loss_data[2]  # surplus, row 3
    profit_loss = profit_loss_data[1] # surplus, row 3


    x = PrettyTable()

    x.field_names = [
        "Stock name",
        "Shares",
        "Purch. price $",
        "Current price $",
        "Surplus %",
        "Surplus total $"
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

        profloss = profit_loss[col_index - 1]  # Get total profit or loss

        # Check if col_index - 1 is within the bounds of profit_loss_percentage
        if col_index - 1 < len(profit_loss_percentage):
            # Get profit or loss percentage
            profloss_percentage = profit_loss_percentage[col_index - 1]
        else:
            # Default value if percentage data is missing
            profloss_percentage = "N/A"

        # Add row to the table
        x.add_row([stock_name, shares, purchase, current,
                   profloss_percentage, profloss])

    # Print the table
    print(x)

    # Display the update time
    print(f"Table values based on the data in google spreadsheet. \n")


def add_stock_column():
    while True:
        new_stock_name = get_valid_input(
            "Enter the name of the new stock:\n ", input_type=str
        )

        # Check if the stock already exists
        header = stock_portfolio.row_values(1)  # Get all headers in one call
        if new_stock_name in header:
            print(
                f"The stock '{new_stock_name}' already exists in portfolio."
            )
        else:
            break

    # Check the current number of columns in the sheet
    num_columns = len(header)
    if num_columns >= 1000:
        print(
            "The maximum number of columns in the googlesheet"
            "has been reached. Cannot add more stocks."
            "Please contact support."
            )
        return

    last_column = len(header)

    # add the new stock to both sheets
    # Use api_call_with_retry for all update operations
    api_call_with_retry(
        stock_portfolio.update_cell, 1, last_column + 1, new_stock_name
    )
    api_call_with_retry(
        profit_loss_sheet.update_cell, 1, last_column + 1, new_stock_name
    )
    print(f"New column for stock '{new_stock_name}' added.")

    # add number of shares in row 2 in sheet stock portfolio
    new_multiplicator = get_valid_input(
        f"Enter the number of shares for {new_stock_name}"
        "(integer): \n", input_type=int)

    try:
        new_multiplicator = int(new_multiplicator)
        api_call_with_retry(
            stock_portfolio.update_cell, 2, last_column + 1, new_multiplicator
        )
        api_call_with_retry(
            profit_loss_sheet.update_cell, 2, last_column + 1,
            new_multiplicator
        )
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
        api_call_with_retry(
            stock_portfolio.update_cell, 4, last_column + 1, purchase_price
        )
        print(f"Purchase price of '{new_stock_name}' added.")
    except ValueError:
        print("Invalid input. Please enter a float number.")

    # add current price
    api_call_with_retry(
        stock_portfolio.update_cell, 5, last_column + 1, purchase_price
    )

    # Ensure that the calculation is done
    time.sleep(2)

    # Now calculate profit/loss (this ensures data is fully updated)
    calculate_profit_loss()

    find_stock_symbol()


def delete_stock_column():
    # delete stock name, header and column on all sheets
    stock_name = get_valid_input(
        "Enter the name of the stock you want to delete:\n ", input_type=str
    )

    # find content in both sheets
    cell = stock_portfolio.find(stock_name)
    cell2 = profit_loss_sheet.find(stock_name)

    # If stock is found in both sheets, delete columns
    if cell:
        stock_portfolio.delete_columns(cell.col)
        profit_loss_sheet.delete_columns(cell2.col)
        print(f"Column for stock '{stock_name}' deleted.")
    else:
        print(
            f"Stock '{stock_name}' not found."
            "Please check your spelling. Otherwise the stock is not available"
        )


def update_stock_value(action: str):
    """
    A generalized function to update stock values such as shares, purchase
    price, or current price. A string indicating the type of action
    ('number_of_shares', 'purchase_price', or 'current_price')
    """
    stock_name = get_valid_input(
        f"Enter the name of the stock to adjust the {action}:\n ",
        input_type=str
    )

    cell = stock_portfolio.find(stock_name)
    if cell:
        # Get the appropriate input based on the action
        if action == 'number_of_shares':
            input = get_valid_input(
                f"Enter the no. of shares for {stock_name} (integer):\n ",
                input_type=int
            )

            # Update the stock portfolio with the new number_of_shares
            api_call_with_retry(
                stock_portfolio.update_cell, 2, cell.col, input
            )

            print(
                    f"Number of shares updated to {input} "
                    f"for {stock_name}."
                    )

        elif action == 'purchase_price':
            input = get_valid_input(
                f"Enter the purchase stock price of {stock_name} (float):\n ",
                input_type=float
                )

            # Update the stock portfolio with the new purchase_price
            api_call_with_retry(
                stock_portfolio.update_cell, 4, cell.col, input
                )

            print(
                f"Purchase price updated to {input} "
                f"for {stock_name}."
                )

        elif action == 'current_price':
            input = get_valid_input(
                f"Enter the current stock price of {stock_name} (float):\n ",
                input_type=float
                )

            # Update the stock portfolio with the current_price
            api_call_with_retry(
                stock_portfolio.update_cell, 5, cell.col,
                input
                )

            print(
                f"Current price updated to {input} "
                f"for {stock_name}."
            )

        else:
            print("Invalid action specified. Contact support")

    else:
        print(f"Stock '{stock_name}' not found.")


""" Use the generic function with different actions
    'multiplicator', 'purchase' or 'current' """


def adjust_multiplicator():
    update_stock_value('number_of_shares')


def add_purchase_price():
    update_stock_value('purchase_price')


def add_current_price():
    update_stock_value('current_price')


def calculate_profit_loss():
    header = stock_portfolio.row_values(1)  # Get the column headers
    rows = stock_portfolio.get_all_values()  # Fetch all rows in one call
    purchase_price_column = rows[3]  # Row for purchase prices
    current_price_column = rows[4]  # Row for current prices
    multiplicator_row = rows[1]  # Row for shares

    # List for profit and loss values
    surplus_data = []
    percentage_data = []

    for col_index in range(1, len(header) + 1):
        # Access the purchase price safely
        try:
            purchase_price = purchase_price_column[col_index - 1]
        except IndexError:
            print(
                f"Error: Purchase price missing "
                "for column {header[col_index - 1]}"
                )
            continue

        # Access the current price safely
        try:
            current_price = current_price_column[col_index - 1]
        except IndexError:
            print(
                f"Error: Purchase price missing "
                "for column {header[col_index - 1]}"
                )
            continue

        try:
            first_value = float(purchase_price)
            last_value = float(current_price)
        except ValueError:
            print(
                f"Non-numeric data found in column: {header[col_index - 1]}"
                )
            continue

        # Calculate profit/loss
        profit_loss_value = last_value - first_value
        rounded_profit_loss_value = round(profit_loss_value, 2)

        if first_value != 0:
            rounded_profit_loss_value_p = (last_value - first_value) / first_value * 100
        else:
            rounded_profit_loss_value_p = 0

        # Fetch multiplicator safely
        try:
            multiplicator = float(multiplicator_row[col_index - 1])
        except IndexError:
            print(
                f"Error: Number of shares missing for"
                "column {header[col_index - 1]}"
                )
            continue

        # Calculate surplus based on multiplicator
        surplus = multiplicator * rounded_profit_loss_value

        # Append results
        surplus_data.append(surplus)
        percentage_data.append(round(rounded_profit_loss_value_p, 2))

        # Update Google Sheets in a single call
        profit_loss_sheet.update(range_name='2:3', values=[surplus_data,
                                                           percentage_data])

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
            "Check sheet stock_portfolio. Data are missing. "
            "Adjust it manually in the sheet stock_portfolio ."
            "If you haven't defined a symbol for a stock that might be the reason. "
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
                "The symbol is invalid or API rate limit is reached if you have exceeded 25 requests per day. "
                "You can add the prices manually. Find here the stock information: https://finance.yahoo.com/quote/"
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
                api_call_with_retry(
                    stock_portfolio.update_cell, 5, col_index + 1,
                    desired_value
                    )
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
                "Check the prices here: https://finance.yahoo.com/quote/"
            )


def find_stock_symbol():
    # Define stock name. Use it for the API request
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

        # Inform the user
        print(
            f"There might be different stock symbols. "
            "Choose one exact stock symbol to proceed with."
        )

        # Check if 'bestMatches' key exists in the JSON response
        if 'bestMatches' in data:
            best_matches = data['bestMatches']

            # Check if there are no matches
            if not best_matches:
                print(
                    "No matching stock symbols were found. "
                    "We cannot provide you this stock information. "
                    "However, you can add stock details manually."
                )
                time.sleep(5)
                # Ask the user if they want to keep the stock information
                user_input = input(
                    "Would you like to mange the stock information manually? "
                    "If not the data is deleted. (y/n): ").strip().lower()
                if user_input == 'y':
                    new_stock_name_symbol = f"{new_stock_name}_no_symbol"
                    # Update the stock portfolio sheet with the new symbol
                    last_column = len(header)
                    api_call_with_retry(
                        stock_portfolio.update_cell, 3,
                        last_column, new_stock_name_symbol
                    )
                    print(f"Symbol for {new_stock_name} is added.")
                else:
                    # Find the column to delete based on the `new_stock_name`
                    column_to_delete = header.index(new_stock_name) + 1  # +1 because columns are 1-based
                    api_call_with_retry(
                        stock_portfolio.delete_columns, column_to_delete
                    )
                    print(f"Column for stock '{new_stock_name}' deleted.")
                return  # Exit the function as the process is complete

            else:
                # Extract symbols and names
                # Store both in a list for validation
                symbols_and_names = [
                    (match['1. symbol'], match['2. name'])
                    for match in best_matches
                ]

                # Print the symbols and names
                for symbol, name in symbols_and_names:
                    print(f"Symbol: {symbol}, Name: {name}")

                # Loop until the user provides a valid symbol
                while True:
                    new_stock_name_symbol = input(
                        "Enter the symbol of the new stock:\n "
                        ).strip()

                    # Validate the input against the list of valid symbols
                    if new_stock_name_symbol in [symbol for symbol,
                    _ in symbols_and_names]:
                        # Update the stock portfolio sheet with the new symbol
                        last_column = len(header)
                        api_call_with_retry(
                            stock_portfolio.update_cell, 3,
                            last_column, new_stock_name_symbol
                            )
                        print(f"Symbol for {new_stock_name} is added.")
                        break  # Exit the loop once a valid symbol is entered
                    else:
                        print(
                            f"Invalid symbol '{new_stock_name_symbol}'."
                            "Please choose a valid symbol from the list."
                            )

        else:
            print(
                "Connection to the API was not successful. "
                "Enter the symbol manually or wait "
                "until the connection is established again."
            )

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
                print(
                    f"Retrying... Attempt {attempt}/{max_retries}. "
                    "Waiting {wait_time} seconds."
                    )
                time.sleep(wait_time)
            else:
                # If the error is not recoverable (other status) raise it
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
    :param valid_range: Optional tuple (min, max) for
    numerical inputs to check against
    :return: Valid user input of the requested type
    """
    while True:
        # Strip to avoid issues with leading/trailing spaces
        user_input = input(prompt).strip()

        if input_type == str:
            if user_input:  # Check if the string is not empty
                return user_input
            else:
                print("Input cannot be empty. Please try again.")

        elif input_type == int:
            try:
                value = int(user_input)
                if valid_range and (value < valid_range[0]
                or value > valid_range[1]):
                    print(
                        f"Please enter an integer between {valid_range[0]} "
                        "and {valid_range[1]}."
                        )
                else:
                    return value
            except ValueError:
                print("Invalid input. Please enter an integer.")

        elif input_type == float:
            try:
                value = float(user_input)
                if valid_range and (value < valid_range[0]
                or value > valid_range[1]):
                    print(
                        f"Please enter a float between {valid_range[0]} "
                        "and {valid_range[1]}."
                        )
                else:
                    return value
            except ValueError:
                print("Invalid input. Please enter a float.")

        else:
            print(f"Unsupported input type {input_type}.")


print('Welcome to Stock Analyst. Get an overview and manage your portfolio\n')


def main():

    column_check()

    while True:

        show_portfolio()
        print("\nOptions:")
        print("1: Add a new stock")
        print("2: Delete a stock")
        print("3: Adjust the number of shares")
        print("4: Show latest stock prices")
        print("5: Add/ adjust current stock price manually")
        print("6: Add/ adjust purchase stock price manually")
        print("7: Add current stock prices automatically")
        print("8: Exit")

        choice = input("Choose an option (1, 2, 3, 4, 5, 6, 7, 8): ")

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
            time.sleep(5)
            clear()
        elif choice == '4':
            provide_updated_data()
            time.sleep(15)
            clear()
        elif choice == '5':
            add_current_price()
            time.sleep(5)
            clear()
        elif choice == '6':
            add_purchase_price()
            time.sleep(5)
            clear()
        elif choice == '7':
            add_updated_data()
            time.sleep(5)
            clear()
        elif choice == '8':
            break
        else:
            print("Invalid option. Please choose again.")


main()
