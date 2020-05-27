#!/bin/bash
#
# take everything
# build & tokenize parallel corpora and split them
# build clean and also noisy tokenised bornholmsk data

DA_ALL="parallel.da.all"
DA_TRAIN="parallel.da.train"
DA_VAL="parallel.da.val"
DA_TEST="parallel.da.test"

DB_ALL="parallel.da-bornholm.all"
DB_TRAIN="parallel.da-bornholm.train"
DB_VAL="parallel.da-bornholm.val"
DB_TEST="parallel.da-bornholm.test"

DB_CLEAN="da-bornholm.clean.txt"
DB_NOISY="da-bornholm.noisy.txt"

> $DA_ALL
> $DB_ALL
> $DB_CLEAN
> $DB_NOISY

# kuhre
echo "Converting Kuhre"
cd resources
for chapter in `ls kuhre.ch? kuhre.ch??` ; do
  ./align_kuhre.py $chapter > /dev/null

  cat $chapter.plain.da >> ../$DA_ALL  
  cat $chapter.plain.da-bo >> ../$DB_ALL

  cat $chapter.norm.da >> ../$DA_ALL  
  cat $chapter.plain.da-bo >> ../$DB_ALL

  cat $chapter.norm.lc.da >> ../$DA_ALL  
  cat $chapter.plain.da-bo | tr 'A-Z' 'a-z' >> ../$DB_ALL
done
cd ..


# citations
echo "Converting citations"
cd resources
./align_citations.py bornholmsk_ordbog_citations.txt
cat citations.da > ../$DA_ALL
cat citations.da-bo > ../$DB_ALL
cd ..

# gubbana
echo "Converting miscellanous parallel text"
./pairs_to_files.py bo_da_sent_gubbana.txt
cat bo_da_sent_gubbana.txt.a >> $DB_ALL
cat bo_da_sent_gubbana.txt.b >> $DA_ALL

# misc
./pairs_to_files.py bo_da_sent.txt
cat bo_da_sent.txt.a >> $DB_ALL
cat bo_da_sent.txt.b >> $DA_ALL

./pairs_to_files.py da_bo_sent_bornholmskersnak.txt
cat da_bo_sent_bornholmskersnak.txt.b >> $DB_ALL
cat da_bo_sent_bornholmskersnak.txt.a >> $DA_ALL


# build bornholmsk text
echo "Building monolingual corpus:"
echo " -- citations and kuhre"
cat resources/citations.da-bo resources/kuhre*.plain.da-bo >> $DB_CLEAN
echo " -- otto j lund"
ls resources/ottolund* | xargs -n1 ./nltktok.py >> $DB_CLEAN

echo " -- untokenized text"
./nltktok.py bornholmsk-untok.txt > bornholmsk.txt
echo " -- noisy text"
cp $DB_CLEAN $DB_NOISY
cat da_bo_sent_bornholmskersnak.txt.b bo_da_sent.txt.a bo_da_sent_gubbana.txt.a bornholmsk.txt >> $DB_NOISY


# shuffle and split parallel texts
echo "Shuffle and split parallel text"
shuf --random-source=rand_seed $DB_ALL > $DB_ALL.shuf
shuf --random-source=rand_seed $DA_ALL > $DA_ALL.shuf

head -n 500 $DB_ALL.shuf > $DB_TEST
head -n 1000 $DB_ALL.shuf | tail -n 500 > $DB_VAL
tail -n +1000 $DB_ALL.shuf > $DB_TRAIN

head -n 500 $DA_ALL.shuf > $DA_TEST
head -n 1000 $DA_ALL.shuf | tail -n 500 > $DA_VAL
tail -n +1000 $DA_ALL.shuf > $DA_TRAIN

# add names to training set
cat resources/men >> $DB_TRAIN
cat resources/men >> $DA_TRAIN
cat resources/women >> $DA_TRAIN
cat resources/women >> $DB_TRAIN
cat resources/geo >> $DA_TRAIN
cat resources/geo >> $DB_TRAIN

# package up the parallel resources
zip parallel.da.da-bornholm.zip parallel.d*


# next step: get a glove encoding on DB_NOISY
# use DB_CLEAN for normalisation



