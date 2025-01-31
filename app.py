import streamlit as st
import spacy
import random
import nltk
from nltk.corpus import wordnet
from textblob import TextBlob

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

# --- Custom Simple Language Rules ---
SIMPLIFY_DICT = {
    "technology": "tech stuff",
    "generator": "tool",
    "environment": "nature",
    "utilize": "use",
    "approximately": "about",
    "communication": "talking",
    "revolutionized": "changed completely",
    "global community": "worldwide friends",
    "digital addiction": "screen time problems"
}

CONVERSATIONAL_STARTERS = [
    "You know what's cool?", "Here's something neat!", 
    "Fun fact alert!", "Check this out!", 
    "Did you hear about this?", "Guess what?"
]

EMOJIS = ["📱", "💡", "🌎", "✨", "🤓", "👧"]

def simplify_text(text):
    """Enhanced simplification with grammar checks"""
    # Stage 1: Grammar correction
    text = TextBlob(text).correct()
    
    # Stage 2: Context-aware replacement
    doc = nlp(text)
    simplified = []
    for token in doc:
        simple_word = SIMPLIFY_DICT.get(token.text.lower(), token.text)
        simplified.append(simple_word if should_replace(token) else token.text)
    
    # Stage 3: Natural sentence reconstruction
    text = " ".join(simplified)
    sentences = [sent.text for sent in nlp(text).sents]
    text = ". ".join([rebuild_sentence(sent) for sent in sentences])
    
    # Stage 4: Humanization
    return humanize_text(text)

def should_replace(token):
    """Avoid replacing proper nouns and specific cases"""
    return (
        token.text.lower() in SIMPLIFY_DICT and
        not token.ent_type_ and
        token.pos_ not in ["PROPN", "PRON"]
    )

def rebuild_sentence(sentence):
    """Ensure grammatical structure"""
    # Fix articles and basic grammar
    sentence = sentence.replace(" a ", " a ").replace(" an ", " a ")
    sentence = sentence.replace(" the ", " the ")
    
    # Capitalize first letter
    if len(sentence) > 0:
        sentence = sentence[0].upper() + sentence[1:]
    
    # Ensure sentence ends with punctuation
    if not sentence.endswith((".", "!", "?")):
        sentence += "."
    
    return sentence

def humanize_text(text):
    """Add natural conversational elements"""
    # Add conversational starters
    if random.random() < 0.4:
        starter = random.choice(CONVERSATIONAL_STARTERS)
        text = f"{starter} {text[0].lower()}{text[1:]}"
    
    # Add contractions
    text = text.replace("do not", "don't").replace("is not", "isn't")
    
    # Add emojis and pauses
    if random.random() < 0.3:
        text = text.replace(".", f"{random.choice(EMOJIS)}.", 1)
    if random.random() < 0.2:
        text = text.replace(",", ", like,", 1)
    
    # Vary sentence lengths
    sentences = text.split(". ")
    if len(sentences) > 3:
        text = ". ".join([s for i, s in enumerate(sentences) if i % 2 == 0])
    
    return text

# --- Streamlit Interface ---
st.set_page_config(page_title="Kid-Friendly Text Maker", page_icon="👧")
st.title("👧 Text Simplifier for Kids")

input_text = st.text_area("Paste your text here:", height=150)
if st.button("Make It Kid-Friendly!"):
    if input_text.strip():
        with st.spinner("Cooking up a simple version..."):
            output = simplify_text(input_text)
            st.subheader("Easy-to-Read Version")
            st.write(output)
            st.download_button("Save Text", output)
    else:
        st.warning("Please enter some text first!")

st.markdown("---")
st.info("💡 Tip: Use short paragraphs for best results!")
