from __future__ import division
 
import settings
import os
import cPickle
import numpy as np
from gensim.models.word2vec import Word2Vec

model = Word2Vec()
model.load(settings.word2vecModel)

def getSentenceDistance(sentence1, sentence2, normalizeForLength=True):
    
    # mandating sentence1 is shorter sentence
    if(len(sentence1) > len(sentence2)):
        return getSentenceDistance(sentence2, sentence1, normalizeForLength)
        # todo swap indices
        # todo transpose matrix
        # todo return
    
    # assuming sentence 1 is smaller!!
    # matrix has sentence1 in columns and sentence2 in rows
    
    words1 = sentence1.split()
    words2 = sentence2.split()
    
    matrix = np.ones((len(words2), len(words1)), dtype='float64')
    # done take largest unsigned float aas data type
    # notdone initial set to largest possible value (infinity?)
    
    # start calculating distance
    for row in range(matrix.size[0]):
        for col in range(matrix.size[1]):
            vec1 = model[words1[col]]
            vec2 = model[words2[row]]
            
            matrix[row, col] = np.linalg.norm(vec1 - vec2)
          
    # select closest words
    selectionsLeft = len(words1)
    sumOfDistances = 0
    while(selectionsLeft > 0):
        min_row, min_col = np.unravel_index(np.argmin(matrix), matrix.shape)
        print (min_row, min_col)
        sumOfDistances += matrix[min_row, min_col]
        matrix = np.delete(matrix, min_row, axis=0)
        matrix = np.delete(matrix, min_col, axis=1)
        print matrix
        selectionsLeft -= 1
    # done make sure that all words from sentence 1 are selected    
    
    if(normalizeForLength):
        return sumOfDistances / len(words1)
    else:
        return sumOfDistances

def main():
    for filename in os.listdir(settings.data_folder):
        # get article
        path = os.path.join(settings.data_folder, filename)
        thisArticle = cPickle.load(open(path, "rb"))
        
        # get sentences from paras
        sentences = []
        for para in thisArticle.paras:
            # todo words to phrases
            # todo remove stopwords from para
            # todo remove punctuations as well
            sentences.extend(para.split("."))
        
        # fill similarity matrix
        dist_matrix = np.zeros((len(sentences), len(sentences)), dtype='float64')#np.ones((len(sentences), len(sentences)), dtype='float64')* float('Inf')
        # done take largest unsigned float aas data type
        # done initial set to largest possible value (infinity?)
        
        for row in range(len(sentences)):
            for col in range(len(sentences)):
                # fill only lower triangle
                if(row == col):continue
                elif( row>col): dist_matrix[row,col] = dist_matrix[col, row]
                else: dist_matrix[row, col] = getSentenceDistance(sentences[row], sentences[col], maxSelections=0)
        
        
        # initialize sum array to calculate sentences at max distance from others
        sums = dist_matrix[:, 0]
        for col in range(1, len(dist_matrix[0])):
            sums += dist_matrix[:, col]
        
        numSentencesToSelect = int(len(sentences) * settings.summaryFraction)
        selectedSentences = []
        masked_dist_matrix = np.ma.array(dist_matrix, mask=np.zeros(dist_matrix.shape).astype('bool'))
        masked_sums = np.ma.array(sums, mask=[False]*len(sums))
        
        while(numSentencesToSelect > 0):
            indexOfMostConnectedSentence = np.argmin(masked_sums)
            masked_sums-=masked_dist_matrix[:,indexOfMostConnectedSentence]
            masked_dist_matrix.mask[:,indexOfMostConnectedSentence] = True
            masked_dist_matrix.mask[indexOfMostConnectedSentence, :] = True
            masked_sums.mask[indexOfMostConnectedSentence] = True
            selectedSentences.append(indexOfMostConnectedSentence)
            
            numSentencesToSelect -= 1
        
        np.sort(selectedSentences)
        
        for index in selectedSentences:
            print sentences[index]
        

if __name__ == "__main__":
    main()
