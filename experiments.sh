#!/bin/bash

mkdir experiment/

# generate bornholmsk embeddings
./gen_bornholmsk_corpus.py > experiment/bo_corpus.txt
fasttext skipgram -input experiment/bo_corpus.txt -output experiment/bo.300d -minCount 1 -minn 2 -maxn 5 -dim 300

# generate bilingual list
cat bo_da_word*tsv | sort -u | shuf > experiment/bo_da_word.tsv

# split list into train & test
head -n 450 experiment/bo_da_word.tsv > experiment/bo_da_word_test.tsv
tail -n +450 experiment/bo_da_word.tsv > experiment/bo_da_word_train.tsv

# align embeddings: unsup, sup, combi
echo "ALIGN: UNSUP"
./align.py -s experiment/bo.300d.vec -t /datasets/cc.da.300.vec -o experiment/bornholmsk.300d.cc-da-aligned.unsup -u

echo "ALIGN: SUP"
./align.py -s experiment/bo.300d.vec -t /datasets/cc.da.300.vec -o experiment/bornholmsk.300d.cc-da-aligned.sup -d experiment/bo_da_word_train.tsv

echo "ALIGN: MIXED"
./align.py -s experiment/bo.300d.vec -t /datasets/cc.da.300.vec -o experiment/bornholmsk.300d.cc-da-aligned.mixed -u -d experiment/bo_da_word_train.tsv

# evaluate embeddings w/ test set
echo "EVAL: UNSUP"
./eval_alignment.sh -s experiment/bornholmsk.300d.cc-da-aligned.unsup -t /datasets/cc.da.300.vec -d experiment/bo_da_word_test.tsv

echo "EVAL: SUP"
./eval_alignment.sh -s experiment/bornholmsk.300d.cc-da-aligned.unsup -t /datasets/cc.da.300.vec -d bo_da_word.tsv

echo "EVAL: MIXED"
./eval_alignment.sh -s experiment/bornholmsk.300d.cc-da-aligned.unsup -t /datasets/cc.da.300.vec -d bo_da_word.tsv
