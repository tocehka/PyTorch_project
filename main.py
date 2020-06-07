from utils import DataCompiler
from utils.dlap import dirty_load_and_process, benchmark
from nlp.inferences import create_infersent_model, create_fse_model
from search_engine.core import SearchPosition
from nlp.preprocessing.utils import prepare_sentence
import numpy as np

@benchmark
def collate_DB(clean, dirty, model, engine):
    search = SearchPosition(model, engine=engine)
    labels, distances = search.search(dirty, n=5, logs=False)
    return labels, distances

if __name__ == "__main__":
    print("Compiling data from csv files")
    data = DataCompiler(["data.csv","data1.csv","data2.csv","data3.csv"])
    data = data.compile_to_preprocessed_data()
    num_elements = len(data)
    print("Number of positions:", num_elements)

    infsent_model = create_infersent_model(data)
    fse_model, indxs = create_fse_model(data)

    dirty_data = dirty_load_and_process()
    # print(dirty_data)

    labels, distances = collate_DB(data, dirty_data, fse_model, "fse")

    labels, distances = collate_DB(data, dirty_data, infsent_model, "hnsw")

    # query = prepare_sentence("Набор+ Ledeme. пластиковый L421-1 (красный).")
    # print("Search for:", query)
    # print("Start search module\n")

    # fse_search = SearchPosition(fse_model, engine="fse")
    # fse_search.search([query.split()], indexes=indxs, n=5)

    # hnsw_search = SearchPosition(infsent_model, engine="hnsw")
    # hnsw_search.search([query], indexes=data, n=5)
    