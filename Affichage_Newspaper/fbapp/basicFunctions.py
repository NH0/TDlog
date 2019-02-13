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

CLIENT_ID = "9f812cf018aa2cb"

def listToString(keywords): # Pour l'affichage lorsqu'aucun article n'est trouvé
    keystring = ""
    for key in keywords:
        keystring += key.lower() + ", "
    keystring = keystring[:-2]
    return keystring

def StringToList(str): # Pour l'affichage lorsqu'aucun article n'est trouvé
    return(str.split(', '))

def time_to_parameter(time):
    if (time == 'hour'):
        return('qdr:h')
    elif (time == 'day'):
        return('qdr:d')
    elif (time == 'week'):
        return('qdr:w')
    elif (time == 'month'):
        return('qdr:m')

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
    #for url in search(query, tld='com', lang='en', num=10, start=0, stop=nb_article, pause=2.0, tpe='nws', params_perso='tbs=ctr:countryUK%7CcountryGB&cr=countryUK%7CcountryGB'):
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
    print('path = {}'.format(path))
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



if __name__ == '__main__':
    # sites = google_news_search('politics', nb_article = 5, time = 'day')
    # wordcloud2(['politics', 'brexit'], 20, 'test5')
    #print(upload_wordcloud('static/css/images', 'clems_daily'))
    fichier = open('fbapp/texte.txt', 'r')
    text = fichier.read()
    stop_english = get_stop_words('english')
    test = create_wordcloud(text, 20, stop_english)
    # #display_wordcloud(test)
    # save_wordcloud(test, 'transparent')
    # #test = google_news_website(['cesq', 'fabregas', 'monaco'], 'www.mirror.co.uk', 2)
    print(type("hey"))
