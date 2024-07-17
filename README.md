# Stock analyst

Welcome to my third project, 'stock analyst', it is a script which supports people to analize their stock portfolio by using an Google Spreedsheet to store stock information and an API to receive updated stock information. The focus is on the terminal screen. Since there are curretnly just basic checks implemented this is a portfolio manager for leisure broker. However, by adding more functions based on the input data tool can be used for more extensive analyses of the stock information. 

<img src="images_README/AmIresponsive.PNG" alt="image shows responisveness by presenting preview on different devices">

The project provides an overview table for the user to see his portfolio - stock names and further details such as number of shares, stock prices and profit loss.
The overview is displayed at the beginning together with all options such as 'add stock', 'delete stock', 'adjust number of shares', ... (see image).
Once an option is chosed the display still appears together with further input requests for the user.

<img src="README.images/start_view.PNG" alt="shows the start view">


## Remarks for handeling the program
Since not all automatications are set the google worksheets has to be updated manually every day. That means each date the current price has to be added to the column by using option 7. The Alphaventage API is limited to 25 requets. That means after a few requests the limit is reached. This also depends on the number of stocks in the portfolio.


## Features

### Feature overview:

| Feature | Description  | images |
| ------------- |------------- | ------------- |
|show portfolio | The feature displays the current status of the portfolio in a table: stock names and number of shares by using a assci feature ||
|add stock |The feature adds the new stock name to the sheet and adds the number of shares ||
|delete stock |The feature identifies the relevant stock and deletes it, deletes number of shares and deletes ||
|adjust number of shares |The feature enables the user to adjust the number of shares of existing stocks ||
|show top performers | The feature analyzes the last three available data points and identifies stocks with rising values ||
|show low performers | The feature analyzes the last three available data points and identifies stocks with decreasing values||
|calculate profit loss | The feature calculates profit loss by substract the first stock values from the last one in a each column. ||
|check columns |||
|clear function| The feature clears the terminal to provide a better user experience ||
|find stock symbol |||
|provide updated data |||


Here the main function in more detail:

#### check columns
Right at the beginning all three google worksheets are validated whether all tables have the same amount of columns. If not there is a note, so that the user can check it in the worksheets.

#### show portfolio
Displays the table of stocks. The information are pulled from the different googlesheets - SHEET.worksheet('stock_portfolio'), SHEET.worksheet('stock_daily_update') and profit_loss_sheet = SHEET.worksheet('profit_loss'). 
The relevant rows are pulled and than the single values of each cell are pulled by using a "loopwith an index".

Pretty table is used to generate the table layout whcih is also used wihtin the loop fcuntion. In addition, the time of the table generation is mentioned below the table.

The price values are depeending on the API connection. If the worksheets are updated, the current price is shown. Otherwise the data are those from the latest update.

#### add stock
Once a new stock is entered, a new column is added to the right of the existing table. It is crutial that the new stock name and it's parameters are added in all three google worksheets to enure the functionality of the other functions. SHEET.worksheet('stock_portfolio'), SHEET.worksheet('stock_daily_update') and profit_loss_sheet = SHEET.worksheet('profit_loss').
Therefore, there is a check function right at the beginning. A while-True loop, if-else and try-except functions are used.

#### delete stock
This function seaches for the user input and deletes the stock from all three google worksheets .SHEET.worksheet('stock_portfolio'), SHEET.worksheet('stock_daily_update') and SHEET.worksheet('profit_loss'). One if-else function is used.

#### adjust number of shares / adjust multiplicator
Once the option is selected, an input is reqeustes to the user. After entering the new number of shares it will updated in the relevant google worksheet SHEET.worksheet('stock_portfolio'). A if-else and a try-except function are used.

#### show top performers
By using a for loop and if-else functions the values of the last 3 entries in SHEET.worksheet('stock_daily_update') for each relevant column is pulled and analyzed. When all three entires are increasing timewise the stock is identified as a current top-performer. All top-performer are displayed in the terminal.

