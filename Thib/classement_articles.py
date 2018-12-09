#!/home/thib/Documents/Travail/ENPC/2A_IMI/TDLog/Projet/env-projetTDlog/bin/python3

import gensim as gs

def findSimilar(word):
    modelTest = gs.models.KeyedVectors.load_word2vec_format('../../freebase-vectors-skipgram1000.bin', binary=True)
    print(modelTest.most_similar(positive=['woman','king'], negative=['man'], topn=1))

findSimilar('temp')
