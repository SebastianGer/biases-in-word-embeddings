# Experiment to perform hyperparameter estimation by Bayesian Optimization using MOE

import gensim 
import sys
import time
import getpass
import zipfile
import os
import itertools

sys.path.insert(0, 'src/train/word2vec')
import trainWord2Vec

sys.path.insert(0, 'src/preprocess/')
import preprocess

sys.path.insert(0, 'src/test/GermanWordEmbeddings/')
import evaluation

corpus = 'news.2013.de.shuffled'
raw = 'data/raw/'+corpus
preprocessed = 'data/processed/'+corpus
model = 'models/word2vec/'+corpus
result = 'results/word2vec/'+corpus

threads = 8

sizes = [100, 200, 300, 400, 500]
windows = [3, 5, 7, 10, 15]

minCount = 20
workers = threads
skipGrams = [0, 1]
hierarchical = 1
negative = 20
cbowMean = 1
sample = 0.001

# Preprocess corpus only if necessary
if not os.path.isfile(preprocessed): 
	preprocess.chunkwisePreprocessing(raw, preprocessed, batchsize = 100000, workers = threads, password = pw)

for (skipGram, size, window) in itertools.product(skipGrams, sizes, windows):
	startTime = time.clock()
	parameters = [size, window, minCount, workers, skipGram, hierarchical, negative, cbowMean]
	print "Starting training..."
	trainWord2Vec.train(preprocessed, model, vectorDim = size, windowSize=window, mincount=minCount,  nWorkers=workers, skipgram=skipGram, hierarchicalSampling=hierarchical, negativeSampling=negative, cbowmean=cbowMean, password = pw)
	print "Starting evaluation..."
	evalResult = evaluation.evaluateSingleResult(model, umlauts = True, topn = 5)

	endTime = time.clock() - startTime

	with open(result, 'a') as outFile:
		line = "skipGram "+str(skipGram)+", size: "+str(size)+", window "+str(window)+", "+str(evalResult)+", "+str(endTime)
		outFile.write(line + '\n')
