# Test the robustness of bias tests by training models on different permutations of a corpus

import numpy as np
import os
import sys

sys.path.insert(0, 'src/train/word2vec')
sys.path.insert(0, 'src/test')
sys.path.insert(0, 'src/preprocess/')

import trainWord2Vec
import biastest
import preprocess

np.random.seed(0)

corpusPath = 'news.2013.de.shuffled'
raw = 'data/raw/'+corpusPath
preprocessed = 'data/processed/'+corpusPath
modelPath = 'models/word2vec/'+corpusPath
resultPath = 'results/word2vec/robustnessToPermutation_unequalLenghtsPandS_'+corpusPath

size = 300
window = 5
minCount = 20
threads = 42
skipGram = 1
hierarchical = 1
negative = 20
cbowMean = 1
sample = 0.001


## Realizing that shuffling the whole corpus takes very long in python, we preprocessed the whole corpus once,
# then create ten permutations of it on disk using the unix 'shuf' utility. Therefore the following paragraph became obsolete.

# Preprocess only if necessary
#if not os.path.isfile(preprocessed):
#	preprocess.chunkwisePreprocessing(raw, preprocessed, batchsize = 100000, workers = threads)


for i in xrange(10):

	# Train model only if we haven't written it to disk in previous runs
	modelPath = 'models/word2vec/'+corpusPath+"permu"+str(i)
	if not os.path.isfile(modelPath):
		with open(preprocessed + ".shuf" + str(i), 'r') as f:
                        corpus = [line.rstrip('\n').split() for line in f]

		# Save intermediate models in different paths in case we need to re-run these tests
		trainWord2Vec.trainGivenCorpus(corpus, modelPath, vectorDim = size, windowSize=window, mincount=minCount,  nWorkers=threads, skipgram=skipGram, hierarchicalSampling=hierarchical, negativeSampling=negative, cbowmean=cbowMean)

	else:
		print "Saved model found! Skipping training for "+modelPath

	biasTestResult = biastest.runBiasTests(modelPath)
	with open(resultPath, 'a') as outFile:
		outFile.write(str(biasTestResult))
		outFile.write('\n')
