from googlesearch import search

def listToString(keywords): # Pour l'affichage lorsqu'aucun article n'est trouvé
    keystring = ""
    for key in keywords:
        keystring += key.lower() + ", "
    keystring = keystring[:-2]
    return keystring


def google_search_website(keywords, website, nb_url):
    """
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
    for url in search(query, tld="com", num=nb_url, stop=nb_url, pause=2):
        print(url)
        sites.append(url)
    return(sites)



# def google_news_search(**params):
#     template = 'https://www.google.com/search?pz=1&cf=all&ned=us&hl=en&tbm=nws&gl=us&as_q={query}&as_occt=any&as_drrb=b&as_mindate={month}%2F%{from_day}%2F{year}&as_maxdate={month}%2F{to_day}%2F{year}&tbs=cdr%3A1%2Ccd_min%3A3%2F1%2F13%2Ccd_max%3A3%2F2%2F13&as_nsrc=Gulf%20Times&authuser=0'
#     response = requests.get(template.format(**params))
#
#
# google_news_search(query="Egypt", month=3, from_day=2, to_day=2, year=13)
