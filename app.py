import streamlit as st
import spacy
import random
import nltk
from textblob import TextBlob
from nltk.corpus import wordnet

# --- Initialization ---
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

# --- Simplified Word Mapping ---
SIMPLIFY_DICT = {
    "technology": "tech stuff",
    "environment": "nature",
    "utilize": "use",
    "approximately": "about",
    "communication": "talking",
    "global community": "worldwide friends"
}

def simplify_text(text):
    """Complete text simplification process"""
    # Validate input
    text = str(text).strip()
    if not text:
        return "Please enter some text to simplify!"
    
    try:
        # Stage 1: Basic correction
        corrected = str(TextBlob(text).correct())
        
        # Stage 2: Word replacement
        doc = nlp(corrected)
        simplified = []
        for token in doc:
            word = SIMPLIFY_DICT.get(token.text.lower(), token.text)
            simplified.append(word)
        
        # Stage 3: Sentence rebuilding
        text = " ".join(simplified)
        sentences = [sent.text for sent in nlp(text).sents]
        final_output = ". ".join([
            f"{s[0].upper()}{s[1:]}" if s else s 
            for s in sentences
        ])
        
        # Stage 4: Humanize
        final_output = final_output.replace("  ", " ")
        if random.random() < 0.3:
            final_output = f"Did you know? {final_output[0].lower()}{final_output[1:]}"
        
        return final_output
    
    except Exception as e:
        return f"Oops! Something went wrong: {str(e)}"

# --- Streamlit Interface ---
st.set_page_config(page_title="Kid Text Converter", page_icon="👧")
st.title("👧 Text Simplifier for Kids")

input_text = st.text_area("Enter your text:", height=150)
if st.button("Simplify"):
    if input_text:
        with st.spinner("Making it kid-friendly..."):
            output = simplify_text(input_text)
            st.subheader("Simple Version")
            st.write(output)
            st.download_button("Download", output)
    else:
        st.warning("Please enter some text first!")
