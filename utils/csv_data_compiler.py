import csv
import numpy as np
import json

from .universal import max_length_index, parsed_list_to_dict, dict_to_json, create_indexed_nlp_dict
from utils import WriterManager
from config import Config

class DataCompiler:
    def __init__(self, files_arr):
        self.__data_array = []
        for file in files_arr:
            with open(file, 'r') as csv_file:
                data = csv.reader(csv_file)
                self.__data_array.extend(data)
        self.__data_array = np.unique(np.array(self.__data_array))

    def compile_to_db_csv(self):
        header = dict_to_json(parsed_list_to_dict(self.__data_array[0]), 0).keys()
        conf = Config()
        writer = WriterManager(conf.db_file, header)
        for i, item in enumerate(self.__data_array):
            print(dict_to_json(parsed_list_to_dict(item), i))
            writer.write_row(dict_to_json(parsed_list_to_dict(item), i))
        del writer
        
    def compile_to_preprocessed_data(self):
        listd = []
        for i, item in enumerate(self.__data_array):
            listd.append(create_indexed_nlp_dict(item, i))
        return listd