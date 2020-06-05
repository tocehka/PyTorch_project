from gensim.models import FastText
from fse.models.sif import SIF
from fse import IndexedList

# import torch
# from torch.autograd import Variable
# import numpy as np
# import torch.functional as F
# import torch.nn.functional as F
# import hnswlib

def get_fasttext_embedding(sentences):
    sentences = [sent["sentence"] for sent in sentences]
    embedding_size = 80
    window_size = 50
    min_word = 1
    down_sampling = 1e-3
    iters = 50
    print("FastText was started for train")
    ft = FastText(sentences, size=embedding_size,
                      window=window_size,
                      min_count=min_word,
                      sample=down_sampling,
                      word_ngrams=4,
                      sg=1,
                      iter=iters)
    print("FastText was finished train")
    print("SIF create indexes for embeddings")
    model = SIF(ft)
    idx_sentences = IndexedList(sentences)
    model.train(idx_sentences, queue_factor=4)
    return model, idx_sentences

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