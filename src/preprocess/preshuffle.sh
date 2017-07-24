#!/bin/bash
# Creates ten permutations of the WMT2013 dataset. This is used in the robustness to subsampling and permutation experiments.
# This approach saves several hours as compared to shuffling within python.
for i in 0 1 2 3 4 5 6 7 8 9; do
	shuf < data/processed/news.2013.de.shuffled > data/processed/news.2013.de.shuffled.shuf${i}
done
