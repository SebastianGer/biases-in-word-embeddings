# Runs WEAT on the model trained on the big corpus. Test suite can be changed by adjusting the 'test' argument

import sys
sys.path.insert(0, 'src/test')
import biastest

#corpusPath = 'news.2007-2016.de.shuffled'
corpusPath = 'deu_news_2011-2016'
modelPath = 'models/word2vec/'+corpusPath
resultPath = 'results/word2vec/'+corpusPath+"_base"

biasTestResult = biastest.runBiasTests(modelPath, test = "base")
with open(resultPath, 'a') as outFile:
	outFile.write(str(biasTestResult))
	outFile.write('\n')
