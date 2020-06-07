import nltk
#nltk.download('punkt')
import torch
from config import Config
from .nlp_models import InferSent

from fse.models.sif import SIF
from fse import IndexedList
from .embedding import load_fasttext_model

conf = Config()
params_model = {'bsize': 24, 'word_emb_dim': 300, 'enc_lstm_dim': 2048,
                'pool_type': 'max', 'dpout_model': 0.0, 'version': 2}

def create_infersent_model(sentences):
    sentences = [" ".join(sent["sentence"]) for sent in sentences]
    infersent = InferSent(params_model)
    infersent.load_state_dict(torch.load(conf.infs_model_path))
    infersent.set_w2v_path(conf.ft_vectors_path)
    infersent.build_vocab(sentences, tokenize=False)
    return infersent

def create_fse_model(sentences):
    sentences = [sent["sentence"] for sent in sentences]
    print("SIF create indexes for embeddings")
    ft = load_fasttext_model()
    model = SIF(ft)
    idx_sentences = IndexedList(sentences)
    model.train(idx_sentences, queue_factor=4)
    return model, idx_sentences
