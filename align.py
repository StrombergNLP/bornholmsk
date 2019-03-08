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

import argparse
p = argparse.ArgumentParser()
p.add_argument('-s', '--source', help='the embeddings to be adjusted', required=True)
p.add_argument('-t', '--target', help='the destination embedding space', required=True)
p.add_argument('-o', '--output', help='output vector filename', required=True)
p.add_argument('-u', '--unsup', help='use unsupervised alignments?', action="store_true")
p.add_argument('-d', '--biling_dict', help='path to bilingual dict TSV file (source target)')
args = p.parse_args()

print('load vectors')
source_vecs = FastVector(vector_file=args.source)
target_vecs = FastVector(vector_file=args.target)

source_words = set(source_vecs.word2id.keys())
target_words = set(target_vecs.word2id.keys())

#en_vector = target_vec["dear"]
#bo_vector = source_vecs["skat"]
#print('vecsim: dear, skat')
#print(FastVector.cosine_similarity(en_vector, bo_vector))

bilingual_dictionary = []

if args.unsup:
    print('build unsup bilingual dict')
    overlap = list(source_words & target_words)
    new_entries = [(entry, entry) for entry in overlap]
    print('found', len(new_entries), 'unsupervised alignments')
    bilingual_dictionary += new_entries

if args.biling_dict:
    words_added = 0
    for line in open(args.biling_dict, 'r'):
        line = line.strip()
        if not line:
            continue
        words = line.split('\t')
        src_word, target_word = map(str.strip, words)
        #TODO: handle OOV, eh
        if src_word in source_words and target_word in target_words:
            bilingual_dictionary += [(src_word, target_word)]
            words_added += 1
    print('found', words_added, 'supervised alignments')



# form the training matrices
print('form training matrices')
source_matrix, target_matrix = make_training_matrices(
    source_vecs, target_vecs, bilingual_dictionary)

# learn and apply the transformation
print('transform')
transform = learn_transformation(source_matrix, target_matrix)
source_vecs.apply_transform(transform)

#en_vector = target_vec["dear"]
#bo_vector = source_vecs["skat"]
#print('vecsim: dear, skat')
#print(FastVector.cosine_similarity(en_vector, bo_vector))

source_vecs.export(args.output)