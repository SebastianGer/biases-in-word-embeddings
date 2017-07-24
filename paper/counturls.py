# Counts how many sentences each url and each domain contributes to the dataset
# Requires the file deu_news_urls to be present which contains one URL per line, one for each sentence in the dataset. It can only be aggregated from the private data set.

import re
from collections import defaultdict

urls = defaultdict(lambda:0)
domains = defaultdict(lambda:0)

cnt = 0

with open("deu_news_urls", "r") as f:
	for line in f:
		url = line.rstrip('\n')
		urls[url] = urls[url] + 1

		# strip any non-domain information
		url = re.sub("https?://", "", url)
		url = re.sub("www.","", url)
		url = re.sub("/.*", "", url)
		url = re.sub("\?.*", "", url)
		url = re.sub("#.*", "", url)
		url = re.sub("dns:", "", url)
		domains[url] = domains[url] + 1

		cnt += 1
		if (cnt %100000 == 0):
			print str(cnt*100.0/171464986)+" %"


with open("urlcounts2", "w") as f:
	for entry in urls:
		f.write(entry+"\t"+str(urls[entry]))
		f.write('\n')

with open("domaincounts2", "w") as f:
	for entry in domains:
		f.write(entry+"\t"+str(domains[entry]))
		f.write('\n')

