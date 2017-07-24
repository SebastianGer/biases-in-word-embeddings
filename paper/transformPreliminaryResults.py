# Transforms the output of the test performed during preliminary tests into nicer csv files.
# First argument of this script should be the name of the output of the bias test.

import pandas as pd
import re
import sys

filename = sys.argv[1]

df = pd.read_csv(filename+'.csv', header = None, names = ["skipgram", "dimension", "contextwindow", "accuracy", "topnaccuracy", "time"])
df = df.drop(['time','topnaccuracy'], axis = 1)

f = lambda s : re.sub('[^0-9\.]', '', s) if type(s)==str else s
for c in df.columns:
	df[c] = df[c].map(f)

df.to_csv(filename+'_clean.csv', index = None)
