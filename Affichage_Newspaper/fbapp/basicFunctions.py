from nltk.corpus import wordnet
from itertools import chain

def findSynonyms(word):
    SetOfSynonyms = wordnet.synsets(word)
    synonyms = set([]) # Unique elements
    for syn in SetOfSynonyms:
        for name in syn.lemma_names():
            synonyms.add(name)
        for hyperList in syn.hypernyms():
            for hyper in hyperList.lemma_names():
                synonyms.add(hyper)
        for hypoList in syn.hyponyms():
            for hypo in hypoList.lemma_names():
                synonyms.add(hypo)
    return (synonyms)

def listToString(keywords): # Pour l'affichage lorsqu'aucun article n'est trouvé
    keystring = ""
    for key in keywords:
        keystring += key.lower() + ", "
    keystring = keystring[:-2]
    return keystring
