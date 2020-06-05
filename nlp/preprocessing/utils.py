import re

def allowed_lexeme_list(arr):
    lexemes = []
    [lexemes.extend(re.sub(r'[\W_]+', ' ', el).split(' ')) for el in arr]
    return [lexeme for lexeme in lexemes if len(lexeme) > 1 or lexeme.isdigit()]

def prepare_sentence(sent):
    return re.sub(r'[\W_]+', ' ', sent).lower()