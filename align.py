#!/usr/bin/env python3

import numpy as np
from fasttext import FastVector

# from https://stackoverflow.com/questions/21030391/how-to-normalize-array-numpy
def normalized(a, axis=-1, order=2):
    """Utility function to normalize the rows of a numpy array."""
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)

def make_training_matrices(source_dictionary, target_dictionary, bilingual_dictionary):
    """
    Source and target dictionaries are the FastVector objects of
    source/target languages. bilingual_dictionary is a list of 
    translation pair tuples [(source_word, target_word), ...].
    """
    source_matrix = []
    target_matrix = []

    for (source, target) in bilingual_dictionary:
        if source in source_dictionary and target in target_dictionary:
            source_matrix.append(source_dictionary[source])
            target_matrix.append(target_dictionary[target])

    # return training matrices
    return np.array(source_matrix), np.array(target_matrix)

def learn_transformation(source_matrix, target_matrix, normalize_vectors=True):
    """
    Source and target matrices are numpy arrays, shape
    (dictionary_length, embedding_dimension). These contain paired
    word vectors from the bilingual dictionary.
    """
    # optionally normalize the training vectors
    if normalize_vectors:
        source_matrix = normalized(source_matrix)
        target_matrix = normalized(target_matrix)

    # perform the SVD
    product = np.matmul(source_matrix.transpose(), target_matrix)
    U, s, V = np.linalg.svd(product)

    # return orthogonal transformation which aligns source language to the target
    return np.matmul(U, V)

print('load vectors')
bo_dictionary = FastVector(vector_file='/datasets/bornholmsk.300d.vec')
en_dictionary = FastVector(vector_file='/datasets/crawl-300d-2M-subword.vec')

en_vector = en_dictionary["dear"]
bo_vector = bo_dictionary["skat"]
print('vecsim: dear, skat')
print(FastVector.cosine_similarity(en_vector, bo_vector))

print('build bilingual dict')
bo_words = set(bo_dictionary.word2id.keys())
en_words = set(en_dictionary.word2id.keys())
overlap = list(bo_words & en_words)
bilingual_dictionary = [(entry, entry) for entry in overlap]

# form the training matrices
print('form training matrices')
source_matrix, target_matrix = make_training_matrices(
    bo_dictionary, en_dictionary, bilingual_dictionary)

# learn and apply the transformation
print('transform')
transform = learn_transformation(source_matrix, target_matrix)
bo_dictionary.apply_transform(transform)

en_vector = en_dictionary["dear"]
bo_vector = bo_dictionary["skat"]
print('vecsim: dear, skat')
print(FastVector.cosine_similarity(en_vector, bo_vector))

bo_dictionary.export('bornholmsk.aligned.vec')