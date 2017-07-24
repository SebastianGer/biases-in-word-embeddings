# Plot variance ratio explained by PCA, used to determine if there is a clear gender subspace
import pandas as pd
import matplotlib
matplotlib.use('pgf')

import matplotlib.pyplot as plt

with open("data/pcaExplainedVarianceExtendedPlus", "r") as f:
	fileContent = f.read()

# Remove leading text
fileContent = fileContent.split()[3:]
# Remove trailing brace
fileContent[-1] = fileContent[-1][:-1]

explainedVariancePercentage = pd.Series(map(float, fileContent[:10]))
explainedVariancePercentage.plot(kind="bar")

plt.xlabel("Principal components")
plt.ylabel("Explained percentage of variance")
plt.xticks([])
plt.ylim((0,0.4))
plt.title("Top 10 PCA result for 132 gendered word pairs")
plt.tick_params(axis='both', which='both', top='off', right='off')

plt.savefig("plots/pca132.pgf")
plt.savefig("plots/pca132.pdf")


plt.clf()
with open("data/pcaExplainedVarianceJobs", "r") as f:
        fileContent = f.read()

# Remove leading text
fileContent = fileContent.split()[3:]
# Remove trailing brace
fileContent[-1] = fileContent[-1][:-1]

explainedVariancePercentage = pd.Series(map(float, fileContent[:10]))
explainedVariancePercentage.plot(kind="bar")

plt.xlabel("Principal components")
plt.ylabel("Explained percentage of variance")
plt.xticks([])
plt.ylim((0,0.4))
plt.title("Top 10 PCA result for 13 gendered occupation word pairs")
plt.tick_params(axis='both', which='both', top='off', right='off')

plt.savefig("plots/pcaJobs.pgf")
plt.savefig("plots/pcaJobs.pdf")



plt.clf()
with open("data/pcaExplainedVariance", "r") as f:
        fileContent = f.read()

# Remove leading text
fileContent = fileContent.split()[3:]
# Remove trailing brace
fileContent[-1] = fileContent[-1][:-1]

explainedVariancePercentage = pd.Series(map(float, fileContent[:10]))
explainedVariancePercentage.plot(kind="bar")

plt.xlabel("Principal components")
plt.ylabel("Explained percentage of variance")
plt.xticks([])
plt.ylim((0,0.4))
plt.title("Top 10 PCA result for 10 stereotypical gendered word pairs")
plt.tick_params(axis='both', which='both', top='off', right='off')

plt.savefig("plots/pca10.pgf")
plt.savefig("plots/pca10.pdf")
