from utils import DataCompiler
from nlp.embedding import create_model
from nlp.fast_embedding import get_fasttext_embedding
from search_engine.core import SearchPosition
from nlp.preprocessing.utils import allowed_lexeme_list
import numpy as np
import hnswlib

if __name__ == "__main__":
    data = DataCompiler(["data.csv","data1.csv","data2.csv","data3.csv"])
    data = data.compile_to_preprocessed_data()
    print("Start search module")
    num_elements = len(data)
    print("Number of positions:", num_elements)
    infsent = create_model(data)
    dim = 4096
    p = hnswlib.Index(space='l2', dim=dim)
    print("Loading index from position_indexes.bin")
    p.load_index("position_indexes.bin", max_elements = num_elements)
    fast_embedding, indxs = get_fasttext_embedding(data)

    query = "Держатель Ledeme д/зубных щёток 2 стаканa"
    print("Search for:", query)

    print("Search by HNSW + InfraSent (FastText Russian set):")
    labels, distances = p.knn_query(infsent.encode([query])[0], k=5)
    print(labels, distances)
    for label in labels[0]:
        print(data[label])

    print("Search by FSE + FastText (FastText self train):")
    fast_search = SearchPosition(fast_embedding)
    fast_search.search(allowed_lexeme_list([query]), indxs, n=5)
    