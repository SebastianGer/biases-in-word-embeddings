# Experiment to perform hyperparameter estimation via grid search

import gensim 
import sys
import time
import os
import itertools

sys.path.insert(0, 'src/train/glove')
import trainGloVe

sys.path.insert(0, 'src/preprocess/')
import preprocess

sys.path.insert(0, 'src/test/GermanWordEmbeddings/')
import evaluation

corpus = 'news.2013.de.shuffled'
raw = 'data/raw/'+corpus
preprocessed = 'data/processed/'+corpus
model = 'models/glove/'+corpus
result = 'results/glove/'+corpus

threads = 8

sizes = [100, 300, 500]
windows = [5, 10, 15]
xmax = 100
maxiter = 5
minCount = 20
memory = 16

# Preprocess corpus only if necessary
if not os.path.isfile(preprocessed): 
	preprocess.chunkwisePreprocessing(raw, preprocessed, batchsize = 100000, workers = threads)

for size in sizes:
	for window in windows:
		print "Starting GloVe preprocessing..."
		trainGloVe.preprocess(raw, model, window, minCount, memory, threads)
	
		for size in sizes:
			startTime = time.clock()
			print "Starting training..."
			trainGloVe.train(model, size, window, minCount, memory, threads, maxiter, xmax)
			print "Starting evaluation..."
			evalResult = evaluation.evaluateSingleResult(model, umlauts = True, topn = 5)

			endTime = time.clock() - startTime

			with open(result, 'a') as outFile:
				line = "size: "+str(size)+", window "+str(window)+", "+str(evalResult)+", "+str(endTime)
				outFile.write(line + '\n')
