# Tests how strongly male or female gendered job titles are associated with the gender they're representing.
# Using gender-to-gender.txt tests how strong explicitly male/female names are associated with their respective gender. 

import sys
sys.path.insert(0, 'src/test')
import biastest

#corpusPath = 'deu_news_2011-2016'
corpusPath = 'GoogleNews-vectors-negative300.bin'
modelPath = 'models/word2vec/'+corpusPath
resultPath = 'results/word2vec/'+corpusPath+"_averageGenderAssociationEn"

testPath = 'data/external/iats/gender-to-gender-en.txt'
#testPath = 'gender-to-gender.txt'

biasTestResult = biastest.averageAssociation(modelPath, testPath, binary = True)
with open(resultPath, 'a') as outFile:
	outFile.write(str(biasTestResult))
	outFile.write('\n')
