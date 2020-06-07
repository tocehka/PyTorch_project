import pandas as pd
import re
from config import Config
from nlp.preprocessing import allowed_lexeme_list
from time import time

def dirty_load_and_process():
    conf = Config()
    df = pd.read_excel(conf.dirty_excel)
    positions = df[df.columns[1]].dropna()

    data = []
    for pos in positions:
        sent = pos.lower()
        if "ledeme" in sent:
            match = re.search(r"l(.?)[0-9]+(.{2}?)[0-9]", sent)
            article = ""
            if match:
                article = match.group(0).replace("(", " ").replace("в", "b")
                if article[1] == " ":
                    article = article[:3].replace(" ", "") + article[3:]
                    article = article.split()[0]
                    sent = sent.replace(article[0] + " " + article[1:], "")
                else:
                    article = article.split()[0]
                    sent = sent.replace(article, "")
                sent = allowed_lexeme_list(sent.split())
                sent.insert(0, article)
                data.append({"sentence": sent, "article": article})
    return data

def benchmark(func):
    def wrapper(*args, **kwargs):
        start = time()
        labels, distances = func(*args)
        end = time() - start
        print(f"Time was spent for positions search: {end}")
        clean_data = args[0]
        dirty_data = args[1]
        acc = 0
        for i, pos in enumerate(dirty_data):
            if True in [True for label in labels[i] if pos["article"] == clean_data[label]["article"]]:
                acc += 1
        acc = acc / len(dirty_data)
        print(f"Benchmark accuracy: {acc}")
        print(f"All positions from dirty database: {len(dirty_data)}")
        return labels, distances
    return wrapper