import re

def allowed_lexeme_list(arr):
    lexemes = []
    [lexemes.extend(re.sub(r'[\W_]+', ' ', el).split(' ')) for el in arr]
    return [lexeme for lexeme in lexemes if len(lexeme) > 1 or lexeme.isdigit()]

def prepare_sentence(positions):
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
            else:
                sent = allowed_lexeme_list(sent.split())
                data.append({"sentence": sent, "article": ""}) 
    return data