import streamlit as st
import spacy
import random
import nltk
from nltk.corpus import wordnet
from textblob import TextBlob
import re

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

# --- Enhanced Replacement Rules ---
SIMPLIFY_DICT = {
    "technology": "tech",
    "approximately": "about",
    "utilize": "use",
    "communication": "talking",
    "environment": "nature",
    "global community": "worldwide friends",
    "significant": "important",
    "revolutionized": "changed completely"
}

def simplify_text(text):
    """Improved simplification with grammatical safeguards"""
    try:
        # Stage 1: Initial cleaning
        text = re.sub(r'\s+', ' ', str(text)).strip()
        
        # Stage 2: Grammar correction
        corrected = str(TextBlob(text).correct())
        
        # Stage 3: Context-aware processing
        doc = nlp(corrected)
        simplified = []
        
        for token in doc:
            # Handle special cases first
            if token.text.lower() in ["ai", "llm"]:
                simplified.append("smart computer system")
            elif token.text.lower() in SIMPLIFY_DICT:
                simplified.append(SIMPLIFY_DICT[token.text.lower()])
            else:
                # Get age-appropriate synonyms
                simple_word = get_simple_word(token)
                simplified.append(simple_word)
        
        # Stage 4: Sentence reconstruction
        text = " ".join(simplified)
        text = re.sub(r'\s([?.!"](?:\s|$))', r'\1', text)  # Fix punctuation spacing
        sentences = [sent.text for sent in nlp(text).sents]
        
        # Stage 5: Grammar normalization
        final_output = ". ".join([
            f"{sentence[0].upper()}{sentence[1:]}" if sentence else ""
            for sentence in sentences
        ])
        
        # Stage 6: Humanization
        return add_natural_touches(final_output)
    
    except Exception as e:
        return f"Error processing text: {str(e)}"

def get_simple_word(token):
    """Get context-appropriate simple words"""
    if token.ent_type_ or token.is_punct:
        return token.text
    
    syns = wordnet.synsets(token.text)
    if syns:
        for lemma in syns[0].lemmas():
            candidate = lemma.name().replace('_', ' ')
            if len(candidate) <= len(token.text) + 2 and candidate.isalpha():
                return candidate
    return token.text

def add_natural_touches(text):
    """Add human-like elements to the text"""
    # Add contractions
    text = text.replace(" do not ", " don't ").replace(" does not ", " doesn't ")
    
    # Add conversational phrases
    starters = ["You know,", "Well,", "So,", "Actually,"]
    if random.random() < 0.3:
        text = f"{random.choice(starters)} {text[0].lower()}{text[1:]}"
    
    # Add occasional informal punctuation
    if random.random() < 0.2:
        text = text.replace(".", "...", 1)
    
    # Fix common word joins
    text = re.sub(r'\b(a|an|the)\s+(\w)', lambda m: f"{m.group(1)} {m.group(2).lower()}", text)
    
    return text

# --- Streamlit Interface ---
st.set_page_config(page_title="Kid-Friendly Text", page_icon="👧")
st.title("👧 Smart Text Simplifier")

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
