# Trains a word2vec model on our big Wortschatz corpus. This takes so long that it deservers its own file.

import os
import sys
sys.path.insert(0, 'src/train/word2vec')
sys.path.insert(0, 'src/preprocess/')

import trainWord2Vec
import preprocess
import gensim

corpusPath = 'deu_news_2011-2016'
raw = 'data/raw/'+corpusPath
preprocessed = 'data/processed/'+corpusPath
modelPath = 'models/word2vec/'+corpusPath

size = 300
window = 5
minCount = 20
threads = 32
skipGram = 1
hierarchical = 1
negative = 20
cbowMean = 1
sample = 0.001





# Preprocess only if necessary
if not os.path.isfile(preprocessed): 
	preprocess.chunkwisePreprocessing(raw, preprocessed, batchsize = 1000000, workers = threads)

trainWord2Vec.trainGivenCorpus(gensim.models.word2vec.LineSentence(preprocessed), modelPath, vectorDim = size, windowSize=window, mincount=minCount,  nWorkers=threads, skipgram=skipGram, hierarchicalSampling=hierarchical, negativeSampling=negative, cbowmean=cbowMean) 