#### show low performers
By using a for loop and if-else functions the values of the last 3 entries in SHEET.worksheet('stock_daily_update') for each relevant column is pulled and analyzed. When all three entires are decreasing timewise the stock is identified as a current low-performer. All top-performer are displayed in the terminal.All top-performer are displayed in the terminal.

#### calculate profit loss
The profit and loss function calculates the surplus of purchase price (row 2, SHEET.worksheet('stock_daily_update')) and the latest price value (row 5, SHEET.worksheet('stock_daily_update')).
The result is saved in SHEET.worksheet('profit_loss'). The result is displayed in the overview table.

When a new stock is added and teh API connection fails, the surplus is not correct. (BUG)


## UX Design (delete)
Since the program is acceable via a terminal the design is limited. However, the user experience is still important. Therefore, some adjustment has been considered.
The tool helps the user to manage his stock portfolio. Because of that the portfolio is displayed as often as possible at the top and it is structured by using a table import.
The size of the terminal is increased to 50 rows (in index.html and default.js). To avoid an information overload and make the use of the tool more convenient for users who are not dealing with a terminal the terminal is cleared each time a new function is used. At the same time the overview is updated with the new input.


## User Stories

### New Site Users

- As a new user, I would like to have to know what the tool is about
- As a new user, I would like to have a good overview about the functionalities of the tool
- As a new user, I would like to have a good overview in the terminal. It should be not overwhelmed with information
- As a new user, I would like to have a tool that helps me managing my stock portfolio

### Returning Site Users

- As a returning user, I would like to have a tool that helps me managing my stock portfolio
- As a returning user, I would like to have a tool that helps me managing my stock portfolio
- As a returning user, I would like to have a tool that helps me managing my stock portfolio


## Testing
- Testing was done in small breaks during the development and at the end of the project
- Validators have been used (see chapter below)
- logic checks
- type in worng input, validation check

### Bugs (not fixed)
When a new stock is added and teh API connection fails, the surplus is not correct. (BUG)


### Bugs (fixed)

| Bug | Description  | images (optional) | Correction | 
| --- |------------- | ----------------- | -----------|
| Error_list_index_out_of_range | There is no reference in the worksheet. A new stock was added, but a value is missing in the column.  | <img src="README.images/Error_list_index_out_of_range.PNG" alt="image shows Error message"> | Adding a validation when a new stock name is added to stock_portfolio sheet. |
| TypeError_unsupported_operand_type_for_str | Using string values for calculation ends up in an error. | <img src="README.images/TypeError_unsupported_operand_type_for_str.PNG" alt="image shows Error message"> | adding float() to the variabels: rounded_profit_loss_value_percentage = ((float(first_column_value) - float(last_column_value)) / float(first_column_value))* 100 |
| IndexError_list_index_out_of_range | The IndexError indicate a mismatch in the lengths of the header and shares_row lists. This mismatch can occur if there are fewer elements in shares_row than in header, or vice versa.|<img src="README.images/IndexError_list_index_out_of_range.PNG" alt="image shows Error message">| Consequently, it is necessary to make sure that there is no mismatch by adding or deleting a stock| 
| DeprecationWarning | DeprecationWarning: The order of arguments in worksheet.update() has changed | <img src="README.images/DeprecationWarning_range_name.PNG" alt="image shows Error message | Trying different ways of range requests and reading https://stackoverflow.com/questions/72562988/how-to-update-multiple-distant-rows-in-google-sheets-using-api the issue was fixed. Original code: profit_loss_sheet.update('A2', [surplus_data]). FIxing the order of the argunments by range "2:2" |
| NameError_name not defined | the variable was missing | <img src="README.images/NameError_name_is_not_defined.PNG" alt="image shows Error message"> | code snipped was not valid anymore. variable was deleted |

### Validator Testing
Validator testing has been done on:

