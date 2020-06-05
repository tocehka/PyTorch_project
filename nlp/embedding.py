import nltk
import torch
#nltk.download('punkt')

from .nlp_models import InferSent

MODEL_PATH = 'encoder/infersent2.pkl'
W2V_PATH = 'ft_russian/cc.ru.300.vec'
params_model = {'bsize': 24, 'word_emb_dim': 300, 'enc_lstm_dim': 2048,
                'pool_type': 'max', 'dpout_model': 0.0, 'version': 2}

def create_model(sentences):
    sentences = [" ".join(sent["sentence"]) for sent in sentences]
    infersent = InferSent(params_model)
    infersent.load_state_dict(torch.load(MODEL_PATH))
    infersent.set_w2v_path(W2V_PATH)
    infersent.build_vocab(sentences, tokenize=False)
    return infersent