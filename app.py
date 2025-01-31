import streamlit as st
import spacy
from nltk.corpus import wordnet
from transformers import pipeline
import random
from textblob import TextBlob  # For simple text processing

# --- Free Alternative Setup ---
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Load free summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# --- Core Functions ---
def simplify_text(text):
    """Simplification pipeline using free resources"""
    # Step 1: Basic preprocessing
    doc = nlp(text)
    
    # Step 2: Replace complex words
    simplified = [replace_with_simple(word.text) for word in doc]
    text = " ".join(simplified)
    
    # Step 3: Split long sentences
    text = ". ".join([shorten_sentence(sent.text) for sent in doc.sents])
    
    # Step 4: Summarize with BART model
    simplified = summarizer(
        text,
        max_length=150,
        min_length=30,
        do_sample=False,
        truncation=True
    )[0]['summary_text']
    
    # Step 5: Add human touches
    return humanize_text(simplified)

def replace_with_simple(word):
    """Use NLTK WordNet for synonym replacement"""
    simple_words = {
        "utilize": "use",
        "commence": "start",
        "terminate": "end",
        "approximately": "about"
    }
    
    # Check custom dictionary first
    if word.lower() in simple_words:
        return simple_words[word.lower()]
    
    # Fallback to NLTK synonyms
    syns = wordnet.synsets(word)
    if syns:
        return syns[0].lemmas()[0].name()
    return word

def shorten_sentence(sentence):
    """Basic sentence splitting"""
    if len(sentence.split()) > 15:
        return ". ".join(sentence.split(", "))
    return sentence

def humanize_text(text):
    """Add conversational elements without external APIs"""
    # Add questions randomly
    if random.random() < 0.3:
        text = f"Did you know? {text[0].lower()}{text[1:]}"
    
    # Add exclamations
    exclamations = ["Cool!", "Wow!", "Awesome!"]
    if random.random() < 0.2:
        text = f"{random.choice(exclamations)} {text}"
    
    # Simple grammar mistakes
    if random.random() < 0.1:
        text = text.replace(" and ", " & ")
    
    return text

# --- Streamlit UI ---
st.set_page_config(page_title="Free Text Simplifier", page_icon="👧")
st.title("👧 Free Text Simplifier for Kids")

input_text = st.text_area("Enter your text:", height=150)
if st.button("Simplify!"):
    if input_text:
        with st.spinner("Making it kid-friendly..."):
            result = simplify_text(input_text)
            st.subheader("Simplified Text")
            st.write(result)
            st.download_button("Download", result)
    else:
        st.warning("Please enter some text!")
