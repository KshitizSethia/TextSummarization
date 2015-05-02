from __future__ import division

import settings
import os
import cPickle
import string
import numpy as np
import sys

from colorama import Fore, Back, Style
import colorama
import gensim
from gensim.models.word2vec import Word2Vec
import re

model = Word2Vec.load(settings.word2vecModel)

colorama.init()

verbose = False
veryVerbose = False
if('-v' in sys.argv): verbose = True
if('-vv' in sys.argv): verbose = True; veryVerbose = True

stopwords = [word.strip() for word in open(settings.stopwords).readlines()]

sentence_splitter = re.compile("([A-Za-z0-9]+ [A-Za-z0-9]+)([\.!?]) [A-Z]")
def getSentences(para):
    result = []
    last_match=0
    matches = sentence_splitter.finditer(para)
    for match in matches:
        sent = para[last_match:match.start(2)]
        result.append(sent)
        last_match = match.start(2)+2
    return result


def getSentenceDistance(sentence1, sentence2, normalizeForLength=True):
    
    # mandating sentence1 is shorter sentence
    if(len(sentence1) > len(sentence2)):
        return getSentenceDistance(sentence2, sentence1, normalizeForLength)
    
    # assuming sentence 1 is smaller!!
    # matrix has sentence1 in columns and sentence2 in rows
    
    words1 = sentence1.split()
    words2 = sentence2.split()
    
    matrix = np.ones((len(words2), len(words1)), dtype='float64')
    matrix = np.ma.array(matrix, mask=np.zeros(matrix.shape).astype('bool'))
    # done take largest unsigned float aas data type
    # notdone initial set to largest possible value (infinity?)
    
    wordsInSentence1 = [True] * len(words1)
    # start calculating distance
    for row in range(matrix.shape[0]):
        word2 = words2[row]
        vec2 = []
        if(word2 in model): vec2 = model[word2]
        else:
            matrix.mask[row, :] = True
            continue
        for col in range(matrix.shape[1]):
            word1 = words1[col]
            if(word1 in model):
                vec1 = model[word1]
                matrix[row, col] = np.linalg.norm(vec1 - vec2)
                if veryVerbose: print word1, word2, "similarity", matrix[row, col]
            else:
                matrix.mask[row, col] = True
                wordsInSentence1[col] = False  # todo would look over this word in next iteration, prevent that
    
    validWordsInSentence1 = 0
    for val in wordsInSentence1:
        if val == True:
            validWordsInSentence1 += 1  
          
    # select closest words
    selectionsLeft = validWordsInSentence1
    sumOfDistances = 0
    while(selectionsLeft > 0):
        min_row, min_col = np.unravel_index(np.argmin(matrix), matrix.shape)
        if(veryVerbose): print ("min row and column in sentence", min_row, min_col)
        sumOfDistances += matrix[min_row, min_col]
        matrix.mask[min_row, :] = True  # = np.delete(matrix, min_row, axis=0)
        matrix.mask[:, min_col] = True  # = np.delete(matrix, min_col, axis=1)
        if(veryVerbose): print matrix
        selectionsLeft -= 1
    # done make sure that all words from sentence 1 are selected    
    
    if(verbose and validWordsInSentence1==0):
        print "error: no valid words in "
        print "    " +sentence1
            
    
    if(normalizeForLength):
        return sumOfDistances / max(1,validWordsInSentence1)
    else:
        return sumOfDistances

def main():
    for filename in os.listdir(settings.data_folder):
    
        try:
            # get article
            path = os.path.join(settings.data_folder, filename)
            thisArticle = cPickle.load(open(path, "rb"))
            
            # get sentences from paras
            sentences = []
            for index in range(len(thisArticle.paras)):
                if index in thisArticle.sections["intro"]:
                    continue
                para = thisArticle.paras[index]
                try:
                    sentences.extend(getSentences(para))
                except Exception:
                    pass
            
            original_sentences = np.copy(sentences)

            # words to phrases
            bigram = gensim.models.Phrases(sentences)
            trigram = gensim.models.Phrases(bigram[sentences])
            sentences = [string.join(trigram[sentence.split(" ")]) for sentence in sentences]
            # remove stopwords
            sentences = [string.join([word for word in sentence.split(" ") if word not in stopwords]) for sentence in sentences]
            # remove punctuations
            sentences = [str(sentence).translate(string.maketrans("", ""), string.punctuation) for sentence in sentences]
            
            
            # fill similarity matrix
            dist_matrix = np.zeros((len(sentences), len(sentences)), dtype='float64')  # np.ones((len(sentences), len(sentences)), dtype='float64')* float('Inf')
            # done take largest unsigned float aas data type
            # done initial set to largest possible value (infinity?)
            
            for row in range(len(sentences)):
                for col in range(len(sentences)):
                    # fill only lower triangle
                    if(row == col):continue
                    elif(row > col): dist_matrix[row, col] = dist_matrix[col, row]
                    else: dist_matrix[row, col] = getSentenceDistance(sentences[row], sentences[col])
            
            
            # initialize sum array to calculate sentences at max distance from others
            sums = dist_matrix[:, 0]
            for col in range(1, len(dist_matrix[0])):
                sums += dist_matrix[:, col]
            
            numSentencesToSelect = int(len(sentences) * settings.summaryFraction)
            selectedSentences = []
            masked_dist_matrix = np.ma.array(dist_matrix, mask=np.zeros(dist_matrix.shape).astype('bool'))
            masked_sums = np.ma.array(sums, mask=[False] * len(sums))
            
            while(numSentencesToSelect > 0):
                indexOfMostConnectedSentence = np.argmin(masked_sums)
                masked_sums -= masked_dist_matrix[:, indexOfMostConnectedSentence]
                masked_dist_matrix.mask[:, indexOfMostConnectedSentence] = True
                masked_dist_matrix.mask[indexOfMostConnectedSentence, :] = True
                masked_sums.mask[indexOfMostConnectedSentence] = True
                selectedSentences.append(indexOfMostConnectedSentence)
                
                numSentencesToSelect -= 1
            
            np.sort(selectedSentences)
            
            print "------------SUMMARY of " +filename
            for index in range(len(original_sentences)):
                if(index in selectedSentences):
                    print original_sentences[index]
                	#print(Back.GREEN +original_sentences[index] +Back.RESET)
                #else:
                #    print original_sentences[index]
            print "------------SUMMARY END------------"
        except Exception as err:
            print "ERROR:"
            print err
			

if __name__ == "__main__":
    main()
