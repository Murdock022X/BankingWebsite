# Banking Website

## Project Description
This project is an attempt to recreate a simple banking application. It is 
completely fake, and does not use real currency. Rather the website simply 
allows you to carry out many of the functions you might see on a banking 
website. For example the project allows you to:
- Create an account.
- Close an account.
- View a graph that shows the balance history of an account.
- Withdraw, deposit, and transfer funds into and from accounts.
- See messages and alerts from admins.
- The application also automatically generates E-Statement PDFs for your account during a term (one week).

## What I learned
I learned to use:
- Flask: This was my first exposure to web applications and flask was an excellent framework for helping me learn fundamentals including:
  - Routes
  - Get and Post
  - Web Structure
- Flask-Login: A flask addon module used to easily log users in and out.
- Flask-Sqlalchemy: A flask addon module used to easily connect to, query, and alter data in an SQL database.
- Flask-Wtforms: A flask addon module that allowed me to easily create forms that performed checks and prevented csrf attacks.
- SQL: This was also my first exposure to SQL and databases in general. I learned how to:
  - Connect to, query, and alter data in an SQL database using both the default command line for MySQL and sqlite3, as well as using the python connector, and Flask-SQLAlchemy as previously mentioned.
  - Create tables.
  - Experienced MySQL before switching to sqlite3 for this project.
- Javascript: I was required to write a little bit of javascript during this project, I am not proficient with javascript at this point but I am familiar.
- Chart.js: I used a javascript library called Chart.js to create a graph on a webpage that displayed balance history. I learned:
  - Basic javascript syntax and how it mirrors that of JSON.
  - How to retrieve information from a url using the javascript fetch command.
  - How to serialize information from python into json format and give it to javascript.
- Json: I had not worked with json file formats before, and I became completely comfortable with the json format during this project.
- Module structure: I learned how to make the python interpreter see folders and files as modules and submodules in python, creating an __init__ file and accessing that module.
- Server Setup: I learned how to setup and configure a web hosting server:
  - Getting a domain name.
  - Getting an SSL certificate and setting up https.
  - Used Nginx to serve static files on the website.
  - Used gunicorn to run the flask application.
  - Used UNIX supervisor to ensure gunicorn was always running on the server.
  - Used UNIX crontabs to set jobs to be executed at certain times.