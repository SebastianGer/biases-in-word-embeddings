# Tests how strongly male or female gendered job titles are associated with the gender they're representing.
# Using gender-to-gender.txt tests how strong explicitly male/female names are associated with their respective gender. 

import sys
sys.path.insert(0, 'src/test')
import biastest

corpusPath = 'deu_news_2011-2016'
modelPath = 'models/word2vec/'+corpusPath
resultPath = 'results/word2vec/'+corpusPath+"_averageGenderAssociationJobs"

testPath = 'data/external/iats/gendered-jobtitles-gender.txt'
#testPath = 'gender-to-gender.txt'

biasTestResult = biastest.averageAssociation(modelPath, testPath)
with open(resultPath, 'a') as outFile:
	outFile.write(str(biasTestResult))
	outFile.write('\n')
