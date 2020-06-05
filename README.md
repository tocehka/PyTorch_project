# Machine search and DB merge
### Project was realised with target of exploration opportunities of machine search and data base merge

## Requirements:
1. Python 3.6 or higher
2. List of dependencies specify in setup.py

For installation all dependencies necessary write in console
<code>pip install .</code>

## Main idea is using approach of sentences embedding and pass it to tool for indexes creation such as HNSW or FSE
hnswlib - https://github.com/nmslib/hnswlib
fse - https://github.com/oborchers/Fast_Sentence_Embeddings

## For embedding using two methods:
1. InferSent - https://github.com/facebookresearch/InferSent - Facebook methods of sentences embedding based on Word2Vec, Glove or FastText depending on the task
2. FSE + FastText trained on own data

## Second part - site parsing
### For purpose of real product data grabbing was used requests and BeatifulSoup library with proxies

# Project start priority:
- You need parse date with help of run <code>python parse.py</code>
- After data grabing - you need compile data and create HNSW index. For this run <code>python create_indexes.py</code>
- Finally - you can run main script which call search methods for your inner query (for this monent)
