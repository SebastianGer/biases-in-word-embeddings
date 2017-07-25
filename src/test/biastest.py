# Runs the WEAT and WEFAT tests introduced by Caliskan et al. 

from gensim.models import KeyedVectors
import numpy as np
import itertools
from scipy.stats import linregress
import logging
import sys

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

np.random.seed(0)

# Number of iterations to approximate p-values
# Change to 10**9 for final experiments
maxIter = 10**6

deBasePath = 'data/external/iats/de/'
iatFilesDe = ['flowers-insects.txt', 'career-family.txt', 'german-asian.txt', 'german-turkish.txt', 'christianity-islam.txt', 'gendered-jobtitles-competence.txt', 'natural-social-sciences.txt']
iatFilesDe = map(lambda x: deBasePath+x, iatFilesDe)

enBasePath = 'data/external/iats/en/'
iatFilesEn = ['career-family', 'european-african', 'european-african2', 'european-african3', 'flowers-insects', 'instruments-weapons', 'math-art', 'science-art']
iatFilesEn = map(lambda x: enBasePath+x, iatFilesEn)

parBasePath = 'data/external/iats/parallel/'
iatFilesPar = ['age','career-family', 'instruments-weapons', 'mental-illness', 'flowers-insects', 'math-arts', 'science-arts']
iatFilesPar = map(lambda x: parBasePath+x, iatFilesPar)


similarityDict = dict()
sDict = dict()

# standard: 4m41.221s, 4m45.833s
def sNormal(model, w, A, B):
	ASim = [model.similarity(w, a) for a in A]
	BSim = [model.similarity(w, b) for b in B]
	ASim = sum(ASim) / len(ASim)
	BSim = sum(BSim) / len(BSim)
	return ASim - BSim

def normalize(x):
	return x / np.sqrt(np.dot(x,x))

# Use dictionary lookup for similarity between vectors
# Only computes dot product if we haven't computed it before to improve performance
def cosineSimilarity(w,a):
	vecTuple = (tuple(w),tuple(a))
	if not vecTuple in similarityDict:
		similarityDict[vecTuple] = np.dot(w,a)
	return similarityDict[vecTuple]

def sLookup(model, x, A, B):
	vecTuple = tuple(x)
	if not vecTuple in sDict:
                sDict[vecTuple] = s(model, x, A, B)
        return sDict[vecTuple]

def s(model, w, A, B):
	wVec = normalize(model[w])
	ASim = [cosineSimilarity(wVec, normalize(model[a])) for a in A]
	BSim = [cosineSimilarity(wVec, normalize(model[a])) for a in B]
	ASim = sum(ASim) / len(ASim)
	BSim = sum(BSim) / len(BSim)
	#ASim = np.mean(ASim)
	#BSim = np.mean(BSim)
	return ASim - BSim


def testStatistic(model, X, Y, A, B):
	Xs = sum([sLookup(model, x, A, B) for x in X])/float(len(X))
	Ys = sum([sLookup(model, y, A, B) for y in Y])/float(len(Y))
	return Xs - Ys

def effectSize(model, X, Y, A, B):
	Xs = [s(model, x, A, B) for x in X]
        Ys = [s(model, y, A, B) for y in Y]
	XYs = Xs + Ys
	#XYs = [s(model, x, A, B) for x in X+Y]
	Xs = sum(Xs) / len(Xs)
        Ys = sum(Ys) / len(Ys)
	#Xs = np.mean(Xs)
	#Ys = np.mean(Ys)
	return (Xs - Ys) / np.std(XYs, ddof=1)


# Approximates the p value by sampling maxIter partitions (Xi, Yi)
# Modification to original approach: |Xi| == |X| and |Yi| == |Y| instead of |Xi| == |Yi|
def pValue(model, X, Y, A, B, sValue):
        Z = X + Y
        ZSet = set(Z)
        n = len(ZSet)
        countBiggerStats = 0

        for i in xrange(maxIter):
                if i%(10**4) == 0:
                        print "Starting p-value computation "+str(i)+" / "+str(maxIter)
                np.random.shuffle(Z)
                Xi = Z[:len(X)]
                Yi = Z[len(X):]
                testStat = testStatistic(model, Xi, Yi, A, B)
                if testStat > sValue:
                        countBiggerStats += 1
        return float(countBiggerStats) / float(maxIter)



