# Runs the given WEFAT on the given corpus
# Change the filepaths to run the other WEFATs found at data/external/iats/wefat-*
import sys
sys.path.insert(0, 'src/test')
import biastest

corpusPath = 'deu_news_2011-2016'
modelPath = 'models/word2vec/'+corpusPath
resultPath = 'results/word2vec/'+corpusPath+"_wefatJobsWeiblSingular"

testPath = 'data/external/iats/wefat-frauenanteil-weiblich-singular.txt'

biasTestResult = biastest.runWefat(modelPath, testPath)
with open(resultPath, 'a') as outFile:
	outFile.write(str(biasTestResult))
	outFile.write('\n')
