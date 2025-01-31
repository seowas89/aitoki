import streamlit as st
import spacy
import random
import nltk
from nltk.corpus import wordnet
from textblob import TextBlob

# --- Fix for spaCy/WordNet initialization ---
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

# --- Custom Simple Word Dictionary ---
SIMPLE_WORDS = {
    "technology": "tech stuff",
    "generator": "maker",
    "transformer": "smart tool",
    "contextually": "in context",
    "coherent": "clear",
    "impact": "effect",
    "society": "people",
    "integral": "important",
    "reshape": "change",
    "revolutionary": "big",
    "advent": "coming",
    "instantaneously": "right away"
}

def simplify_text(text):
    """Improved simplification with custom rules"""
    # Step 1: Basic cleaning
    doc = nlp(text)
    
    # Step 2: Replace complex words
    simplified = []
    for token in doc:
        if token.text.lower() in SIMPLE_WORDS:
            simplified.append(SIMPLE_WORDS[token.text.lower()])
        elif len(token.text) > 8 and not token.is_punct:  # Long words
            simple = get_simple_synonym(token.text)
            simplified.append(simple)
        else:
            simplified.append(token.text)
    
    # Step 3: Rebuild text with proper spacing
    text = " ".join(simplified)
    
    # Step 4: Split long sentences
    sentences = [sent.text for sent in nlp(text).sents]
    text = ". ".join([shorten(sent) for sent in sentences])
    
    # Step 5: Make kid-friendly
    return humanize_text(text)

def get_simple_synonym(word):
    """Get child-friendly synonyms with filtering"""
    syns = wordnet.synsets(word)
    if syns:
        for lemma in syns[0].lemmas():
            candidate = lemma.name().replace("_", " ")
            if len(candidate) <= len(word) and " " not in candidate:
                return candidate
    return word

def shorten(sentence):
    """Split long sentences naturally"""
    if len(sentence.split()) > 12:
        return ".\n".join(sentence.split(", "))
    return sentence

def humanize_text(text):
    """Make text conversational for kids"""
    # Add questions and exclamations
    if random.random() < 0.4:
        starters = ["Guess what?", "Did you know?", "Cool fact:", "Hey!"]
        text = f"{random.choice(starters)} {text[0].lower()}{text[1:]}"
    
    # Simplify punctuation
    text = text.replace(" - ", " ").replace(";", ".")
    
    # Add emojis
    emojis = ["📱", "💻", "🌍", "✨"]
    if random.random() < 0.3:
        text += f" {random.choice(emojis)}"
    
    return text

# --- Streamlit UI ---
st.set_page_config(page_title="Kid-Friendly Text", page_icon="👧")
st.title("👧 Make Text Easy for Kids!")

input_text = st.text_area("Enter your text:", height=150)
if st.button("Simplify"):
    if input_text.strip():
        with st.spinner("Making it kid-friendly..."):
            output = simplify_text(input_text)
            st.subheader("Simple Version")
            st.write(output)
            st.download_button("Download", output)
    else:
        st.warning("Please enter some text first!")
