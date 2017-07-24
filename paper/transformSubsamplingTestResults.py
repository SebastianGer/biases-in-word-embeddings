# Transforms the output of the robustness to subsampling experiments into nicer csv files.
# First argument of this script should be the name of the output of the bias test.

import pandas as pd
import re
import sys

filename = sys.argv[1]

with open(filename, 'r') as f:
	testResults = [eval(line) for line in f.read().splitlines()]


iteration = list()
samplingRate = list()
testName = list()
testStatistic = list()
pValue = list()
effectSize = list()
coverageX = list()
coverageY = list()
coverageA = list()
coverageB = list()
coverageXCount = list()
coverageYCount = list()
coverageACount = list()
coverageBCount = list()


testNameDict = {'flowers-insects':'Pleasantness/Flowers', 'career-family':'Gender/Career', 'german-asian':'Unpleasantness/Asian', 'german-turkish':'Unpleasantness/Turkish', 'christianity-islam':'Unpleasantness/Islam', 'natural-social-sciences':'Gender/Sciences', 'gendered-jobtitles-competence':'Gender/Competence'}

for i in range(len(testResults)):
	for res in testResults[i]:
		iteration.append(i)
		samplingRate.append(res[0])
		shortName = res[1].split('/')[-1].split('.txt')[0]
		testName.append(testNameDict[shortName])
		testStatistic.append(res[2])
		pValue.append(res[4])
		effectSize.append(res[3])
		coverageX.append(res[5][0])
		coverageY.append(res[5][1])
		coverageA.append(res[5][2])
		coverageB.append(res[5][3])
		coverageXCount.append(res[6][0])
		coverageYCount.append(res[6][1])
		coverageACount.append(res[6][2])
		coverageBCount.append(res[6][3])

df = pd.DataFrame({'Iteration':iteration, 'Sampling Rate':samplingRate, 'Test':testName, 'Value':testStatistic, 'p':pValue, 'Effect size':effectSize, 'CoverageX':coverageX, 'CoverageY':coverageY, 'CoverageA':coverageA, 'CoverageB':coverageB, 'CoverageXCount':coverageXCount, 'CoverageYCount':coverageYCount, 'CoverageACount':coverageACount, 'CoverageBCount':coverageBCount})
df.to_csv(filename+'_clean.csv', index = None)
