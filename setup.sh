#!/bin/bash
python -m spacy download en_core_web_sm
python -m nltk.downloader wordnet
python -m textblob.download_corpora
