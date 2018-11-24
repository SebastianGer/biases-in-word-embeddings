# Investigating a measure to detect societal biases in the word2vec model

Experiments were performed on a public data set of news articles found at http://www.statmt.org/wmt17/translation-task.html

This work is based on my bachelor thesis 'Examining societal biases in word vector models trained on German language corpora', therefore, some folders and files are included that are not relevant to the experiments in the paper. 


## Preparation
Before executing any experiments, we must download and extract German News Crawl articles into 'data/raw/' by executing 'data/raw/downloadData.sh' from within that directory. Next, we preprocess the data using 'src/preprocess/preprocessAll.sh', removing stop words, converting umlauts etc.. Then, we create ten random permutations of the corpora by running 'src/preprocess/preshuffle.sh' so we don't have to shuffle the data every time we run a crossvalidated experiment.

## Experiments

Experiments can be found in 'src/experiments/'. Any experiments should be started with working directory set to the root directory of this project. 

To run the experiments mentioned in the paper, run 'src/experiments/robustnessToPermutation.py' and 'src/experiments/robustnessToSubsampling.py' after performing the preparation steps mentioned above.

## Folder structure
data
-raw (raw data should be downloaded here)
-processed (scripts place preprocessed data here)
-external (any external data used for tests)
--iats (word lists, mostly procured from psychological IATs, used by us for the WEAT)
---de (German word lists for WEAT)
---en (English word lists used by Caliskan et al. in their WEAT)
---parallel (Tests for parallel comparison of psychological experiments, results computed on Calsikan et al.'s and our models)

src (contains source code)
-train (code to train word embedding models)
--word2vec
--glove
-test (semantic/syntactic and bias tests)
--GermanWordEmbeddings (code from https://github.com/devmount/GermanWordEmbeddings, we only use the syntactic/semantic tests)
-experiments (code to run the experiments mentioned in thesis and paper)

models (scripts save models in the respective subfolders)
-glove
-word2vec

results (results of experiments are placed here by the scripts)
-word2vec
-glove

paper (contains scripts and data to create the plots used in thesis and paper)
-data
-plots
