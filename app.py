import streamlit as st
import spacy
import random
import nltk
from textblob import TextBlob
from nltk.corpus import wordnet

# --- Initialize NLP ---
try:
    nlp = spacy.load("en_core_web_sm")
except:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# --- Input Validation ---
def validate_input(text):
    """Ensure input is valid text"""
    if not isinstance(text, str):
        return ""
    return text.strip()

# --- Core Function with Type Safety ---
def simplify_text(text):
    """Robust text processing with type checks"""
    # Ensure text is string
    text = validate_input(text)
    if not text:
        return "Please enter some text to simplify!"
    
    # Grammar correction
    try:
        text = str(TextBlob(text).correct())
    except:
        pass
    
    # Process with spaCy
    try:
        doc = nlp(str(text))  # Explicit string conversion
    except Exception as e:
        return f"Error processing text: {str(e)}"
    
    # Rest of processing logic...
    # [Keep your existing simplification code here]
    
    return final_output

# --- Streamlit Interface ---
st.set_page_config(page_title="Kid Text Converter", page_icon="👧")
st.title("👧 Text Simplifier for Kids")

input_text = st.text_area("Enter your text:", height=150)
if st.button("Simplify"):
    if input_text:
        with st.spinner("Making it kid-friendly..."):
            output = simplify_text(str(input_text))  # Force string conversion
            st.subheader("Simple Version")
            st.write(output)
    else:
        st.warning("Please enter some text first!")
