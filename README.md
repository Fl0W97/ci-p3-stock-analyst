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
| --- |------------- | ------------- |



### The Footer (delete)
?

## UX Design (delete)
?

### Color Scheme (delete)
?

### Typography (delete)
?

## User Stories

### New Site Users

- As a new user, I would like to ...



### Returning Site Users

- As a returning user, I would like to ...



## Testing
- Testing was done in small breaks during the development and at the end of the project
- Validators have been used (see chapter below)
- logic checks
- using wrong input (format, ...)

### Bugs (fixed)

| Bug | Description  | images (optional) |
| --- |------------- | ------------- |

### Validator Testing
Validator testing has been done on:
?

#### Accessability (delete)
?

### Unfixed Bugs
(No unfixed bugs.)

## Deployment

The site was deployed to GitHub pages. The steps to deploy are as follows:

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
- phython
- Git used for version control (git status, git add, git commit)
- GitHub used for secure online code storage
- GitHub Pages used for hosting the deployed front-end site
- Gitpod used for local IDE for development


## Improvements and ideas for subsequent projects

- add API from https://www.alphavantage.co/ and suing live stock data



## Credits

### Content


### Code

| No | Description  | Source | URL |
| --- |------------- | ------------- | ------------- |

