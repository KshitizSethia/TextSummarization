import numpy as np

ref = np.arange(25).reshape(5, 5)

dist_matrix = np.zeros((5, 5), dtype='float64')

for row in range(len(ref)):
    for col in range(len(ref[0])):
        # fill only lower triangle
        # new
        if(row == col):continue
        # new
        elif(row > col):dist_matrix[row, col] = dist_matrix[col, row]
        #new
        else: dist_matrix[row, col] = ref[row, col]


#new
sums = np.copy(dist_matrix[:, 0])
for col in range(1, len(dist_matrix[0])):
    sums += dist_matrix[:, col]

numSentencesToSelect = 3  # int(len(sentences) * settings.summaryFraction)
selectedSentences = []
masked_dist_matrix = np.ma.array(dist_matrix, mask=np.zeros(dist_matrix.shape).astype('bool'))
masked_sums = np.ma.array(sums, mask=[False]*len(sums))

while(numSentencesToSelect > 0):
    indexOfMostConnectedSentence = np.argmin(masked_sums)
    
    masked_sums -= masked_dist_matrix[:, indexOfMostConnectedSentence]
    masked_dist_matrix.mask[:,indexOfMostConnectedSentence] = True
    masked_dist_matrix.mask[indexOfMostConnectedSentence, :] = True
    masked_sums.mask[indexOfMostConnectedSentence] = True
    
    selectedSentences.append(indexOfMostConnectedSentence)
    
    numSentencesToSelect -= 1

np.sort(selectedSentences)

print selectedSentences
