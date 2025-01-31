import streamlit as st
import spacy
from spacy.cli import download
from spacy.util import load_model
import random
from nltk.corpus import wordnet
import nltk

# --- Compatibility Fix ---
try:
    nlp = spacy.load("en_core_web_sm")
except (OSError, ImportError):
    download("en_core_web_sm")
    nlp = load_model("en_core_web_sm")

# --- Required NLTK Setup ---
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# --- Simplified Version ---
def simplify_text(text):
    """Basic text simplification without external models"""
    doc = nlp(text)
    output = []
    for sent in doc.sents:
        simplified = []
        for token in sent:
            # Get simple synonyms
            syns = wordnet.synsets(token.text)
            if syns:
                simplified.append(syns[0].lemmas()[0].name())
            else:
                simplified.append(token.text)
        output.append(" ".join(simplified))
    return humanize_text(". ".join(output))

def humanize_text(text):
    """Add natural-sounding elements"""
    if random.random() < 0.3:
        text = f"Hey! {text[0].lower()}{text[1:]}"
    if random.random() < 0.2:
        text = text.replace(" and ", " & ")
    return text

# --- Streamlit UI ---
st.set_page_config(page_title="Simple Text Converter", page_icon="👧")
st.title("👧 Text Simplifier for Kids")

input_text = st.text_area("Enter text:", height=150)
if st.button("Simplify"):
    if input_text.strip():
        output = simplify_text(input_text)
        st.subheader("Simplified Text")
        st.write(output)
    else:
        st.warning("Please enter some text!")
