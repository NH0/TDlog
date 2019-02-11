from flask import Flask, render_template, url_for, request, session, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_hashing import Hashing
from pprint import pprint

app = Flask(__name__) # Base de données pour les articles
app.config.from_object('config')
db = SQLAlchemy(app)
hashing = Hashing(app)

from .utils import *
from .utils_authentification import login_successful, user_not_in_database, find_interests_in_db
from newspaper import Article
from .models import User, Article_c, Votes


@app.route('/article', methods=['GET', 'POST'])
def projet():

    sources = []

    if request.method == 'POST':
        keywords = request.form['keywords'].replace(" ","").split(',') # créer une liste de string contenant les mots-clés
        for news_site in News_Sites:
            if(request.form.get(news_site)):
                sources.append(news_site)
    else:
        keywords = request.args.get('keywords').replace(" ","").split(',')
        for news_site in News_Sites:
            if (request.args.get(news_site)):
                sources.append(news_site)

    # for key in keywords:
    #     key = key.lower() # insensible à la casse
    keywords = formatKeywords(keywords)
    stringOfKeywords = listToString(keywords)

    # articles_list = find_article_db(keywords, sources)  # cherche l'article dans la base de données
    #
    # if (articles_list == 0):    # si aucun article ne correspond dans la BDD, le chercher sur google news
    #     if len(sources)==0:
    #         articles_list = find_article_news(keywords, nb_article = 2)   # cherche nb_article articles
    #     else:
    #         articles_list = find_article_news_from(keywords, 2, sources) # cherche l'article dans la base de données en ne gardant que les articles provenant de certains sites d'information
    #         #for article in articles_list:
    #             #article.keyword=listToString(liteClient.getKeywords(article.text.encode('utf-8')))))
    #             #Cette etape prend du temps, il faut trouver un autre endroit pour le faire
    #             #db.session.add(article)
    #             #db.session.commit()
    # articles_list = sorted(articles_list, key=lambda x: x.note, reverse=True) #Triés par préférences des utilisateurs
    articles_list = find_article_db_and_news(keywords,sources)
    return render_template('projet.html',
                            articleList = articles_list[0:2], # on affiche que les 2 premiers articles
                            searchedKeywords = stringOfKeywords,)

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
    password = hashing.hash_value(password, salt='GrisThibVeloCast')
    if(user_not_in_database(username)):
        db.session.add(User(username = username,
                            password = password,
                            interests = interests))
        db.session.commit()
        flash("You are now registered, welcome :)") #Registered but not logged in ! maybe redirect to login.html ?
        return redirect(url_for("login_page"))
    else:
        flash("This name is already taken, try something else")
        return redirect(url_for("signup"))

# Profile page
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if ('logged_in' in session) and session['logged_in']:
        userInterests = find_interests_in_db(session['username'])
        return render_template('profile.html',
                                username = session['username'],
                                interests = userInterests,
                                userArticles = find_article_db_and_news(list(userInterests)))
    else:
        flash("You must be logged in to view your profile !")
        return redirect(url_for("login_page"))

@app.route('/rateArticle', methods=['GET','POST'])
def notation():
    if ('logged_in' in session) and session['logged_in']:

        id = int(request.form['idA'])
        noteA = int(request.form['note'])

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
            flash("You rated \""+articleNoted.title+"\" "+str(noteA)+"/5.")

        else:
            flash("You already rated the article !")

    else:
        session['logged_in'] = False
        flash("You must be logged in to vote !")
    return redirect(url_for("home"))