#### [CI Python validator](https://pep8ci.herokuapp.com/)

No errors were returned for run.py

IMAGE UPDATE NEEDED!
<img src="README.images/PI_python_linter_validation.PNG" alt="image shows preview of validator results" width="500px">

<details>
    <summary>further results of HTML, CSS Validator</summary>

<img src="" alt="image shows preview of validator results" width="500px">
<img src=""_html_end.PNG alt="image shows preview of validator results" width="500px">

#### [HTML validator](https://validator.w3.org/)

No errors were returned

<img src="README.images/HTML_validation.PNG" alt="image shows preview of validator results" width="500px">


#### [CSS validator](https://jigsaw.w3.org/css-validator/)

No errors were returned

<img src="README.images/CSS_validation.PNG" alt="image shows preview of validator results" width="500px">


#### [JS Validator] (https://jshint.com/)

Errors occured. However, since I reused the suggested template from Code Institute and I haven't made any adjustments I keep the current status.

Code from index.js and defaul.js checked. 

Here an example of index.js
<img src="README.images/JS_validation.PNG" alt="image shows preview of validator results" width="500px">

</details>


#### Accessability (delete)
I confirm that the selected colors and fonts are easy to read and accessible by using Lighthouse in devtools (Chrome).

(screenshot)

### Unfixed Bugs
(No unfixed bugs.)
API_stock_daily_update()


## Deployment
The site was deployed to a Heroku page using a GitHub repository for data storage.

Heroku page: https://stock-analyst-390ed9b08457.herokuapp.com/
GitHub repository: https://github.com/Fl0W97/ci-p3-stock-analyst

### Configure Heroku 
The steps to configure Heroku are as follows:

Log in to your account, or set up a new one
Create a new app on Heroku
<img src="README.images/heroku_create_new_app.PNG" alt="image shows infos about heroku set up"> 

#### Connect to GitHub
Next, you can configure deploys with Github. If you prefer to deploy without using Github, you can read Heroku's deployment documentation. https://devcenter.heroku.com/categories/deployment

In the Deploy tab, select the option to Connect this app to GitHub
<img src="README.images/heroku_connect_to_github1.PNG" alt="image shows infos about heroku set up">

Select the branch you want to deploy your app from
<img src="README.images/heroku_manually_deployment.PNG" alt="image shows infos about heroku set up">

#### Add Discord credentials
Before your app can go online, you'll have to configure your Heroku environment with your Discord bot's credentials:
Add your bot’s TOKEN, GUILD_ID, CLIENT_ID, and any other credentials your bot might need. More details on credentials for Baker bot can be found in the tutorial.
<img src="README.images/heroku_credentials.PNG" alt="image shows infos about heroku set up">

#### Add a buildpack
Next, add a Heroku buildpack to your app. Click add a buildpack to your app and configure it for NodeJS.
<img src="README.images/heroku_add_builpack.PNG" alt="image shows infos about heroku set up">

### GitHub

The steps to set up your repository in GitHub are as follows:

- In the GitHub repository, navigate to the Settings tab
- From the source section drop-down menu, select the Main Branch, then click "Save"
- The page will be automatically refreshed with a detailed ribbon display to indicate the successful deployment.


Here the live link:  ...

<details>
    <summary>Cloning repository</summary>

1. Visit the GitHub repository.
2. Find the Code button situated above the file list and give it a click.
3. Choose your preferred cloning method — whether it's HTTPS, SSH, or GitHub and hit the copy button to copy the URL to your clipboard.
4. Launch Git Bash or Terminal.
5. Navigate to the directory where you want the cloned directory to reside.
6. In your IDE Terminal, input the following command to clone the repository:
 git clone https://github.com/Fl0W97/ci_p3_stock-analyst.git
7. Press Enter to create your local clone.

</details>


## Tools & Technologies used

