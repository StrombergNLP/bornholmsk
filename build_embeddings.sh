#!/bin/bash

mkdir experiment/

# generate bornholmsk embeddings
echo "== GENERATE CORPUS"
./gen_bornholmsk_corpus.py > experiment/bo_corpus.txt

echo "== INDUCE SOURCE EMBEDDING"
fasttext skipgram -input experiment/bo_corpus.txt -output experiment/bo.300d -minCount 1 -minn 2 -maxn 5 -dim 300

# generate bilingual list
echo "== CREATE BILINGUAL MASTER LISTS AND PARTITIONS"
cat bo_da_word*tsv | sort -u | shuf > experiment/bo_da_word.tsv

echo "== ALIGN (supervised)"
./align.py -s experiment/bo.300d.vec -t /datasets/cc.da.300.vec -o bornholmsk.300d.cc-da-aligned.all -d experiment/bo_da_word.tsv -i

