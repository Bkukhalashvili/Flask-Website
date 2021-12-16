from flask import render_template, session,flash, request, Blueprint
from flaskweb.models import Post, apod, Games

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html', title='Home')


# Contains posts added by users 
@main.route("/news")
def news():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('news.html', title='News', posts=posts)


# you can filter data from games table in site.db
@main.route('/filter', methods=['GET', 'POST'])
def filter():
    
    if  request.method == 'POST':
        select = request.form.get('price')
        session['games'] = 'Games'

        if select == 'Under $10':
            session['filter'] = select
            filtered_games = Games.query.filter(Games.price <= '10').all()
            return render_template("filter.html", filtered_games=filtered_games, title='Filter')

        if select == 'Under $15':
            session['filter'] = select
            filtered_games = Games.query.filter(Games.price <= '15').all()
            return render_template("filter.html", filtered_games=filtered_games, title='Filter')

        if select == 'Under $25':
            session['filter'] = select
            filtered_games = Games.query.filter(Games.price <= '25').all()
            return render_template("filter.html", filtered_games=filtered_games, title='Filter')

        if select == 'Over $25':
            session['filter'] = select
            filtered_games = Games.query.filter(Games.price >= '25').all()
            return render_template("filter.html", filtered_games=filtered_games, title='Filter')
    else:
        session.pop('games', None)
        session.pop('filter', None)
        return render_template('filter.html', title='Filter')


# Media page contains nasas api (Astronomy Picture of the Day) (main code is in models.py (apod))
@main.route('/media', methods=['GET', 'POST'])
def media():

    if request.method == 'POST':
        session.pop('img_link', None)
        session.pop('thumb_url', None)
        session.pop('vid_url', None)

        date = request.form.get('datee')
        session['date'] = date
        quality = request.form.get('quality')
        session['quality'] = quality

        if date != '':
            apod(date, quality)

            return render_template('media.html', title='Media')

        if date == '':
            session.pop('status', None)
            session.pop('media_type', None)
            session.pop('date',None)
            session.pop('quality', None)
            session.pop('title', None)
            session.pop('explanation', None)
            session.pop('img_link', None)
            session.pop('thumb_url', None)
            session.pop('vid_url', None)

            flash('Please Enter The Date', 'error2') #!###

            return render_template('media.html', title='Media')
    return render_template('media.html', title='Media')