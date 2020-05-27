#!/bin/bash
set -e

mkdir experiment/
rm -f experiment/*pickle # get rid of leftover caches - this script refreshes the embeddings

# generate bornholmsk embeddings
echo "== GENERATE CORPUS"
./gen_bornholmsk_corpus.py > experiment/bo_corpus.txt
echo "== INDUCE SOURCE EMBEDDING"
fasttext skipgram -input experiment/bo_corpus.txt -output experiment/bo.300d -minCount 1 -minn 2 -maxn 5 -dim 300 -epoch 100

# generate bilingual list
echo "== CREATE BILINGUAL MASTER LISTS AND PARTITIONS"
cat bo_da_word*tsv | sort -u | shuf > experiment/bo_da_word.tsv

# split list into train & test
head -n 450 experiment/bo_da_word.tsv > experiment/bo_da_word_test.tsv
tail -n +450 experiment/bo_da_word.tsv > experiment/bo_da_word_train.tsv

# align embeddings: unsup, sup, combi
echo "== ALIGN: UNSUP"
./align.py -s experiment/bo.300d.vec -t /datasets/cc.da.300.vec -o experiment/bornholmsk.300d.cc-da-aligned.unsup -u -i

echo "== ALIGN: SUP"
./align.py -s experiment/bo.300d.vec -t /datasets/cc.da.300.vec -o experiment/bornholmsk.300d.cc-da-aligned.sup -d experiment/bo_da_word_train.tsv -i

echo "== ALIGN: MIXED"
./align.py -s experiment/bo.300d.vec -t /datasets/cc.da.300.vec -o experiment/bornholmsk.300d.cc-da-aligned.mixed -u -d experiment/bo_da_word_train.tsv -i

echo "== ALIGN: ALL SUP"
./align.py -s experiment/bo.300d.vec -t /datasets/cc.da.300.vec -o experiment/bornholmsk.300d.cc-da-aligned.all -d experiment/bo_da_word.tsv -i
pbzip2 experiment/bornholmsk.300d.cc-da-aligned.all

# evaluate embeddings w/ test set
echo "== EVAL: UNSUP"
./eval_alignment.sh -s experiment/bornholmsk.300d.cc-da-aligned.unsup -t /datasets/cc.da.300.vec -d experiment/bo_da_word_test.tsv

echo "== EVAL: SUP"
./eval_alignment.sh -s experiment/bornholmsk.300d.cc-da-aligned.sup -t /datasets/cc.da.300.vec -d experiment/bo_da_word_test.tsv

echo "== EVAL: MIXED"
./eval_alignment.sh -s experiment/bornholmsk.300d.cc-da-aligned.mixed -t /datasets/cc.da.300.vec -d experiment/bo_da_word_test.tsv
