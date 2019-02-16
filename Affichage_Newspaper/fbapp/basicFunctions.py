from googlesearch import search
import requests
import re
from bs4 import BeautifulSoup
import urllib
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import csv
import os
from stop_words import get_stop_words
from newspaper import Article
import pyimgur
from newsapi import NewsApiClient

CLIENT_ID = "9f812cf018aa2cb"
newsapi_key = "d2f6b8506b584d45b8ddbb7b19814ca1"

def listToString(keywords): # Pour l'affichage lorsqu'aucun article n'est trouvé
    keystring = ""
    for key in keywords:
        keystring += key.lower() + ", "
    keystring = keystring[:-2]
    return keystring

def StringToList(str): # Pour l'affichage lorsqu'aucun article n'est trouvé
    if len(str) > 0:
        return(str.split(', '))
    else:
        return(str)

def time_to_parameter(time):
    if (time == 'hour'):
        return('qdr:h')
    elif (time == 'day'):
        return('qdr:d')
    elif (time == 'week'):
        return('qdr:w')
    elif (time == 'month'):
        return('qdr:m')

def website_name(adress): # Method exhaustive, piste d'amélioration
    site = ''
    if (adress == 'http://www.nytimes.com'):
        site = 'the-new-york-times'
    elif (adress == 'https://www.theguardian.com'):
        site = 'the-guardian-uk'
    elif (adress == 'https://www.economist.com'):
        site = 'the-economist'
    elif (adress == 'http://www.huffingtonpost.com'):
        site = 'the-huffington-post'
    elif (adress == 'http://time.com'):
        site = 'time'
    elif (adress == 'http://www.theverge.com'):
        site = 'the-verge'
    return(site)




def google_news_website(keywords, website, nb_article, time = '0'):
    """
    fonction faisant une recherche sur google classique
    input :
    1- keywords : une liste de mots clefs de la forme ['keyword1','keyword2',...]
    2- web_site : une string du site web sur lequel chercher le/les articles, ex : 'www.theguardian.com'
    3- nb_article : un entier, nombre d'url a selectionner
    4- time : une string sur la limite de temps de parution de l'article
    output :
    1- sites = une liste des url des articles trouvés sur le web de la forme ['url1','url2',...]
    """
    query = ''
    sites = []
    for keyword in keywords:
        query += keyword + ' '
    if (len(website)!=0):
        query += 'site:' + website
    print(query)
    if (time != '0'):
        time = time_to_parameter(time)
    count = 0
    for url in search(query, tld='com', lang='en', tbs=time, num=10, start=0, stop=nb_article, pause=2.0, tpe='nws'):
        if(count < nb_article):
            print(url)
            sites.append(url)
            count += 1
        else:
            break
    return(sites)

def google_news_search(keywords, nb_article, time = '0'):
    """
    fonction faisant une recherche sur google news
    input :
    1- keywords : une liste de mots clefs de la forme ['keyword1','keyword2',...]
    2- nb_article : un entier, nombre d'url a selectionner
    output :
    1- sites = une liste des url des articles trouvés sur le web de la forme ['url1','url2',...]
    """
    query = ''
    for keyword in keywords:
        query += keyword + ' '
    if (time != '0'):
        time = time_to_parameter(time)
    sites = []
    count = 0
    for url in search(query, tld='com', lang='en', tbs=time, num=10, start=0, stop=nb_article, pause=2.0, tpe='nws'):
        if(count < nb_article):
            sites.append(url)
            count += 1
        else:
            break
    return(sites)

def create_wordcloud(text, nb_words, banned_words = []):
    stopwords = set(STOPWORDS)
    stopwords.update(banned_words)
    rgb = 'RGB'
    roman_color = 'rgb(118,153,204)'
    transparent = 'rgba(255, 255, 255, 0)'
    rgba = 'RGBA'
    return(WordCloud(stopwords=stopwords, max_font_size=50, max_words=nb_words, background_color=roman_color, mode=rgb, color_func=lambda *args, **kwargs: (37,48,64)).generate(text))

def display_wordcloud(wordcloud):
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def save_wordcloud(wordcloud, file_name):
    path = 'css/images/' + file_name + '.png'
    save_path = 'fbapp/static/' + path
    print('save_path = {}'.format(save_path))
    wordcloud.to_file(save_path)
    return(path)

def upload_wordcloud(path, name):
    im = pyimgur.Imgur(CLIENT_ID)
    path = path + name + ".png"
    uploaded_image = im.upload_image(path, title="test")
    final_link = uploaded_image.link
    print("final_link = {}".format(final_link))
    return(final_link)


def data(chemin):
    """
Fonction qui prend un chemin et transforme en un string du texte
    """
    f= open(chemin)
    text=""
    nb_lignes=0
    for i in f:
        if i!='':
            nb_lignes+=1
    f.close()

    f= open(chemin)
    for i in range(nb_lignes):
        ligne=f.readline()
        ligne=ligne.replace("\n"," ")
        ligne=ligne.replace("\n\r"," ")
        text+=ligne
    f.close()
    return(text)


def wordcloud_url(url_list, nb_words, name):
    """
    Creer un nuage de mots à partir d'une liste d'url d'articles
    """
    text = ''
    for url in url_list:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        for keyword in article.keywords:
            text += keyword + ' '
    stop_english = get_stop_words('english')
    cloud = create_wordcloud(text, nb_words, stop_english)
    save_wordcloud(cloud, name)
    return(cloud)

def wordcloud_keyword(keyword_list, nb_words, name):
    """
    Creer un nuage de mots à partir d'une liste de mots-clés
    """
    text = ''
    url_list = google_news_search(keyword_list, nb_article = 5, time = 'day')
    for url in url_list:
        print(url)
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        for keyword in article.keywords:
            text += keyword + ' '
    stop_english = get_stop_words('english')
    cloud = create_wordcloud(text, nb_words, stop_english)
    save_wordcloud(cloud, name)
    return(cloud)


newsapi = NewsApiClient(api_key=newsapi_key)

def get_api(keywords, nb_article, website=''):
    """
    Recherche d'articles à partir de mots clés en utilisant l'API "newsapi"
    """
    query = ''
    for keyword in keywords:
        query += keyword + ' '
    search = newsapi.get_everything(q=query, language='en')
    if (len(website)!=0):
        print("website={}".format(website))
        site = website_name(website)
        search = newsapi.get_everything(q=query, sources=site, language='en')
    articles = search["articles"]
    return(articles)

if __name__ == '__main__':
    get_api(['bitcoin', 'island'], 5)
