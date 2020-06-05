class SearchPosition:
    def __init__(self, model):
        self.model = model

    def search(self, query_sent, indexes, n=5):
        res = self.model.sv.similar_by_sentence(query_sent, self.model, indexable=indexes, topn=n)
        print(res)
