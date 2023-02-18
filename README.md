# Banking Website

## Project Goals
The overarching goal for this project was to create a website that implements 
the major functions that you might find on any major banking website. Some 
functions cannot be implemented of course because this is not a real banking 
website, for example wire transfers. The major functionality I was seeking to 
reproduce was:
- Create a bank account
- Close a bank account
- Withdraw from a bank account
- Deposit into a bank account
- Transfer money from one of your bank accounts to another
- View various breakdowns of your transactions

## Project Description
This project uses Flask, Flask-Login, and Flask-SQLAlchemy to create this 
website. There were several simplifications necessary to be able to build 
this project:
- Withdrawals, deposits, and balances are in no way backed up with any kind of 
currency and in no way represent real money.
- Account creation and closure can be done automatically online, normally this 
would require a phone call to the bank but this is the best solution.
- Because the goal is to simply emulate the functionality necessary for a 
banking website, users can start an account with any amount of money in an 
account and deposit or withdraw as much as they would like.