# Stock analyst

Welcome to my third project, 'stock analyst', it is a script which supports people to analize their stock portfolio by using an Google Spreedsheet to store stock information and an API to receive updated stock information. The focus is on the terminal screen. 

<img src="images_README/AmIresponsive.PNG" alt="image shows responisveness by presenting preview on different devices">

The project provides an overview table for the user to see his portfolio - stock names and further details such as number of shares, stock prices and profit loss.
The overview is displayed at the beginning together with all options such as 'add stock', 'delete stock', 'adjust number of shares', ... (see image).
Once an option is chosed the display still appears together with further input requests for the user.

<img src="README.images/start_view.PNG" alt="shows the start view">

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


### Validator Testing
Validator testing has been done on:
https://pep8ci.herokuapp.com/

#### Accessability (delete)
?

### Unfixed Bugs
(No unfixed bugs.)
API_stock_daily_update()



## Deployment - https://github.com/discord/heroku-sample-app/blob/main/README.md
The site was deployed to Heroku pages using a GitHub repository for data storage.

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


## API and Google spreadsheet add-on alpha vantage 
https://www.alphavantage.co/


### Description API
Alpha vantage is a free proivder of stock information. 25 requests per day are included in the free version. In addition, it provides google add-ons which can be integrated into google sheets. Due to better handling and the direct API is used wihtin this project.

The documentation shows a standrad API documentation including request urls, parameter definition.

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
https://documentation.alphavantage.co/GoogleSheetsMarketDataAddon/V_1/index.html



## Improvements and ideas for subsequent projects

- add API from https://www.alphavantage.co/ and using live stock data
- add more validations
- adjust html and JavaSript files to improve the design


## Credits

### Content
https://github.com/discord/heroku-sample-app/blob/main/README.md

### Code

| No | Description  | Source | URL |
| -- | ------------ | ------ | --- |
| 1 | using ascci tables to improve visualization of stock overview | Forum geeksforgeeks.org | https://www.geeksforgeeks.org/generate-simple-ascii-tables-using-prettytable-in-python/ |
| 2 | clear terminal | portal stackoverflow.com | https://stackoverflow.com/questions/517970/how-can-i-clear-the-interpreter-console
clear()

https://stackoverflow.com/questions/75459360/how-to-fix-the-typeerror-can-only-concatenate-str-not-float-to-str
https://stackoverflow.com/questions/1343890/how-do-i-restrict-a-float-value-to-only-two-places-after-the-decimal-point-in-c
https://stackoverflow.com/questions/517970/how-can-i-clear-the-interpreter-console