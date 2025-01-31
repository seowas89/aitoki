# app.py
import streamlit as st
import spacy
import random
from nltk.corpus import wordnet
from transformers import pipeline
from textblob import TextBlob
import nltk

# --- Initial Setup ---
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Download NLTK data
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# Load small summarization model
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="t5-small")

model = load_model()

# --- Core Functions ---
def simplify_text(text):
    """Main simplification pipeline"""
    # Step 1: Basic cleaning
    text = TextBlob(text).correct()
    
    # Step 2: Replace complex words
    simplified = " ".join([get_simple_word(word.text) for word in nlp(text)])
    
    # Step 3: Split long sentences
    simplified = ". ".join([str(sent) for sent in TextBlob(simplified).sentences])
    
    # Step 4: Simplify with T5
    simplified = model(
        f"simplify: {simplified}",
        max_length=256,
        num_beams=4,
        repetition_penalty=2.5
    )[0]['generated_text']
    
    # Step 5: Humanize
    return humanize_text(simplified)

def get_simple_word(word):
    """Get simpler synonym using NLTK"""
    syns = wordnet.synsets(word)
    if syns:
        return syns[0].lemmas()[0].name().replace("_", " ")
    return word

def humanize_text(text):
    """Add natural-sounding elements"""
    # Add conversational phrases
    starters = ["Hey there!", "Did you know?", "Check this out!", "Fun fact:"]
    if random.random() < 0.3:
        text = f"{random.choice(starters)} {text.lower()}"
    
    # Add occasional typos
    if random.random() < 0.1:
        text = text.replace(" and ", " & ").replace(" the ", " da ")
    
    # Add emojis
    emojis = ["😊", "🌟", "✨", "🎈", "🤓"]
    if random.random() < 0.2:
        text += f" {random.choice(emojis)}"
    
    return text

# --- Streamlit UI ---
st.set_page_config(page_title="Kid Text Simplifier", page_icon="👧")
st.title("👧 Free Text Simplifier for Kids")

input_text = st.text_area("Enter your text here:", height=150)
if st.button("Simplify!"):
    if input_text.strip():
        with st.spinner("Making it kid-friendly..."):
            try:
                output = simplify_text(input_text)
                st.subheader("Simplified Text")
                st.write(output)
                st.download_button("Download Result", output)
            except Exception as e:
                st.error(f"Oops! Error: {str(e)}")
    else:
        st.warning("Please enter some text to simplify!")

st.markdown("---")
st.info("Note: This free version uses open-source models and might be less polished than paid alternatives.")
