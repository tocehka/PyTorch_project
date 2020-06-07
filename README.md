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
1. InferSent - https://github.com/facebookresearch/InferSent - Facebook methods of sentences embedding based on PyTorch framework (LSTM layer with self pretrained model infersent2) and word embedders (FastText, Word2Vec)
2. Fast Sentence Embedding + Smooth Inverse Frequency trained at FastText embedding

## Second part - site parsing
### For purpose of real product data grabbing was used requests and BeatifulSoup library with proxies

# Project start priority:
- You need parse date with help of run 

<code>python parse.py</code>

- After data grabing - you need compile data, build FastText embeddings for sentences and create HNSW index. For this run 

<code>python create_origin.py</code>

- Finally - you can run main script which call two search methods for your inner query (for this monent)

<code>python main.py</code>
