from flask import Flask, render_template, url_for, request, session, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_hashing import Hashing
from pprint import pprint #used for debugging
import retinasdk

app = Flask(__name__) # Base de données pour les articles, les utilisateurs et les notes
app.config.from_object('config')
db = SQLAlchemy(app)
hashing = Hashing(app)

api_key="eabe2bc0-1286-11e9-bb65-69ed2d3c7927"

from .utils import * # Fonctions utilitaires,
from .utils_authentification import *
from newspaper import Article
from .models import *

NUMBER_OF_ARTICLES_PER_SEARCH = 2
News_Sites = ['https://www.theguardian.com','https://www.nytimes.com','https://www.economist.com']

@app.route('/article', methods=['GET', 'POST'])
def projet():
    """
    Recherche des articles en fonctions des mots clés entrés
    S'il n'y a pas d'articles, renvoie vers un page d'erreur
    Sinon renvoie vers l'affichage
    """
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
    articles_list = find_article_api_from(keywords, NUMBER_OF_ARTICLES_PER_SEARCH, sources)

    if (len(articles_list)!=0):
        return render_template('projet.html',
                                articleList = articles_list,
                                searchedKeywords = stringOfKeywords,
                                numberOfArticles = [i for i in range(len(articles_list))])
    elif (len(articles_list)==0):
        site = ''
        for source in sources:
            site = site + website_name(source) + ' & '
        return render_template('erreur.html',
                                keywords = stringOfKeywords,
                                sources = site[:-2])

@app.route('/', methods=['GET', 'POST'])
@app.route('/home/')
def home():
    """
    Page d'accueil
    """
    if not('logged_in' in session): # Permet d'initialiser la valeur de logged_in
        session['logged_in'] = False
    return render_template('home.html')


# Routes relatives à l'identification des utilisateurs
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """
    Traitement du login, après authentification
    """
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
    """
    Traitement des informations entrées pour se connecter au site
    """
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

@app.route('/login/signup/', methods=['GET','POST'])
def signup():
    """
    Page d'inscription
    """
    if not(('logged_in' in session) and session['logged_in']):
        return render_template('sign-up.html')
    else:
        flash("Already logged in !")
        return redirect(url_for("home"))

@app.route('/register-signup', methods=['GET', 'POST'])
def register_signup():
    """
    Traitement des informations entrées lors de l'inscription
    Il y a quelques contraintes, comme le mdp à plus de 6 caracters
    """
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

    if(user_not_in_database(username)): # On verifie qu'il n'existe pas déjà un utilisateur avec le même nom

        session['username'] = username

        # On recherche des articles en lien avec ses intérêts lors du sign up
        keywords = StringToList(interests)
        articles = find_api(keywords, 3)
        urls = []
        for article in articles:
            urls.append(article.url)

        # generation du wordcloud lors du sign-up
        cloud_name = session['username']+'_daily'
        wordcloud_url(urls, 20, cloud_name)
        cloud_path = 'css/images/' + cloud_name + '.png'

        # Ajout de l'utilisateur nouvellement inscrit
        db.session.add(User(username = username,
                            password = password,
                            interests = interests,
                            recommendation = articles,
                            cloud_path = cloud_path))
        db.session.commit()

        # Authentification automatique lors de l'inscription
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

@app.route('/rateArticle', methods=['POST'])
def notation():
    """
    Traitement des notes d'articles
    L'objectif est de ne pas recharger la page d'articles en notant
    Donc l'appel se fait par du JS d'où le retour 204
    Lorsque l'on note un article qui n'est pas dans la base de données, il est ajouté
    """
    # Bien connecté
    if ('logged_in' in session) and session['logged_in']:
        # Requête non vide
        if request.form['urlA'] and request.form['note']: #Not empty post

            urlA = str(request.form['urlA'])
            noteA = int(request.form['note'])

            articleNoted = Article_c.query.filter_by(source_url = urlA).first()

            # Article est ou non dans la base de données
            if articleNoted == None:
                add_article_to_db(urlA)
                db.session.commit()
                articleNoted = Article_c.query.filter_by(source_url = urlA).first()

            id = int(articleNoted.idarticle)

            # Pas de trucage de note
            if noteA in [0,1,2,3,4,5]:

                #Si l'utilisateur n'a pas déjà voté
                if not( Votes.query.filter_by(userid = session['uid'],articleid = id).count() ):

                    # Modification de la table article
                    articleNoted = Article_c.query.filter_by(idarticle = id).first()
                    articleNoted.note = round((articleNoted.note * articleNoted.nbVotes + noteA) / (articleNoted.nbVotes + 1),1)
                    articleNoted.nbVotes = articleNoted.nbVotes + 1

                    db.session.merge(articleNoted)
                    db.session.commit()

                    # Ajout du nouveau vote dans la table Votes
                    db.session.add(Votes(userid=session['uid'],
                                         articleid=id,
                                         note = noteA))
                    db.session.commit()

                    flash("You rated \""+articleNoted.title+"\" "+str(noteA)+"/5.")

                else:
                    flash("You already rated the article !")

            else:
                flash("Notes must be integer between 0 and 5 !")

        else:
            flash("No note or article found !")

    else:
        session['logged_in'] = False
        flash("You must be logged in to vote !")

    # Dans tous les cas, retour 204 : No content
    # car on ne veut rien renvoyer (à part les messages)
    return ('',204)
