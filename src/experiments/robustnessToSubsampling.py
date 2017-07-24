# Test the robustness of bias tests by training models on different slices and permutations of a corpus

import os
import sys
sys.path.insert(0, 'src/train/word2vec')
sys.path.insert(0, 'src/test')
sys.path.insert(0, 'src/preprocess/')

import numpy as np
import trainWord2Vec
import biastest
import preprocess
import random
import itertools

np.random.seed(0)

corpusPath = 'news.2013.de.shuffled'
raw = 'data/raw/'+corpusPath
preprocessed = 'data/processed/'+corpusPath
modelPath = 'models/word2vec/sub'+corpusPath
resultPath = 'results/word2vec/robustnessToSubsampling_unequalLengthsPandS_'+corpusPath

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
#
#with open(preprocessed, 'r') as f:
#	bigCorpus = [line.rstrip('\n').split() for line in f]


# Determine length of input corpus using the unix wc tool
# Taken from http://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python
# Used to find out how many lines the corpus actually has, so we can determine how much x% of that are. 
import subprocess
def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE, 
                                              stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])

nMax = file_len(preprocessed)

# For each sampling ratio subsample the corpus ten times, train a word2vec model on each of these and run bias tests on these models
for samplingRatio in [0.01, 0.05, 0.1, 0.5]:
	n = int(nMax*samplingRatio)
	for i in xrange(10):
		# Load pre-shuffled corpus from disk
		with open(preprocessed + ".shuf" + str(i), 'r') as f:
			corpus = [f.next().rstrip('\n').split() for j in xrange(n)]

		trainWord2Vec.trainGivenCorpus(corpus, modelPath, vectorDim = size, windowSize=window, mincount=minCount,  nWorkers=threads, skipgram=skipGram, hierarchicalSampling=hierarchical, negativeSampling=negative, cbowmean=cbowMean)

		biasTestResult = biastest.runBiasTests(modelPath)
		with open(resultPath, 'a') as outFile:
			outFile.write(",".join(map(str,map(lambda x: [samplingRatio] +x, biasTestResult))) + '\n')
