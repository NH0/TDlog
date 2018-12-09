def listToString(keywords): # Pour l'affichage lorsqu'aucun article n'est trouvé
    keystring = ""
    for key in keywords:
        keystring += key.lower() + ", "
    keystring = keystring[:-2]
    return keystring
