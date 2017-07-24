#!/bin/bash
for i in 2007 2008 2009 2010 2011 2012 2013; do
  wget http://www.statmt.org/wmt14/training-monolingual-news-crawl/news.$i.de.shuffled.gz
done
