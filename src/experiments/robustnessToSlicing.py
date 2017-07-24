# Test the robustness of bias tests by training models on different slices and permutations of a corpus

import os
import sys
sys.path.insert(0, 'src/train/word2vec')
sys.path.insert(0, 'src/test')
sys.path.insert(0, 'src/preprocess/')

import trainWord2Vec
import biastest
import preprocess
import random

np.random.seed(0)

corpusPath = 'news.2013.de.shuffled'
raw = 'data/raw/'+corpusPath
preprocessed = 'data/processed/'+corpusPath
modelPath = 'models/word2vec/'+corpusPath
resultPath = 'results/word2vec/robustnessToSlicing_'+corpusPath

size = 300
window = 5
minCount = 20
threads = 8
skipGram = 1
hierarchical = 1
negative = 20
cbowMean = 1
sample = 0.001



# Preprocess only if necessary
if not os.path.isfile(preprocessed):
	preprocess.chunkwisePreprocessing(raw, preprocessed, batchsize = 100000, workers = threads)

with open(preprocessed, 'r') as f:
	bigCorpus = [line.rstrip('\n').split() for line in f]

# Taken from
# http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
# Yield successive n-sized chunks from l.

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]

kf = range(len(bigCorpus)) 
np.random.shuffle(kf)
kf = chunks(kf, int(len(kf)/10) + 1)

for trainIndices in kf:
	corpus = [bigCorpus[i] for i in trainIndices]
	trainWord2Vec.trainGivenCorpus(corpus, modelPath, vectorDim = size, windowSize=window, mincount=minCount,  nWorkers=threads, skipgram=skipGram, hierarchicalSampling=hierarchical, negativeSampling=negative, cbowmean=cbowMean)

	biasTestResult = biastest.runBiastTests(modelPath)
	with open(resultPath, 'a') as outFile:
		outFile.write(str(biasTestResult))
		outFile.write('\n')
