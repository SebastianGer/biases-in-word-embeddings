# Replicate Caliskan et al.'s experiments to verify our implementation

import os
import sys
sys.path.insert(0, 'src/train/word2vec')
sys.path.insert(0, 'src/test')
sys.path.insert(0, 'src/preprocess/')

import trainWord2Vec
import biastest
import preprocess
import random

#modelPath = 'models/word2vec/GoogleNews-vectors-negative300.bin'
modelPath = 'models/glove/glove.840B.300d.w2v.format'
resultPath = 'results/glove/caliskanReproduction'

# Run english tests
biasTestResult = biastest.runBiastTests(modelPath, en=True)
with open(resultPath, 'a') as outFile:
	outFile.write(str(biasTestResult))
	outFile.write('\n')
