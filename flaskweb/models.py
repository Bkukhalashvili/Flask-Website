import json
from datetime import datetime
from flaskweb import db, login_manager
from bs4 import BeautifulSoup
from flask_login import UserMixin
from flask import session, flash, current_app
import requests


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# user table in db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# post table in db
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


# nasas api (Astronomy Picture of the Day)
def apod(date, quality):

    api_key = current_app.config['API_KEY']
    url = f'https://api.nasa.gov/planetary/apod?date={date}&thumbs=True&api_key={api_key}'
    req = requests.get(url)
    txt = json.loads(req.text)

    try:
        media_type = txt['media_type']
        
        if media_type == 'video':
            status = "Found"
            session['status'] = status
            session['media_type'] = media_type.capitalize()
            session['title'] = txt['title']
            session['explanation'] = txt['explanation']
            vid_url = txt["url"]
            session['vid_url'] = vid_url
            thumb_url = txt["thumbnail_url"]
            session['thumb_url'] = thumb_url
        if quality == 'HD' and media_type == 'image':
            status = "Found"
            session['status'] = status
            session['media_type'] = media_type.capitalize()
            session['title'] = txt['title']
            session['explanation'] = txt['explanation']
            web = txt["hdurl"]
            session['img_link'] = web
            
        if quality == "SD" and media_type == 'image':
            status = "Found"
            session['status'] = status
            session['media_type'] = media_type.capitalize()
            session['title'] = txt['title']
            session['explanation'] = txt['explanation']
            web = txt["url"]
            session['img_link'] = web
            
    except KeyError:
        session['status'] = ''
        flash('ERROR', 'error3') 
        session['date'] = ''
        flash('Wrong Format!', 'error4') 

        session.pop('media_type', None)
        session.pop('quality', None)
        session.pop('title', None)
        session.pop('explanation', None)
        session.pop('img_link', None)
        session.pop('thumb_url', None)
        session.pop('vid_url', None)


# Parsing currency from tbc bank (data is displayed on account page)
def pars_currency():
    
    url = 'https://www.tbcbank.ge/web/ka/web/guest/exchange-rates'
    req = requests.get(url)
    content = req.text
    soup = BeautifulSoup(content, 'html.parser')

# US to GEL
    us_offi = soup.find_all('div', {'class':'currRateTop'})[0]
    us_s = soup.find_all('div', {'class':'currRate'})[0]
    us_b = soup.find_all('div', {'class':'currRate'})[1]

    pars_currency.us_official = ''.join(us_offi).strip()
    session['us_official'] = pars_currency.us_official

    pars_currency.us_sell = ''.join(us_s).strip()
    session['us_sell'] = pars_currency.us_sell

    pars_currency.us_buy = ''.join(us_b).strip()
    session['us_buy'] = pars_currency.us_buy
    # print('official: ' + us_offi + ' ₾', 'sell: ' + us_sell + ' ₾', 'buy: ' + us_buy + ' ₾')

# EUR to GEL
    eur_offi = soup.find_all('div', {'class':'currRateTop'})[1]
    eur_s = soup.find_all('div', {'class':'currRate'})[2]
    eur_b = soup.find_all('div', {'class':'currRate'})[3]
    
    pars_currency.eur_official = ''.join(eur_offi).strip()
    session['eur_official'] = pars_currency.eur_official

    pars_currency.eur_sell = ''.join(eur_s).strip()
    session['eur_sell'] = pars_currency.eur_official

    pars_currency.eur_buy = ''.join(eur_b).strip()
    session['eur_buy'] = pars_currency.eur_official
    # print('official: ' + eur_offi + ' ₾', 'sell: ' + eur_sell + ' ₾', 'buy: ' + eur_buy + ' ₾')
    
# GBP to GEL
    gbp_offi = soup.find_all('div', {'class':'currRateTop'})[2]
    gbp_s = soup.find_all('div', {'class':'currRate'})[4]
    gbp_b = soup.find_all('div', {'class':'currRate'})[5]

    pars_currency.gbp_official = ''.join(gbp_offi).strip()
    session['gbp_official'] = pars_currency.gbp_official

    pars_currency.gbp_sell = ''.join(gbp_s).strip()
    session['gbp_sell'] = pars_currency.gbp_sell

    pars_currency.gbp_buy = ''.join(gbp_b).strip()
    session['gbp_buy'] = pars_currency.gbp_buy
    # print('official: ' + gbp_offi + ' ₾', 'sell: ' + gbp_sell + ' ₾', 'buy: ' + gbp_buy + ' ₾')


# games table in db
class Games(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    URL = db.Column(db.Text, nullable=False)
    
    def __str__(self):
        return f'Game title: {self.title}, Price: ${self.price}'