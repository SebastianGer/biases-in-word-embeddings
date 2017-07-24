# Plots results of preliminary experiments to determine parameter settings for all other experiments

import pandas as pd
import matplotlib
matplotlib.use('pgf')

import matplotlib.pyplot as plt

df = pd.read_csv("data/preliminaryWord2vecComplete_clean.csv")

df3 = df.query('(skipgram == 1) & (contextwindow == 3)')
df5 = df.query('(skipgram == 1) & (contextwindow == 5)')
df7 = df.query('(skipgram == 1) & (contextwindow == 7)')
df10 = df.query('(skipgram == 1) & (contextwindow == 10)')
df15 = df.query('(skipgram == 1) & (contextwindow == 15)')

plt.plot(df3.dimension, df3.accuracy, 'o', label = "context window = 3")
plt.plot(df5.dimension, df5.accuracy, 'o', label = "context window = 5")
plt.plot(df7.dimension, df7.accuracy, 'o', label = "context window = 7")
plt.plot(df10.dimension, df10.accuracy, 'o', label = "context window = 10")
plt.plot(df15.dimension, df15.accuracy, 'o', label = "context window = 15")
plt.xlabel("vector dimension")
plt.ylabel("accuracy")
plt.xlim(90,510)
plt.ylim(40,60)
plt.legend(loc = "lower right")
plt.title("Parameter estimation for Skip-Gram model")
plt.tick_params(axis='both', which='both', top='off', right='off')

plt.savefig("plots/word2vecSkipgramPreliminary.pgf")
plt.savefig("plots/word2vecSkipgramPreliminary.pdf")

df3 = df.query('(skipgram == 0) & (contextwindow == 3)')
df5 = df.query('(skipgram == 0) & (contextwindow == 5)')
df7 = df.query('(skipgram == 0) & (contextwindow == 7)')
df10 = df.query('(skipgram == 0) & (contextwindow == 10)')
df15 = df.query('(skipgram == 0) & (contextwindow == 15)')

plt.clf()
plt.plot(df3.dimension, df3.accuracy, 'o', label = "context window = 3")
plt.plot(df5.dimension, df5.accuracy, 'o', label = "context window = 5")
plt.plot(df7.dimension, df7.accuracy, 'o', label = "context window = 7")
plt.plot(df10.dimension, df10.accuracy, 'o', label = "context window = 10")
plt.plot(df15.dimension, df15.accuracy, 'o', label = "context window = 15")
plt.xlabel("vector dimension")
plt.ylabel("accuracy")
plt.xlim(90,510)
plt.ylim(40,60)
#plt.legend(loc = "lower right")
plt.title("Parameter estimation for CBOW model")
plt.tick_params(axis='both', which='both', top='off', right='off')

plt.savefig("plots/word2vecCBOWPreliminary.pgf")
plt.savefig("plots/word2vecCBOWPreliminary.pdf")

df = pd.read_csv("data/preliminaryGloVeResults_clean.csv")

df5 = df.query('contextwindow == 5')
df10 = df.query('contextwindow == 10')
df15 = df.query('contextwindow == 15')

plt.clf()
plt.plot(df5.dimension, df5.accuracy, 'o', label = "context window = 5")
plt.plot(df10.dimension, df10.accuracy, 'o', label = "context window = 10")
plt.plot(df15.dimension, df15.accuracy, 'o', label = "context window = 15")
plt.xlabel("vector dimension")
plt.ylabel("accuracy")
#plt.ylim(45,55)
plt.legend(loc = "lower right")
plt.title("Parameter estimation for GloVe model")
plt.tick_params(axis='both', which='both', top='off', right='off')

plt.savefig("plots/gloVePreliminary.pgf")
plt.savefig("plots/gloVePreliminary.pdf")

