import streamlit as st
import spacy
import nltk
from textblob import TextBlob
import re
import textstat
from transformers import pipeline
from nltk.corpus import wordnet
import random

# --- MUST BE FIRST STREAMLIT COMMAND ---
st.set_page_config(page_title="Smart Kid Text", page_icon="👧", layout="wide")

# --- Initialization AFTER page config ---
try:
    nlp = spacy.load("en_core_web_sm")
except:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

try:
    nltk.data.find('corpora/wordnet')
except:
    nltk.download('wordnet')

# --- Rest of your code remains the same from previous version ---
# [Keep all your existing code here without changes]
# ...
