# Determine the vector subspace containing most of the gender information in a word2vec model

from gensim.models import KeyedVectors
from sklearn.decomposition import PCA
import pickle
import numpy as np


# normalizes a vector
def normalize(x):
        return x / np.sqrt(np.dot(x,x))

modelPath = 'models/word2vec/deu_news_2011-2016'
wordPairsPath = 'data/external/genderedWordPairsExtended.txt'
resultPath = 'results/word2vec/pcaExplainedVarianceExtendedJobs'

# load model
model = KeyedVectors.load_word2vec_format(modelPath, binary = False)
vocab = set(model.index2word)

# load word pairs
with open(wordPairsPath, 'r') as f:
	wordPairs = f.read().splitlines()

# map to vectors
centeredVectors = list()
for pair in wordPairs:
        w1, w2 = pair.split(',')
        if not (w1 in model and w2 in model):
                continue
        w1 = normalize(model[w1])
        w2 = normalize(model[w2])
        c = np.mean([w1,w2], axis = 0)
        centeredVectors.append(np.subtract(w1,c))
        centeredVectors.append(np.subtract(w2,c))

X = np.array(centeredVectors)

# Compute principal components and output the ratios of explained variance
pca = PCA(random_state = 0).fit(X)
print "Explained variance percentage: \n"+str(pca.explained_variance_ratio_)

# Save model, in case we want to use it later
pickle.dump(pca, open("models/pca-"+modelPath.split('/')[-1]+".pickle", "w"))
