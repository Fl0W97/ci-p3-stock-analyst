# Stock analyst

Welcome to my third project, 'stock analyst', it is a script which supports people to analize their stock portfolio by using an Google Spreedsheet API. 

<img src="images_README/AmIresponsive.PNG" alt="image shows responisveness by presenting preview on different devices">

##Input/actions:

###Show my portfolio
present all company names in the terminal (get info from first sheet, first row)
first sheet contains company names and the number of stocks (in row two)
second sheet contains names and daily updated stock values (in row two up to XXX)
thrid sheet contains the profit/loss which was generated this year

###Show the winner of the last day/week/month
show all stocks with a positive result (get info from second sheet, substracting the value in row two (ever, of the week or month) from the last value (...) same for each column

###Show the losers of the last day/week/month
show all stocks with a negative result (get info from second sheet, substracting the first value (ever, of the week or month) from the last value (...) same for each column

###Show stocks with signals
show the top performer (get info from second sheet, 3 days in a row positive)
show the flops (get info from second sheet, 3 days in a row negative)
add more signs... i.e. 5 days negative, then 2 postive in a row (...) 

###Show stocks which brings me money when I sell and how much
show the stocks (get info from first & second sheet, calculate difference from first day and last day, substract sales fee... and multiplicate with the number of stocks)
show the stocks (get info from first & second sheet, calculate difference from first day and last day, substract taxes 25%, from those add church and "solidaritäts" taxes 13,50% again)

Keep in mind the 1000€ allowance (Freibetrag)

###Buy a new stock (adjust sheet 1, 2 and 3)
###Sell a stock (adjust sheet 1, 2 and 3)

store when a sale was done. Keep in mind the 1000€ allowance (Freibetrag)

###Show overview of profit and loss this year
store when a sale was done. Keep in mind the 1000€ allowance (Freibetrag) (sheet 3, add profit/loss for each sale)


## Features



### Features:

| Feature | Description  | images |
| ------------- |------------- | ------------- |
|show portfolio | The feature displays the current status of the portfolio in a table: stock names and number of shares by using a assci feature ||
|add stock |The feature adds the new stock name to the sheet and adds the number of shares ||
|delete stock |The feature identifies the relevant stock and deletes it, deletes number of shares and deletes ||
|adjust number of shares |The feature enables the user to adjust the number of shares of existing stocks ||
|show top performers | The feature analyzes the last three available data points and identifies stocks with rising values ||
|show low performers | The feature analyzes the last three available data points and identifies stocks with decreasing values||
|calculate profit loss | The feature calculates profit loss by substract the first stock values from the last one in a each column. ||
|
|clear function| The feature clears the terminal to provide a better user experience ||



## UX Design (delete)
Since the program is acceable via a terminal the design is limited. However, the user experience is still importan. Therefore, some adjustment has been considered.
The tool helps the user to manage his stock portfolio. Because of that the portfolio is displayed as often as possible at the top and it is structured by using a table import.
The size of the terminal is increased to 50 rows (in index.html and default.js). To avoid an infomration overflow and make the tooluse more convenient for users who are not dealing all day long with a terminal the terminal is cleared eac time a new function is used.


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

## Deployment - https://github.com/discord/heroku-sample-app/blob/main/README.md
The site was deployed to Heroku pages using a GitHub repository for data storage.

### Configure Heroku 
The steps to configure Heroku are as follows:

Log in to your account, or set up a new one
Create a new app on Heroku
<img src="README.images/heroku_create_new_app.PNG" alt="image shows Error message"> 

#### Connect to GitHub
Next, you can configure deploys with Github. If you prefer to deploy without using Github, you can read Heroku's deployment documentation. https://devcenter.heroku.com/categories/deployment

In the Deploy tab, select the option to Connect this app to GitHub
<img src="README.images/heroku_connect_to_github1.PNG" alt="image shows Error message">

Select the branch you want to deploy your app from
<img src="README.images/heroku_manually_deployment.PNG" alt="image shows Error message">

#### Add Discord credentials
Before your app can go online, you'll have to configure your Heroku environment with your Discord bot's credentials:
Add your bot’s TOKEN, GUILD_ID, CLIENT_ID, and any other credentials your bot might need. More details on credentials for Baker bot can be found in the tutorial.
<img src="README.images/heroku_credentials.PNG" alt="image shows Error message">

#### Add a buildpack
Next, add a Heroku buildpack to your app. Click add a buildpack to your app and configure it for NodeJS.
<img src="README.images/heroku_add_builpack.PNG" alt="image shows Error message">

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
Alpha vantage is a free proivder of stock information. IN addition, it provides google add-ons to directly isnert the stock information into a googel spread sheet.
The documentation shows that all implemented function of the add-on. Those functions can be used simply in a spread sheet cell.

Example (picture)

 https://documentation.alphavantage.co/GoogleSheetsMarketDataAddon/V_1/index.html
https://documentation.alphavantage.co/GoogleSheetsMarketDataAddon/V_1/function_reference/index.html



## Improvements and ideas for subsequent projects

- add API from https://www.alphavantage.co/ and using live stock data
- add more validations
- adjust html and JavaSript files to improve the design


## Credits

### Content


### Code

| No | Description  | Source | URL |
| -- | ------------ | ------ | --- |
| 1 | using ascci tables to improve visualization of stock overview | Forum geeksforgeeks.org | https://www.geeksforgeeks.org/generate-simple-ascii-tables-using-prettytable-in-python/ |
| 2 | clear terminal | portal stackoverflow.com | https://stackoverflow.com/questions/517970/how-can-i-clear-the-interpreter-console
clear()

https://stackoverflow.com/questions/75459360/how-to-fix-the-typeerror-can-only-concatenate-str-not-float-to-str
https://stackoverflow.com/questions/1343890/how-do-i-restrict-a-float-value-to-only-two-places-after-the-decimal-point-in-c
https://stackoverflow.com/questions/517970/how-can-i-clear-the-interpreter-console
