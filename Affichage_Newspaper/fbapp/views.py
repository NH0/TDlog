from flask import Flask, render_template, url_for, request, session, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_hashing import Hashing
from pprint import pprint

app = Flask(__name__) # Base de données pour les articles, les utilisateurs et les notes
app.config.from_object('config')
db = SQLAlchemy(app)
hashing = Hashing(app)

from .utils import * # Fonctions utilitaires,
from .utils_authentification import *
from newspaper import Article
from .models import User, Article_c, Votes


@app.route('/article', methods=['GET', 'POST'])
def projet():

    sources = []

    if request.method == 'POST' and request.form['keyword']:
        keywords = StringToList(request.form['keywords']) # créer une liste de string contenant les mots-clés
        for news_site in News_Sites:
            if(request.form.get(news_site)):
                sources.append(news_site)

    elif request.method == 'GET' and request.args.get('keywords'):
        keywords = StringToList(request.args.get('keywords'))
        for news_site in News_Sites:
            if (request.args.get(news_site)):
                sources.append(news_site)

    else:
        flash("You have to enter a keyword !")
        return redirect(url_for("home"))

    if keywords != ["" for k in range(len(keywords))]:
        keywords = formatKeywords(keywords)
        stringOfKeywords = listToString(keywords)

    #articles_list = find_article_db_and_news(keywords, sources, 2)
    articles_list = find_article_api_from(keywords, 2, sources)

    return render_template('projet.html',
                            articleList = articles_list, # on affiche que les 2 premiers articles
                            searchedKeywords = stringOfKeywords)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home/')
def home():
    if not('logged_in' in session):
        session['logged_in'] = False
    return render_template('home.html')


# Routes relatives à l'identification des utilisateurs
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if not(('logged_in' in session) and session['logged_in']):
        return render_template('login.html')
    else:
        flash("Already logged in !")
        return redirect(url_for("home"))

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()

@app.route('/authentification', methods=['GET','POST'])
def do_admin_login():

    POST_USERNAME = request.form['username']
    POST_PASSWORD = request.form['password']

    POST_PASSWORD = hashing.hash_value(POST_PASSWORD,'GrisThibVeloCast')

    result = login_successful(POST_USERNAME, POST_PASSWORD)

    if result:
        session['uid'] = User.query.filter_by(username=POST_USERNAME).first().id
        session['username'] = POST_USERNAME
        session['logged_in'] = True
        flash("Succesfully logged in!")
        return redirect(url_for("home"))
    else:
        flash('Wrong username/password')
        return redirect(url_for("login_page"))

@app.route('/login/signup', methods=['GET','POST'])
def signup():
    if not(('logged_in' in session) and session['logged_in']):
        return render_template('sign-up.html')
    else:
        flash("Already logged in !")
        return redirect(url_for("home"))

@app.route('/register-signup', methods=['GET', 'POST'])
def register_signup():
    username = request.form['username']
    password = request.form['password']
    interests = request.form['interests']

    if len(interests) == 0:
        flash("Enter at least one interest please !")
        return render_template('sign-up.html')

    if len(password) < 6:
        flash("Passwords must be at least 6 characters !")
        return render_template('sign-up.html')

    if len(username) < 3:
        flash("Usernames must be at least 3 characters !")
        return render_template('sign-up.html')

    password = hashing.hash_value(password, salt='GrisThibVeloCast')

    keywords = StringToList(interests)
    articles = find_api(keywords, 3)
    urls = []
    for article in articles:
        urls.append(article.url)

    if(user_not_in_database(username)):

        session['username'] = username

        # generation du wordcloud lors du sign-up
        cloud_name = session['username']+'_daily'
        wordcloud_url(urls, 20, cloud_name)
        cloud_path = 'css/images/' + cloud_name + '.png'

        db.session.add(User(username = username,
                            password = password,
                            interests = interests,
                            recommendation = articles,
                            cloud_path = cloud_path))
        db.session.commit()

        session['uid'] = User.query.filter_by(username=username).first().id
        session['logged_in'] = True
        flash("You are now registered and logged in, welcome :)")
        return redirect(url_for("home"))
    else:
        flash("This name is already taken, try something else")
        return redirect(url_for("signup"))

# Profile page
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if ('logged_in' in session) and session['logged_in']:
        if request.method == 'POST':
            new_interest = request.form['add-interest']
            if len(new_interest) > 0:
                new_interest = formatKeywords(new_interest)
                isNewInterest = new_interest in StringToList(User.query.filter_by(username = session['username']).first().interests)

                if not(isNewInterest):
                    user = User.query.filter_by(username = session['username']).first()
                    user.interests = user.interests + ', ' + new_interest
                    db.session.merge(user)
                    db.session.commit()

        interests = StringToList(find_interests_in_db(session['username']))
        recom = find_recommandation_in_db(session['username'])
        cloud_name = find_cloud_path_in_db(session['username'])
        return render_template('profile.html',
                                username = session['username'],
                                interests = interests,
                                cloud_name = cloud_name,
                                recommendation = recom)
    else:
        flash("You must be logged in to view your profile !")
        return redirect(url_for("login_page"))

@app.route('/rateArticle', methods=['GET'])
def notation():
    pprint("Inside notation")
    if ('logged_in' in session) and session['logged_in']:

        # id = int(request.form['idA'])
        # noteA = int(request.form['note'])
        id = int(request.args.get('idA'))
        noteA = int(request.args.get('note'))
        if noteA in [0,1,2,3,4,5]:

            if not( Votes.query.filter_by(userid = session['uid'],articleid = id).count() ):

                articleNoted = Article_c.query.filter_by(idarticle = id).first()
                articleNoted.note = round((articleNoted.note * articleNoted.nbVotes + noteA) / (articleNoted.nbVotes + 1),1)
                articleNoted.nbVotes = articleNoted.nbVotes + 1

                db.session.merge(articleNoted)
                db.session.commit()

                db.session.add(Votes(userid=session['uid'],
                                     articleid=id,
                                     note = noteA))
                db.session.commit()
                pprint("You rated \""+articleNoted.title+"\" "+str(noteA)+"/5.")
                return redirect(url_for('profile'))

            else:
                pprint("You already rated the article !")
                #return redirect(url_for('profile'))
        else:
            pprint("Notes must be integer between 0 and 5 !")

    else:
        session['logged_in'] = False
        pprint("You must be logged in to vote !")
        return redirect(url_for('home'))
