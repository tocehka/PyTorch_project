if __name__ == "__main__":
    from utils import DataCompiler

    data = DataCompiler(["data.csv","data1.csv","data2.csv","data3.csv"])
    data = data.compile_to_preprocessed_data()
    for item in data:
        print(item)