The main functions are generated with Python. However, to set up the whole project a standard template consits of files of json, js, txt, html and css.

- node.js
- phython (import prettyTable, os, gspread, datetime, requests, json)
- Git used for version control (git status, git add, git commit)
- GitHub used for secure online code storage
- GitHub Pages used for hosting the deployed front-end site
- GitHub- template reused from love sandwiches
- Gitpod used for local IDE for development
- Heroku
- JavaScript
- Html
- CSS


## Set up (API) Google spreadsheet, add-on alphavantage 

### Step 1: Create a Google Spreadsheet
<details>

<summary>details</summary>
First create a google account https://myaccount.google.com/

    Sign in to Google Account:
        Go to Google Sheets and sign in with your Google account.

    Create a New Spreadsheet:
        On the Google Sheets homepage, click the + button labeled "Blank" to create a new spreadsheet.

    Name Your Spreadsheet:
        Click on "Untitled Spreadsheet" at the top left corner and enter a name for your spreadsheet.

</details>

### Step 2: Set Up Your Spreadsheet
<details>

<summary>details</summary>
    Enter Data:
        Enter your data in the cells of the spreadsheet. You can start with simple data entries, such as column headers and rows of data.

    Format Cells (Optional):
        You can format the cells by selecting them and using the toolbar options (e.g., bold, italic, text color, cell background color, etc.).

    Save Your Work:
        Google Sheets automatically saves your work as you go. However, it’s good practice to ensure your data is saved by checking the "Saved to Drive" message at the top.

</details>

### Step 3: Add alpha vantage Google Add-on
<details>

<summary>details</summary>
    Open Add-ons Menu:
        In your Google Spreadsheet, go to the top menu and click on Extensions, then select Add-ons.

    Get Add-ons:
        Click on Get add-ons from the drop-down menu. This will open the Google Workspace Marketplace.

    Search for an Add-on:
        In the Google Workspace Marketplace, use the search bar to find the add-on 'Alpha Vantage Market Data'

    Install the Add-on:
        Once you find the desired add-on, click on it to open its details page.
        Click on the Install button. A pop-up window will appear asking for permissions.
        Review the permissions and click Allow to proceed with the installation.

</<details>

### Step 4: Use the Add-on
<details>

<summary>details</summary>
    Activate add-on alpha vantage with API-KEy

        Get Alpha Vantage API Key:
        Go on https://www.alphavantage.co/support/#api-key and request an API Key.
        Go back in the Google spreadsheet to Extensions in the menu, go an Alpha Vantage and enter the API Key.
        Now you can start using formulars of Alpha Vantage to enter those in the spreadsheet.

Find more details on https://documentation.alphavantage.co/GoogleSheetsMarketDataAddon/V_1/index.html

        
        Find here an overview of possible add-on formulas and how they will be added.
        https://documentation.alphavantage.co/GoogleSheetsMarketDataAddon/V_1/example_screens.html
        https://documentation.alphavantage.co/GoogleSheetsMarketDataAddon/V_1/function_reference/index.html

</details>

### Description Alpha Vantage API
Alpha vantage is a free proivder of stock information. 25 requests per day are included in the free version. you can find here an extensive API documentation: https://www.alphavantage.co/documentation/

<details>
<summary>details</summary>
The documentation shows a standard API documentation including request urls, parameter definition.

The API function TIME_SERIES_DAILY is used in this project.
<img src="README.images/API_daily_time_series.PNG" alt="image shows example of data provided from time_series_daily function">

It shows the stock price of one single stock of the last 100 days. This colums contain the parameters timestamp, open, high, low, close and volume

<img src="README.images/API_daily_time_series_example.PNG" alt="image shows example of data provided from time_series_daily function">

https://www.alphavantage.co/documentation/#time-series-data

THe API function SYMBOL_SEARCH is used in this project.
<img src="README.images/API_search_symbols.PNG" alt="image shows example of data provided from time_series_daily function">