def wefatScore(model, w, A, B):
        ASim = [model.similarity(w, a) for a in A]
        BSim = [model.similarity(w, b) for b in B]
	ABSim = ASim + BSim
        ASim = sum(ASim) / len(ASim)
        BSim = sum(BSim) / len(BSim)
        return float((ASim - BSim)) / float(np.std(ABSim))


# return average s value of X and Y
def averageAssociation(modelPath, testPath, binary = False):
        model = KeyedVectors.load_word2vec_format(modelPath, binary = binary)
        with open(testPath, 'r') as f:
                IAT = f.read().splitlines()
        X = IAT[0].split(' ')
        Y = IAT[1].split(' ')
        A = IAT[2].split(' ')
        B = IAT[3].split(' ')

	mX = [s(model, w, A, B) for w in X if w in model]
        mY = [s(model, w, A, B) for w in Y if w in model]
	print mX
	print mY
	print "Coverage X: ", len(mX)/float(len(X))
        print "Coverage Y: ", len(mY)/float(len(Y))
	return [np.mean(mX), np.mean(mY), mX, mY]



# runs Caliskan et al.'s WEFAT test, props is a list with one property associated with each x in X
def runWefat(modelPath, testPath):
	model = KeyedVectors.load_word2vec_format(modelPath)
	with open(testPath, 'r') as f:
		IAT = f.read().splitlines()
	X = IAT[0].split(' ')
        props = IAT[1].split(' ')
	props = map(float, props)
        A = IAT[2].split(' ')
        B = IAT[3].split(' ')

	scores = [(wefatScore(model, x, A, B),y) for (x,y) in zip(X,props) if x in model]
	scores, props = zip(*scores)
	slope, intercept, r_value, p_value, std_err = linregress(scores, props)
	return r_value, p_value

# Run bias tests after loading the model from the provided filepath
def runBiasTests(modelPath, test = "base"):
        model = KeyedVectors.load_word2vec_format(modelPath)
	return runBiasTestsGivenModel(model, test)

# Run bias tests on the given model
# 'test' chooses which tests to run.
# "en": English tests used in the original paper by Caliskan et al.
# "par": German tests equivalent to the tests used by Caliskan et al. for parallel comparison with those and with original psychological studies
# "base" or other: our own tests as outlined in the paper. partially translated, partially taken from psychological studies, partially original
def runBiasTestsGivenModel(model, test = "base"):

	vocab = set(model.index2word)
	output = list()

	if test == "en":
		iatList = iatFilesEn
	elif test == "par":
		iatList = iatFilesPar
	else:
		iatList = iatFilesDe

	for fileName in iatList:

		sDict = dict()

		with open(fileName, 'r') as f:
			IAT = f.read().splitlines()
		X = IAT[0].split(' ')
		Y = IAT[1].split(' ')
                A = IAT[2].split(' ')
                B = IAT[3].split(' ')

		# account for words not being in the vocabulary
		n0 = map(float,[len(X), len(Y), len(A), len(B)])
		X = [x for x in X if x in vocab]
		Y = [x for x in Y if x in vocab]
		A = [x for x in A if x in vocab]
		B = [x for x in B if x in vocab]
		n1 = map(float,[len(X), len(Y), len(A), len(B)])
		coverage = [n1[0]/n0[0], n1[1]/n0[1], n1[2]/n0[2], n1[3]/n0[3]]

		# If one of the word sets is completely empty, running the tests is not possible
		if (n1[0] == 0 or n1[1] == 0 or n1[2] == 0 or n1[3] == 0):
			stat = float("NaN")
			effect = float("NaN")
			p = float("NaN")
		else:
			print "starting testing for "+fileName+ " with coverage "+str(coverage)
			stat = testStatistic(model, X, Y, A, B)
			effect = effectSize(model, X, Y, A, B)
			p = pValue(model, X, Y, A, B, stat)
		print fileName, str(stat), str(effect), str(p), str(coverage), str(n1)
		output.append([fileName, stat, effect, p, coverage, n1])
	return output

