#!/bin/bash
# Preprocesses all news datasets
for i in 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016; do
  python src/preprocess/preprocess.py data/raw/news.$i.de.shuffled data/preprocessed/news.$i.de.shuffled
done