It enables the user to find the exact stock symbol as reference to get the correct stock price values. As search input usually the company name can be used. It provides a list of symbol codes which are used for the time_series_day function. This colums contain the parameters symbol, name, type, region, marketOpen, marketClose, timezone, currency, matchScore.

<img src="README.images/API_search_symbols_example.PNG" alt="image shows example of data provided from time_series_daily function">

https://www.alphavantage.co/documentation/#symbolsearch

The google add-on has been tested successfully. It can be easily integrated into a google spreadsheet.
However, due to better and more flexible handling of the data no add-on function is used. 


Links for googlesheet add-on integration:
https://documentation.alphavantage.co/GoogleSheetsMarketDataAddon/V_1/example_screens.html#avsearchequitysymbol

</details>

## Improvements and ideas for subsequent projects

- add profit_loss percentage to the table overview
- buy premium version of Alphavantage API so that there is no limmitation of 25 requests
- add an automatically update for google spreadsheet stock_daily_update. Using 'time series' from Alpha Vantage https://www.alphavantage.co/documentation/#time-series-data
- add more validations by taking into account more input issues from the user
- adjust html and JavaSript files to improve the design i.e. by using html and css the terminal can be centered, attractive images wiht a link to finance can be added. Links or snippets to news about stocks could be implemented.
- due to safety issues don't show the APIKey in the code. Hide it and set a parameter in creds.json


## Credits

### Content
By going through the API documentation and further examples of Alpha Vantage I decided which options will be added. Series update and smybol search seems a good start for providing stock information.

https://www.alphavantage.co/documentation/#symbolsearch
https://documentation.alphavantage.co/GoogleSheetsMarketDataAddon/V_1/function_reference/index.html

Description of Heroku deployment is resused from github project
https://github.com/discord/heroku-sample-app/blob/main/README.md

### Code

| No | Description  | Source | URL |
| -- | ------------ | ------ | --- |
| 1 | Python Specific core concepts | Code institute | i.e. https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+CPP_06_20+3/courseware/f780287e5c3f4e939cd0adb8de45c12a/8d9c1efb1864472bb682a0c233898a17/ |
| 2 | clear terminal | portal stackoverflow.com | https://stackoverflow.com/questions/517970/how-can-i-clear-the-interpreter-console |
| 3 | datetime | Code Institute | https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+CPP_06_20+3/courseware/272f493b4d57445fbd634e7ceca3a98c/4ab3e01af44f4bf2828739c1d0591a45/|
| 4 | restrict float value | Stackoverflow.com | https://stackoverflow.com/questions/75459360/how-to-fix-the-typeerror-can-only-concatenate-str-not-float-to-str, https://pythonhow.com/how/limit-floats-to-two-decimal-points/ |
| 5 | converting a listint | Stackoverflow.com | https://stackoverflow.com/questions/1528724/converting-a-listint-to-a-comma-separated-string|
| 6 | use request libary for API set up | Stackoverflow.com | https://realpython.com/python-requests/ |
| 7 | working with spreadsheets via API | Code institute, Stackoverflow | https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+LS101+1/courseware/293ee9d8ff3542d3b877137ed81b9a5b/071036790a5642f9a6f004f9888b6a45/, https://stackoverflow.com/questions/59272851/python-gspread-changing-contents-of-a-cell-based-on-contents-of-another-cell, https://www.sitepoint.com/using-python-parse-spreadsheet-data/ |
| 8 | using ascci tables to improve visualization of stock overview | Forum geeksforgeeks.org | https://www.geeksforgeeks.org/generate-simple-ascii-tables-using-prettytable-in-python/ |
| 9 | f" print variable | Stackoverflow.com | https://stackoverflow.com/questions/17153779/how-can-i-print-variable-and-string-on-same-line-in-python
| 10 | API request check, example | https://stackoverflow.com/questions/54087303/python-requests-how-to-check-for-200-ok
