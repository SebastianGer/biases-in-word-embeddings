# Performs GloVe-specific preprocessing and then computes the GloVe model.
# The executable training- and preprocessing code is the original code published by the GloVe authors.

import gensim 
import argparse
import os
from subprocess import call
from gensim.scripts.glove2word2vec import glove2word2vec

def preprocess(corpus, target, window, mincount, memory, threads):
	call([glovePath + "build/vocab_count", "-min-count",  str(mincount), "-verbose 2"], stdin = open(corpus, 'r'), stdout = open(VOCAB_FILE, 'w'))
	call([glovePath + "build/cooccur", "-memory", str(memory), "-vocab-file", VOCAB_FILE, "-verbose 2", "-window-size", str(window)], stdin = open(corpus, 'r'),  stdout = open(COOCCURRENCE_FILE, 'w'))
	call([glovePath + "build/shuffle", "-memory", str(memory), "-verbose 2"], stdin = open(COOCCURRENCE_FILE, 'r'), stdout = open(COOCCURRENCE_SHUF_FILE, 'w'))

def train(target, size, window, mincount, memory, threads, maxiter, xmax):
	call([glovePath + "build/glove", "-save-file",  target , "-threads", str(threads), "-input-file", COOCCURRENCE_SHUF_FILE, "-x-max", str(xmax), "-iter", str(maxiter), "-vector-size", str(size), "-binary", "0", "-vocab-file", VOCAB_FILE, "-verbose 2", "-model", "2"])
	# Convert format and remove intermediary file
	glove2word2vec(target+".txt", target)
	call(["rm", target+".txt"])

glovePath = os.path.dirname(os.path.abspath(__file__)) + '/'

VOCAB_FILE=glovePath + "vocab.txt"
COOCCURRENCE_FILE=glovePath + "cooccurrence.bin"
COOCCURRENCE_SHUF_FILE=glovePath + "cooccurrence.shuf.bin"

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Script for training word2vec model')
	parser.add_argument('corpus', type=str, help='Corpus to train model on')
	parser.add_argument('target', type=str, help='target file name to store model in')
	parser.add_argument('-s', '--size', type=int, default=100, help='dimension of word vectors')
	parser.add_argument('-w', '--window', type=int, default=5, help='size of the sliding window')
	parser.add_argument('-m', '--mincount', type=int, default=20, help='minimum number of occurences of a word to be considered')
	parser.add_argument('-r', '--memory', type=int, default=4, help='memory... probably max memory to be allocated')
	parser.add_argument('-t', '--threads', type=int, default=4, help='number of worker threads to train the model')
	parser.add_argument('-i', '--maxiter', type=int, default=15, help='maximum iterations')
	parser.add_argument('-x', '--xmax', type=int, default=10, help='xmax, some kind of hyper parameter')
	args = parser.parse_args()

	preprocess(args.corpus, args.target, args.window, args.mincount, args.memory, args.threads)
	train(args.target, args.size, args.window, args.mincount, args.memory, args.threads, args.maxiter, args.xmax)



