from googlesearch import search
import requests
import re
from bs4 import BeautifulSoup
import urllib

def listToString(keywords): # Pour l'affichage lorsqu'aucun article n'est trouvé
    keystring = ""
    for key in keywords:
        keystring += key.lower() + ", "
    keystring = keystring[:-2]
    return keystring


def google_news_website(keywords, website, nb_article):
    """
    fonction faisant une recherche sur google classique
    input :
    1- keywords : une liste de mots clefs de la forme ['keyword1','keyword2',...]
    2- web_site : une string du site web sur lequel chercher le/les articles, ex : 'www.theguardian.com'
    3- nb_article : un entier, nombre d'url a selectionner
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
    count = 0
    for url in search(query, tld='com', lang='en', num=10, start=0, stop=nb_article, pause=2.0, tpe='nws'):
        if(count < nb_article):
            print(url)
            sites.append(url)
            count += 1
        else:
            break
    return(sites)

def google_news_search(keywords, nb_article):
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
    sites = []
    count = 0
    #for url in search(query, tld='com', lang='en', num=10, start=0, stop=nb_article, pause=2.0, tpe='nws', params_perso='tbs=ctr:countryUK%7CcountryGB&cr=countryUK%7CcountryGB'):
    for url in search(query, tld='com', lang='en', num=10, start=0, stop=nb_article, pause=2.0, tpe='nws'):
        if(count < nb_article):
            sites.append(url)
            count += 1
        else:
            break
    return(sites)

# def google_news_search_v2(keywords, nb_url):
#     url = 'https://news.google.com/search?q={query}&hl=en-GB&gl=GB&ceid=GB%3Aen'
#     temp = ''
#     for keyword in keywords:
#         temp += keyword + '%20'
#     url = url.format(query=temp)
#     page = requests.get(url)
#     anchors = soup.find(id='search').findAll('a')
#     for a in anchors:
#         try:
#             link = a['href']
#         except KeyError:
#             continue
#     # soup = BeautifulSoup(page.content, 'html.parser')
#     # print(page.status_code)
#     # for news in soup.findAll("div", {"class": "st"}):
#     #     print(news.link)
#     return(['https://www.theguardian.com/business/2017/jul/20/french-dutch-culture-clash-revealed-leaked-air-france-klm-report'])


if __name__ == "__main__":
    test = google_news_website(['cesq', 'fabregas', 'monaco'], 'www.mirror.co.uk', 2)
