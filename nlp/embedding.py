from gensim.models import FastText
#from gensim.models.fasttext import load_facebook_model
from config import Config
from pathlib import Path

conf = Config()

def create_fasttext_embeddings(sentences):
    sentences = [sent["sentence"] for sent in sentences]
    embedding_size = 300
    window_size = 10
    min_word = 1
    down_sampling = 0.0005
    iter_num = 200
    print("FastText started for train")
    ft = FastText(size=embedding_size,
                    window=window_size,
                    min_count=min_word,
                    sample=down_sampling,
                    sg=1)
    ft.build_vocab(sentences=sentences)
    ft.train(sentences=sentences, total_examples=ft.corpus_count, epochs=iter_num)
    Path(conf.ft_vectors_path.split("/")[0]).mkdir(parents=True, exist_ok=True)
    ft.wv.save_word2vec_format(conf.ft_vectors_path)
    ft.save(conf.ft_model_path)
    print(f"FastText finished train and saved models to {conf.ft_model_path}")

def load_fasttext_model():
    return FastText.load(conf.ft_model_path)

def update_fasttext_model(sentences):
    iter_num = 200
    sentences = [sent["sentence"] for sent in sentences]
    print("FastText started for updating")
    ft = FastText.load(conf.ft_model_path)
    ft.build_vocab(sentences=sentences, update=True)
    ft.train(sentences=sentences, total_examples=ft.corpus_count, epochs=iter_num)
    ft.wv.save_word2vec_format(conf.ft_vectors_path)
    ft.save(conf.ft_model_path)
    print(f"FastText finished updating and saved models to {conf.ft_model_path}")
    
# import torch
# from torch.autograd import Variable
# import numpy as np
# import torch.functional as F
# import hnswlib

# def create_index(data):

#     data = [sent["sentence"] for sent in data]
#     vocabulary = []
#     for sentence in data:
#         for token in sentence:
#             if token not in vocabulary:
#                 vocabulary.append(token)
#     print(vocabulary)
#     word2idx = {w: idx for (idx, w) in enumerate(vocabulary)}
#     idx2word = {idx: w for (idx, w) in enumerate(vocabulary)}

#     vocabulary_size = len(vocabulary)

#     window_size = 2
#     idx_pairs = []
#     for sentence in data:
#         indices = [word2idx[word] for word in sentence]
#         for center_word_pos in range(len(indices)):
#             for w in range(-window_size, window_size + 1):
#                 context_word_pos = center_word_pos + w
#                 if context_word_pos < 0 or context_word_pos >= len(indices) or center_word_pos == context_word_pos:
#                     continue
#                 context_word_idx = indices[context_word_pos]
#                 idx_pairs.append((indices[center_word_pos], context_word_idx))

#     idx_pairs = np.array(idx_pairs)

#     print(idx_pairs.shape)

#     def get_input_layer(word_idx):
#         x = torch.zeros(vocabulary_size).float()
#         x[word_idx] = 1.0
#         return x

#     embedding_dims = 10
#     W1 = Variable(torch.randn(embedding_dims, vocabulary_size).float(), requires_grad=True)
#     W2 = Variable(torch.randn(vocabulary_size, embedding_dims).float(), requires_grad=True)
#     num_epochs = 15
#     learning_rate = 0.001

#     for epo in range(num_epochs):
#         loss_val = 0
#         for data, target in idx_pairs:
#             x = Variable(get_input_layer(data)).float()
#             y_true = Variable(torch.from_numpy(np.array([target])).long())

#             z1 = torch.matmul(W1, x)
#             z2 = torch.matmul(W2, z1)
        
#             log_softmax = F.log_softmax(z2, dim=0)

#             loss = F.nll_loss(log_softmax.view(1,-1), y_true)
#             loss_val += loss.data
#             loss.backward()
#             W1.data -= learning_rate * W1.grad.data
#             W2.data -= learning_rate * W2.grad.data

#             W1.grad.data.zero_()
#             W2.grad.data.zero_()
 
#         print(f'Loss at epo {epo}: {loss_val/len(idx_pairs)}')
#         print(W1, W2)