# Plots the results of the experiments investigating the robustness of the WEAT to permutation and subsampling

import pandas as pd
import matplotlib
matplotlib.use('pgf')

import matplotlib.pyplot as plt


df = pd.read_csv("data/robustnessToPermutation.csv")
plotDf = df.pivot(index = "Iteration", columns = 'Test', values = 'p')

fig = plt.figure()
plotDf.boxplot(rot=45)
plt.tight_layout() # makes sure that long x labels are not cut off
plt.gcf().subplots_adjust(left=0.15)

plt.ylim((-0.1,1.1))
plt.ylabel("p")
plt.legend()
plt.title("Robustness of bias tests under permutation")
plt.tick_params(axis='both', which='both', top='off', right='off')

fig.savefig("plots/robustnessToPermutationP.pgf")
fig.savefig("plots/robustnessToPermutationP.pdf")

plt.clf()
df = pd.read_csv("data/robustnessToPermutation.csv")
plotDf = df.pivot(index = "Iteration", columns = 'Test', values = 'Effect size')

fig = plt.figure()
plotDf.boxplot(rot=45)
plt.tight_layout() # makes sure that long x labels are not cut off
plt.gcf().subplots_adjust(left=0.15)

plt.ylim((-2,2))
plt.ylabel("Effect size")
plt.legend()#loc = "lower right")
plt.title("Robustness of bias tests under permutation")
plt.tick_params(axis='both', which='both', top='off', right='off')

fig.savefig("plots/robustnessToPermutationD.pgf")
fig.savefig("plots/robustnessToPermutationD.pdf")




plt.clf()
df = pd.read_csv("data/robustnessToSubsampling.csv")
df = df[df['Sampling Rate'] == 0.01]

# Replace NA string with NaN value
df = df.apply(lambda s: map(lambda x : float('NaN') if x=="'NA'" else x, s), axis = 1)
plotDf = df.pivot(index = "Iteration", columns = 'Test', values = 'p')

fig = plt.figure()
plotDf.boxplot(rot=45)
plt.tight_layout() # makes sure that long x labels are not cut off
plt.gcf().subplots_adjust(left=0.15)

plt.ylim((-0.1,1.1))
plt.ylabel("p")
plt.legend()
plt.title("Robustness of biast tests under subsampling: sampling rate 0.01")
plt.tick_params(axis='both', which='both', top='off', right='off')

fig.savefig("plots/robustnessToSubsampling0.01P.pgf")
fig.savefig("plots/robustnessToSubsampling0.01P.pdf")


plotDf = df.pivot(index = "Iteration", columns = 'Test', values = 'Effect size')

fig = plt.figure()
plotDf.boxplot(rot=45)
plt.tight_layout() # makes sure that long x labels are not cut off
plt.gcf().subplots_adjust(left=0.15)

plt.ylim((-2,2))
plt.ylabel("Effect size")
plt.legend()
plt.title("Robustness of biast tests under subsampling: sampling rate 0.01")
plt.tick_params(axis='both', which='both', top='off', right='off')

fig.savefig("plots/robustnessToSubsampling0.01D.pgf")
fig.savefig("plots/robustnessToSubsampling0.01D.pdf")






plt.clf()
df = pd.read_csv("data/robustnessToSubsampling.csv")
df = df[df['Sampling Rate'] == 0.05]

# Replace NA string with NaN value
df = df.apply(lambda s: map(lambda x : float('NaN') if x=="'NA'" else x, s), axis = 1)
plotDf = df.pivot(index = "Iteration", columns = 'Test', values = 'p')


fig = plt.figure()
plotDf.boxplot(rot=45)
plt.tight_layout() # makes sure that long x labels are not cut off
plt.gcf().subplots_adjust(left=0.15)

plt.ylim((-0.1,1.1))
plt.ylabel("p")
plt.legend()
plt.title("Robustness of biast tests under subsampling: sampling rate 0.05")
plt.tick_params(axis='both', which='both', top='off', right='off')

