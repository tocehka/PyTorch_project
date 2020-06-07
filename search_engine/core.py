import hnswlib
from config import Config

class SearchPosition:
    def __init__(self, model, engine):
        self.model = model
        self.engine = engine
        self.conf = Config()

    def search(self, query_sent, indexes=None, n=5):
        if self.engine == "hnsw":
            dim = 4096
            p = hnswlib.Index(space='cosine', dim=dim)
            print(f"Loading index from {self.conf.hnsw_indexes}")
            p.load_index(self.conf.hnsw_indexes)
            print("Search by HNSW + InfraSent (FastText):\n")
            labels, distances = p.knn_query(self.model.encode([query_sent])[0], k=n)
            print(labels, distances)
            for label in labels[0]:
                print(indexes[label])
            print("\n")
        elif self.engine == "fse":
            print("Search by FSE + Smooth Inverse Frequency (FastText):\n")
            res = self.model.sv.similar_by_sentence(query_sent, self.model, indexable=indexes, topn=n)
            print(res)
            print("\n")
