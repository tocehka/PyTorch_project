# Machine search and DB merge
### Project was realised with target of exploration opportunities of machine search and data base merge

## Requirements:
1. Python 3.6 or higher
2. List of dependencies specified in setup.py

For installation all dependencies necessary write in console

<code>pip install .</code>

## Main idea is using approach of sentences embedding and pass it to tool for indexes creation such as HNSW or FSE
- hnswlib - https://github.com/nmslib/hnswlib
- fse - https://github.com/oborchers/Fast_Sentence_Embeddings

## For embedding using two methods:
1. InferSent - https://github.com/facebookresearch/InferSent - Facebook methods of sentences embedding based on PyTorch framework (LSTM layer with self pre-trained model infersent2) and word embedders (FastText, Word2Vec)
2. Fast Sentence Embedding + Smooth Inverse Frequency trained at FastText embedding

## Second part - site parsing
### For purpose of real product data grabbing was used requests and BeatifulSoup library with proxies

## For InferSent working you necessary download pre-trained model infersent2:

<code>mkdir encoder</code>

<code>curl -Lo encoder/infersent2.pkl https://dl.fbaipublicfiles.com/infersent/infersent2.pkl</code>

# Project start priority:
- You need parse data with help of run:

<code>python parse.py</code>

- After data grabing - you need compile data, build FastText embeddings for sentences and create HNSW index. For this run:

<code>python create_origin.py</code>

- Finally - you can run main script which call two search methods for your inner query (for this monent)

<code>python main.py</code>

# Results:
Number of positions: 1742

Found 2605(/2607) words with w2v vectors

Vocab size : 2605

SIF create indexes for embeddings

Search by FSE + Smooth Inverse Frequency (FastText):

<b>Time was spent for positions search: 0.11711311340332031 seconds</b>

<b>Benchmark accuracy: 0.21515151515151515</b>

All positions from dirty database: 330

Loading index from hnswidx/indexes.bin

Search by HNSW + InfraSent (FastText):

<b>Time was spent for positions search: 5.047646999359131 seconds</b>

<b>Benchmark accuracy: 0.603030303030303</b>

All positions from dirty database: 330

### Total accuracy was couted as at least one entry of true item article of K nearest neighbors. In our case - it is 5.
## For conclusion, this model sufficiently bad applicable for problem of machine DB merge as there are many nuances
## However, for simplify search and in order to reduce the load of server - this approach has the place to be
