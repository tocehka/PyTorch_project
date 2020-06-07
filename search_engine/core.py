import hnswlib
from config import Config

class SearchPosition:
    def __init__(self, model, engine):
        self.model = model
        self.engine = engine
        self.conf = Config()

    def search(self, query_sent, indexes=None, n=5, logs=True):
        try:
            query_sent = [sent["sentence"] for sent in query_sent]
        except:
            pass

        if self.engine == "hnsw":
            dim = 4096
            p = hnswlib.Index(space='cosine', dim=dim)
            print(f"Loading index from {self.conf.hnsw_indexes}")
            p.load_index(self.conf.hnsw_indexes)
            print("\nSearch by HNSW + InfraSent (FastText):\n")
            embeddings = []
            for sent in query_sent:
                embeddings.append(self.model.encode([" ".join(sent)])[0])
            labels, distances = p.knn_query(embeddings, k=n)
            if not logs:
                return labels, distances
            print(labels, distances)
            for label in labels[0]:
                print(indexes[label])
            print("\n")

        elif self.engine == "fse":
            print("\nSearch by FSE + Smooth Inverse Frequency (FastText):\n")
            labels = []
            distances = []
            for sent in query_sent:
                res = self.model.sv.similar_by_sentence(sent, self.model, indexable=indexes, topn=n)
                if logs:
                    print(res)
                    print("\n")
                    return
                labels.append([el[0] for el in res])
                distances.append([el[1] for el in res])
            return labels, distances
