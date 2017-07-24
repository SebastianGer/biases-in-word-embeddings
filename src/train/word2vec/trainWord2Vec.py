# Trains a word2vec model using the gensim library

import gensim 
import argparse
import zipfile
import getpass
import logging
import sys


# This one takes a corpus
def trainGivenCorpus(corpus, target, vectorDim = 100, windowSize=5, mincount=20,  nWorkers=4, skipgram=1, hierarchicalSampling=1, negativeSampling=0, cbowmean=0, downsample = 0.001, password = None):

	logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	model = gensim.models.Word2Vec(
	    corpus,
	    size=vectorDim,
	    window=windowSize,
	    min_count=mincount,
	    workers=nWorkers,
	    sg=skipgram,
	    hs=hierarchicalSampling,
	    negative=negativeSampling,
	    cbow_mean=cbowmean,
	    sample=downsample
	)

	model.wv.save_word2vec_format(target, binary=False)

# This one takes a path
def train(corpus, target, vectorDim = 100, windowSize=5, mincount=20,  nWorkers=4, skipgram=1, hierarchicalSampling=1, negativeSampling=0, cbowmean=0, downsample = 0.001, password = None):
	inFile = None

	if corpus.split('.')[-1] == 'zip':
		if password is None:
			password = getpass.getpass()
		inFile = zipfile.ZipFile(corpus)
		zippedFile = ".".join(corpus.split('/')[-1].split('.')[:-1])
		inFile = inFile.open(zippedFile, pwd = password)
	else:
		inFile = open(corpus, 'r')
	sentences = [line.rstrip('\n').split() for line in inFile]
	inFile.close()
	del inFile
	trainGivenCorpus(sentences, target, vectorDim, windowSize, mincount, nWorkers, skipgram, hierarchicalSampling, negativeSampling, cbowmean, downsample, password)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Script for training word2vec model')
	parser.add_argument('corpus', type=str, help='Corpus to train model on')
	parser.add_argument('target', type=str, help='target file name to store model in')
	parser.add_argument('-s', '--size', type=int, default=100, help='dimension of word vectors')
	parser.add_argument('-w', '--window', type=int, default=5, help='size of the sliding window')
	parser.add_argument('-m', '--mincount', type=int, default=20, help='minimum number of occurences of a word to be considered')
	parser.add_argument('-c', '--workers', type=int, default=4, help='number of worker threads to train the model')
	parser.add_argument('-g', '--sg', type=int, default=1, help='training algorithm: Skip-Gram (1), otherwise CBOW (0)')
	parser.add_argument('-i', '--hs', type=int, default=1, help='use of hierachical sampling for training')
	parser.add_argument('-n', '--negative', type=int, default=0, help='use of negative sampling for training (usually between 5-20)')
	parser.add_argument('-o', '--cbowmean', type=int, default=0, help='for CBOW training algorithm: use sum (0) or mean (1) to merge context vectors')
	parser.add_argument('-d', '--downsample', type=int, default=0.001, help='downsampling of frequent words')
	args = parser.parse_args()

	train(args.corpus, args.target, args.size, args.window, args.mincount, args.workers, args.sg, args.hs, args.negative, args.cbowmean)
