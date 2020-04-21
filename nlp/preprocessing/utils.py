import re

def allowed_lexeme_list(arr):
    lexemes = [re.sub(r'[\W_]+', ' ', el).split(' ') for el in arr]
    return lexemes