#!/usr/bin/env python
# -*- coding: utf-8 -*-

# script to preprocess corpora for training
# 
# @author: Andreas Mueller
# @see: Bachelor Thesis 'Analyse von Wort-Vektoren deutscher Textkorpora'
# 
# @example: python preprocessing.py test.raw test.corpus -psub

# Assumption: -psu is always present as parameter

import gensim
import nltk.data
from nltk.corpus import stopwords
import argparse
import os
import re
import logging
import sys
from multiprocessing import Pool


# configuration
parser = argparse.ArgumentParser(description='Script for preprocessing public corpora')
parser.add_argument('raw', type=str, help='source file with raw data for corpus creation')
parser.add_argument('target', type=str, help='target file name to store corpus in')
parser.add_argument('-p', '--punctuation', action='store_true', help='remove punctuation tokens')
parser.add_argument('-s', '--stopwords', action='store_true', help='remove stop word tokens')
parser.add_argument('-u', '--umlauts', action='store_true', help='replace german umlauts with their respective digraphs')
parser.add_argument('-b', '--bigram', action='store_true', help='detect and process common bigram phrases')
args = parser.parse_args()
logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentence_detector = nltk.data.load('tokenizers/punkt/german.pickle')
punctuation_tokens = set(['.', '..', '...', ',', ';', ':', '(', ')', '"', '\'', '[', ']', '{', '}', '?', '!', '-', u'–', '+', '*', '--', '\'\'', '``'])
punctuation = '[?.!/;:()&+|%\']'


# function replace_umlauts
# ... replaces german umlauts and sharp s in given text
# @param string  text
# @return string with replaced umlauts
def replace_umlauts(text):
    res = text
    res = res.replace(u'ä', 'ae')
    res = res.replace(u'ö', 'oe')
    res = res.replace(u'ü', 'ue')
    res = res.replace(u'Ä', 'Ae')
    res = res.replace(u'Ö', 'Oe')
    res = res.replace(u'Ü', 'Ue')
    res = res.replace(u'ß', 'ss')
    return res

# get stopwords
#stop_words = stopwords.words('german') if not args.umlauts else [replace_umlauts(token.decode('utf-8')) for token in stopwords.words('german')]
stop_words = set(stopwords.words('german') if not args.umlauts else [replace_umlauts(token) for token in stopwords.words('german')])

# start preprocessing
num_sentences = sum(1 for line in open(args.raw))
# if not os.path.exists(os.path.dirname(args.target)):
    # os.makedirs(os.path.dirname(args.target))
output = open(args.target, 'w')
i = 1


# Process a single sentence
def processSentence(sentence):

       	sentence = replace_umlauts(sentence)
	words = nltk.word_tokenize(sentence)

	cleanWords = list()
	for word in words:
        	if word in punctuation_tokens:
			continue
	    	word = re.sub(punctuation, '', word)
		word = word.lower()
		word = re.sub('^\d+$', '', word)
        	if word in stop_words or word == '':
			continue
		else:
			cleanWords.append(word)
	return cleanWords

# Process a single line, sometimes containing multiple words
def processLine(line):
        # only take sentence, not info about source or date
        decLine = line.decode('utf-8').split('\t')[0]
        #sentences = sentence_detector.tokenize(decLine)
	#return map(processSentence, sentences)
	return processSentence(decLine)

pool = Pool(3)

logging.info('preprocessing ' + str(num_sentences) + ' sentences')
with open(args.raw, 'r') as infile:

    sentences = pool.map(processLine, infile)

    # write one sentence per line in output file, if sentence has more than 1 word
    for sentence in sentences:
   	if len(sentence)>1:
		#print sentence
		#print type(sentence)
                #output.write(sentence.encode('utf-8') + '\n')
		output.write(' '.join(sentence).encode('utf-8') + '\n')
        # logging.info('preprocessing sentence ' + str(i) + ' of ' + str(num_sentences))
        # i += 1

logging.info('preprocessing of ' + str(num_sentences) + ' sentences finished!')

# get corpus sentences
class CorpusSentences:
    def __init__(self, filename):
        self.filename = filename
    def __iter__(self):
        for line in open(self.filename):
            yield line.split()

if args.bigram:
    logging.info('train bigram phrase detector')
    bigram = gensim.models.Phrases(CorpusSentences(args.target))
    logging.info('transform corpus to bigram phrases')
    output = open(args.target + '.bigram', 'w')
    for tokens in bigram[CorpusSentences(args.target)]:
        output.write(' '.join(tokens).encode('utf8') + '\n')

