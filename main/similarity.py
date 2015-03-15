import nltk
from nltk.corpus import stopwords
import re
from collections import Counter
import math

def counter_dot(A_vec, B_vec):
    result = 0
    A_l = list(A_vec)
    B_l = list(B_vec)
    if(len(B_l)<len(A_l)): return counter_dot(B_vec, A_vec)
    return sum(B_vec.get(f, 0) * v for f, v in A_vec.items())
    #for word in A_l:
    #    result+= A_vec[word]*B_vec[word]
    #return result       

def counter_mult(scalar, vector):
    return Counter(dict([(k, v*scalar) for (k, v) in vector.iteritems()]))

def text2vec(text):
    text = re.sub('[~!@$%^&*()_+-=<>?,./;:\'\"{}\[\]\\|]','',text)
    tokens = nltk.word_tokenize(text)
    bigrams = Counter(zip(tokens,tokens[1:]))
    words = Counter(tokens)
    vec = bigrams+words
    #normalize
    total = math.sqrt(sum(map(lambda x:x**2, vec.values())))
    vec = counter_mult(1.0/total, vec)
    return vec
    
    '''
    tokens = nltk.word_tokenize(text)
    bgs = nltk.bigrams(tokens)
    #print bgs
    #bgs_words = bgs + tokens
    fdist_bgs = nltk.FreqDist(bgs)
    #print type(fdist_bgs)
    #print len(fdist_bgs)
    fdist_words = nltk.FreqDist(tokens)
    #TODO: Find a better way to merge two distributions
    fdist = Counter(fdist_bgs.most_common(len(fdist_bgs))) + Counter(fdist_words.most_common(len(fdist_words)))
    print fdist
    #print fdist.values()
    #print map(lambda x:x**2, fdist.values())
    #print map(lambda x:x**2, fdist.values())
    #normalize
    total = math.sqrt(sum(map(lambda x:x**2, fdist.values())))
    fdist = counter_mult(1.0/total, fdist)

    print fdist
    return fdist
    #bigrams = getBigrams(text)
    #text = removeStopwords(text)
    #fdist = FreqDist(text)
    '''

def vec_similarity(vec1, vec2):
    return counter_dot(vec1, vec2)

def text_similarity(text1, text2):
    vec1 = text2vec(text1)
    vec2 = text2vec(text2)
    #print vec1, vec2
    #print vec_similarity(vec1, vec2)
    return vec_similarity(vec1, vec2)

#text2vec("This is a test. This is a test.")
#text_similarity("this is a test", "something random")