fig.savefig("plots/robustnessToSubsampling0.05P.pgf")
fig.savefig("plots/robustnessToSubsampling0.05P.pdf")


plotDf = df.pivot(index = "Iteration", columns = 'Test', values = 'Effect size')

fig = plt.figure()
plotDf.boxplot(rot=45)
plt.tight_layout() # makes sure that long x labels are not cut off
plt.gcf().subplots_adjust(left=0.15)

plt.ylim((-2,2.0))
plt.ylabel("Effect size")
plt.legend()
plt.title("Robustness of biast tests under subsampling: sampling rate 0.05")
plt.tick_params(axis='both', which='both', top='off', right='off')

fig.savefig("plots/robustnessToSubsampling0.05D.pgf")
fig.savefig("plots/robustnessToSubsampling0.05D.pdf")





plt.clf()
df = pd.read_csv("data/robustnessToSubsampling.csv")
df = df[df['Sampling Rate'] == 0.1]

# Replace NA string with NaN value
df = df.apply(lambda s: map(lambda x : float('NaN') if x=="'NA'" else x, s), axis = 1)
plotDf = df.pivot(index = "Iteration", columns = 'Test', values = 'p')

fig = plt.figure()
plotDf.boxplot(rot=45)
plt.tight_layout() # makes sure that long x labels are not cut off
plt.gcf().subplots_adjust(left=0.15)

plt.ylim((-0.1,1.1))
plt.ylabel("p")
plt.legend()
plt.title("Robustness of biast tests under subsampling: sampling rate 0.1")
plt.tick_params(axis='both', which='both', top='off', right='off')

fig.savefig("plots/robustnessToSubsampling0.1P.pgf")
fig.savefig("plots/robustnessToSubsampling0.1P.pdf")


plotDf = df.pivot(index = "Iteration", columns = 'Test', values = 'Effect size')

fig = plt.figure()
plotDf.boxplot(rot=45)
plt.tight_layout() # makes sure that long x labels are not cut off
plt.gcf().subplots_adjust(left=0.15)

plt.ylim((-2,2.0))
plt.ylabel("Effect size")
plt.legend()
plt.title("Robustness of biast tests under subsampling: sampling rate 0.1")
plt.tick_params(axis='both', which='both', top='off', right='off')

fig.savefig("plots/robustnessToSubsampling0.1D.pgf")
fig.savefig("plots/robustnessToSubsampling0.1D.pdf")



plt.clf()
df = pd.read_csv("data/robustnessToSubsampling.csv")
df = df[df['Sampling Rate'] == 0.5]

# Replace NA string with NaN value
df = df.apply(lambda s: map(lambda x : float('NaN') if x=="'NA'" else x, s), axis = 1)
plotDf = df.pivot(index = "Iteration", columns = 'Test', values = 'p')

fig = plt.figure()
plotDf.boxplot(rot=45)
plt.tight_layout() # makes sure that long x labels are not cut off
plt.gcf().subplots_adjust(left=0.15)

plt.ylim((-0.1,1.1))
plt.ylabel("p")
plt.legend()
plt.title("Robustness of biast tests under subsampling: sampling rate 0.5")
plt.tick_params(axis='both', which='both', top='off', right='off')

fig.savefig("plots/robustnessToSubsampling0.5P.pgf")
fig.savefig("plots/robustnessToSubsampling0.5P.pdf")



plotDf = df.pivot(index = "Iteration", columns = 'Test', values = 'Effect size')

fig = plt.figure()
plotDf.boxplot(rot=45)
plt.tight_layout() # makes sure that long x labels are not cut off
plt.gcf().subplots_adjust(left=0.15)

plt.ylim((-2,2.0))
plt.ylabel("Effect size")
plt.legend()
plt.title("Robustness of biast tests under subsampling: sampling rate 0.5")
plt.tick_params(axis='both', which='both', top='off', right='off')

fig.savefig("plots/robustnessToSubsampling0.5D.pgf")
fig.savefig("plots/robustnessToSubsampling0.5D.pdf")

