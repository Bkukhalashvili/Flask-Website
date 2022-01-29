# Flask Website
## General Info
Website is written in Python, using Flask Framework. <br>
For texts and visuals I used one of my favorite games Mass Effect  as an inspiration. 

* Basic users can see/use: blog posts (also filter them with username),  Nasa's API (apod) and filter data from SQLite.
* Registered users can see/use:  all the above plus access account page, parsed currency rates, create blog posts and edit/delete them.


# Technologies
Project is created with: <br>

* Python 3.9.6 
* SQLite 3.37.0
* Flask 2.0.1
* Flask-SQLAlchemy 2.5.1
* Flask-Login 0.5.0
* Flask-WTF 0.15.1
* Pillow 8.3.2
* BeautifulSoup4 4.9.3
* Requests 2.26.0
* flask_bcrypt 0.7.1
* email_validator 1.1.3

# Launch
### Before you try to run the project you need to edit config.py :
```
class Config:
    SECRET_KEY = "Type secret key here"
    API_KEY = "Type Nasa's API Key here"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
```
For Secret Key you need a string that contains a good set of random characters, for this open the CMD and type: <br>
1. ```python ```
2. ```import secrets```
3. ```secrets.token_hex(16)```

      
For API Key you need to get a free Nasa's API Key from <a href="https://api.nasa.gov" target="_blank">here</a>

### If you want to run the project without editing config.py :

Create environment variables with same name and give values there. <br>
How to do this on :
<a href="https://www.youtube.com/watch?v=IolxqkL7cD8" target="_blank">Windows</a> 
/
<a href="https://www.youtube.com/watch?v=5iWhQWVXosU&t=0s" target="_blank">Mac and Linuxs</a>


## Run the project

Before running the project install all the dependencies, type: ```pip install -r requirements.txt``` in the terminal. <br>
To run the project type: ```python run.py``` in the terminal.
