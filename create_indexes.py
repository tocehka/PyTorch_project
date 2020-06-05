import hnswlib
import numpy as np
from utils import DataCompiler
from nlp.embedding import create_model

data = DataCompiler(["data.csv","data1.csv","data2.csv","data3.csv"])
data = data.compile_to_preprocessed_data()
print("Start creating indexes")
print("Length of positions: ",len(data))
infsent = create_model(data)

dim = 4096
num_elements = len(data)

embeddings = []
labels = []
for i, sentence in enumerate(data):
    print(f"{i+1} of {len(data)} is embedding")
    embeddings.append(infsent.encode([" ".join(sentence["sentence"])])[0])
    labels.append(sentence["index"])


p = hnswlib.Index(space = 'cosine', dim = dim)
p.init_index(max_elements = num_elements, ef_construction = 200, M = 16)
p.add_items(embeddings, labels)
p.set_ef(40)

labels, distances = p.knn_query(embeddings, k=1)
print("Recall for the positions:", np.mean(labels.reshape(-1) == np.arange(len(embeddings))), "\n")

index_path='position_indexes.bin'
print(f"Saving indexes to {index_path}")
p.save_index(index_path)