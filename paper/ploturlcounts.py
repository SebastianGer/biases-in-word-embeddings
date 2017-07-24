# -*- coding: utf-8 -*-
# Plots the distribution of sentences contributed per url and per domain.

import pandas as pd
import matplotlib
matplotlib.use('pgf')

import numpy as np

import matplotlib.pyplot as plt


from matplotlib import rcParams
rcParams['text.latex.unicode']=True

df = pd.read_csv("domaincounts", header = None)
df.columns = ["Domain", "Number of Sentences"]
df["Number of Sentences"] = pd.cut(df["Number of Sentences"],include_lowest=True, bins=[0, 1, 10, 10**2, 10**3, 10**4, 10**5, 10**6, 10**7], labels=[u'1', u'10', u'10\^{}2', u'10\^{}3', u'10\^{}4', u'10\^{}5', u'10\^{}6', u'10\^{}7'])
df.groupby('Number of Sentences').count().plot.bar(legend = None)

plt.ylabel("Number of Domains")
plt.title("Sentences contributed to the dataset per web domain")
plt.tight_layout()
plt.tick_params(axis='both', which='both', top='off', right='off')

plt.savefig("sentencesPerDomain.pdf")
plt.savefig("sentencesPerDomain.pgf")

plt.figure()


df = pd.read_csv("urlcounts", sep = '\t', header = None)
df.columns = ["URL", "Number of Sentences"]
df["Number of Sentences"] = pd.cut(df["Number of Sentences"],include_lowest=True, bins=[0, 1, 10, 10**2, 10**3], labels=[u'1', u'10', u'10\^{}2', u'10\^{}3'])

df.groupby('Number of Sentences').count().plot.bar(legend = None)

plt.ylabel("Number of Articles")
plt.title("Sentences contributed to the dataset per article")
plt.tight_layout()
plt.tick_params(axis='both', which='both', top='off', right='off')

locs,labels = plt.yticks()
plt.yticks(locs, map(lambda x: "0" if x == 0 else str(int(x/(10**int(np.log10(x)))))+"*10\^{}"+str(int(np.log10(x))), locs))

plt.savefig("sentencesPerUrl.pdf")
plt.savefig("sentencesPerUrl.pgf")
