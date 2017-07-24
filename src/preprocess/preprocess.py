#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Script to preprocess corpora and write the result back to disk
# Assumption: All input files consist of exactly one sentence per line, seperated by \n

import nltk.data
#from nltk.corpus import stopwords
from multiprocessing import Pool
import re
import argparse
import zipfile
import getpass
import logging
import sys

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Taken from GermanWordEmbeddings(https://github.com/devmount/GermanWordEmbeddings)
#
# function replaceUmlauts
# ... replaces german umlauts and sharp s in given text
# @param string  text
# @return string with replaced umlauts
def replaceUmlauts(text):
    res = text
    res = res.replace(u'ä', 'ae')
    res = res.replace(u'ö', 'oe')
    res = res.replace(u'ü', 'ue')
    res = res.replace(u'Ä', 'Ae')
    res = res.replace(u'Ö', 'Oe')
    res = res.replace(u'Ü', 'Ue')
    res = res.replace(u'ß', 'ss')
    return res

# Process a single sentence, removing stop words, punctuation, only-digits words
def processSentence(sentence):

       	sentence = replaceUmlauts(sentence)
	words = nltk.word_tokenize(sentence)

	cleanWords = list()
	for word in words:
        	if word in punctuationTokens:
			continue
		word = word.lower()
		word = re.sub('[^a-z0-9]', '', word)
		word = re.sub('^\d+$', '', word)
		if word == '':
			continue
        	#if word in stopWords or word == '':
		#	continue
		else:
			cleanWords.append(word)
	return cleanWords


# Decode line, then preprocess the resulting sentence
def processNonTsvLine(line):

        decLine = line.decode('utf-8')
	return processSentence(decLine)


# Throw away additional information from tsv file, then preprocess the sentence
def processTsvLine(line):

        # Only take sentence, discard info about source or date
        decLine = line.decode('utf-8').split('\t')[0]
	return processSentence(decLine)


# Load and preprocess sentences from a file containing a single sentence per line
def preprocessSentencesFromFile(filename):

	pool = Pool(args.workers)
	with open(filename, 'r') as infile:
		sentences = pool.map(processNonTsvLine, infile)
		pool.close()
		return sentences


# Load only sentence data from tsv file and preprocess the sentences
def preprocessSentencesFromTsv(filename):

	pool = Pool(args.workers)
	with open(filename, 'r') as infile:
		sentences = pool.map(processTsvLine, infile)
		pool.close()
		return sentences

		
# Write one sentence per line into output file, if sentence has more than 1 word
def writeSentences(sentences, filename):

	with open(filename, 'w') as f:
		for sentence in sentences:
			if len(sentence)>1:
				f.write(' '.join(sentence).encode('utf-8') + '\n')


# Alternative with chunkwise reading and writing, doesn't need to keep everything in memory at once
def chunkwisePreprocessing(source, target, batchsize, workers, password = None):
	
	inFile =  open(source, 'r')
	with open(target, 'w') as outFile:
		pool = Pool(workers)

		eof = False
		while not eof:
			sentences = []
			print "Starting preprocessing of new batch.."
			for i in range(batchsize):
				line = inFile.readline().decode('utf-8')
				if line == '':
					eof = True
					break
				sentences.append(line.rstrip('\n'))
			sentences = pool.map(processSentence, sentences)
			for sentence in sentences:
				if len(sentence)>1:
					outFile.write(' '.join(sentence).encode('utf-8') + '\n')


	inFile.close()


punctuationTokens = set(['.', '..', '...', ',', ';', ':', '(', ')', '"', '\'', '[', ']', '{', '}', '?', '!', '-', u'–', '+', '*', '--', '\'\'', '``'])
punctuation = '[?.,!/;:()&+|%\']'
#stopWords = set([replaceUmlauts(token) for token in stopwords.words('german')])

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Script for preprocessing corpora')
	parser.add_argument('source', type=str, help='source corpus (one sentence plain text per line)')
	parser.add_argument('target', type=str, help='target file name to save preprocessed corpus in')
	parser.add_argument('-b', '--batchsize', type=int, default = 100000, help = 'number of lines to read and distribute to worker threads at once')
	parser.add_argument('-w', '--workers', type=int, default=3, help='number of worker threads to use while preprocessing')
	parser.add_argument('-t', '--tsv', action='store_true', help='indicates whether the file is in tsv format or not')
	#parser.add_argument('-b', '--bzip', action='store_true', help='indicates whether the file is in bzip format or not')
	args = parser.parse_args()

	sentences = []

	# Before chunkwise IO was implemented, this was used
	#if args.tsv:
	#	sentences = preprocessSentencesFromTsv(args.source)
	#else:
	#	sentences = preprocessSentencesFromFile(args.source)
	#
	#writeSentences(sentences, args.target)

	chunkwisePreprocessing(args.source, args.target, args.batchsize, args.workers)
