# Plot average gender association of gendered job titles, and explicitly gender-specific names

import matplotlib
matplotlib.use('pgf')
import matplotlib.pyplot as plt

with open("data/deu_news_2011-2016_averageGenderAssociationJobs") as f:
	results = eval(f.read())

fig = plt.figure()

m = results[2]
f = results[3]
f = map(lambda x: -x, results[3])

m.sort()
f.sort()

plt.plot(m, "bo", label = "Male occupation terms")
plt.plot(f, "ro", label = "Female occupation terms")

plt.tick_params(axis='both', which='both', top='off', right='off', bottom='off')
plt.xticks([])

plt.xlabel("Terms ordered by their association value")
plt.ylabel("Association with respective gender")

plt.legend(loc = "lower right")
plt.title("Gender association of male and female occupation terms")

fig.savefig("plots/genderAssociationJobs.pgf")
fig.savefig("plots/genderAssociationJobs.pdf")


plt.clf()
with open("data/deu_news_2011-2016_averageGenderAssociationNames") as f:
        results = eval(f.read())

m = results[2]
f = results[3]
f = map(lambda x: -x, results[3])

m.sort()
f.sort()

plt.plot(m, "bo", label = "Male names")
plt.plot(f, "ro", label = "Female names")

plt.tick_params(axis='both', which='both', top='off', right='off', bottom='off')
plt.xticks([])
plt.xlabel("Terms ordered by their association value")
plt.ylabel("Association with respective gender")

plt.legend(loc = "lower right")
plt.title("Gender association of male and female names")

fig.savefig("plots/genderAssociationNames.pgf")
fig.savefig("plots/genderAssociationNames.pdf")

