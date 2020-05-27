# Bornholmsk

Language processing resources and tools for Bornholmsk, a language spoken on the island of Bornholm, with roots in Danish and closely related to Scanian. Includes corpora, word vectors, and parallel Bornholmsk/Danish text.

The language resources are in `resources/`. Processed corpora are in the top directory, including the parallel text for machine translation (`parallel.*`). The CC embeddings are 300-dimension and aligned with the FastText multilingual space using the algorithm in `align.py`. The `.clean` corpus skips some less-canonical resources. The `resources/` directory also contains some source PDFs, including a good scan of Kuhre's Sansager and Espersen's 1908 Ordbog (both public domain). The Kuhre is split into chapters and aligned, tidied Danish and Bornholmsk. The split-chapter versions have had some slight edits to ensure 1:1 sentence alignment. There are also a few selected works by Otto Lunch. Note that the `resources/` contains also some Danish gazetteers, mostly for anchoring the machine translation system, which can otherwise be ignored.

## Licensing
Annotations licensed CC-BY. Some material public domain (e.g. CC0). The embeddings are licensed CC-BY (open for use, attribution is required). If you use this data/tools, you must acknowledge their source.

## Contact
Contact: Leon Strømberg-Derczynski, ITU Copenhagen (ld@itu.dk)

## Attribution
Some data is credited to Allan B. Hansen / Gubbana.dk, to Espersen's 1908 dictionary, to Dion Westh / Bornholmersnak.dk, and to Wikipedia / The Wikimedia Foundation.


## Acknowledgment
Credit this as "Derczynski, L. S., & Kjeldsen, A. S. (2019, October). Bornholmsk Natural Language Processing: Resources and Tools. In Proceedings of the 22nd Nordic Conference on Computational Linguistics. NEALT."

Bibtex is:
```
@inproceedings{derczynski2019bornholmsk,
  title={Bornholmsk Natural Language Processing: Resources and Tools},
  author={Derczynski, Leon Str{\o}mberg and Copenhagen, ITU and Kjeldsen, Alex Speed},
  booktitle={Proceedings of the 22nd Nordic Conference on Computational Linguistics},
  year={2019},
  pages={338--410},
  publisher={NEALT}
}
```
