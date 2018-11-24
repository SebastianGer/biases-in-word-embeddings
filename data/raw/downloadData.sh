for i in 2007 2008 2009 2010 2011 2012 2013; do
  wget http://www.statmt.org/wmt14/training-monolingual-news-crawl/news.$i.de.shuffled.gz
  gzip -d news.$i.de.shuffled.gz
done

wget http://www.statmt.org/wmt15/training-monolingual-news-crawl-v2/news.2014.de.shuffled.v2.gz
gzip -d news.2014.de.shuffled.v2.gz

wget http://data.statmt.org/wmt16/translation-task/news.2015.de.shuffled.gz
gzip -d news.2015.de.shuffled.gz

wget http://data.statmt.org/wmt17/translation-task/news.2016.de.shuffled.gz
gzip -d news.2016.de.shuffled.gz
