import streamlit as st
import spacy
import nltk
from textblob import TextBlob
from language_tool_python import LanguageTool
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

tool = LanguageTool('en-US')  # Grammar checker

# --- Enhanced Replacement Rules ---
SIMPLIFY_DICT = {
    "technology": "tech",
    "approximately": "about",
    "utilize": "use",
    "communication": "talking",
    "environment": "nature",
    "global community": "worldwide friends",
    "significant": "important",
    "revolutionized": "changed completely",
    "methodologies": "ways",
    "contemporary": "modern"
}

def simplify_text(text):
    """Robust text simplification pipeline"""
    try:
        # Stage 1: Text normalization
        text = re.sub(r'\W+', ' ', str(text)).strip()
        text = re.sub(r'\s+', ' ', text)
        
        # Stage 2: Grammar correction
        matches = tool.check(text)
        corrected = tool.correct(text)
        
        # Stage 3: Context-aware processing
        doc = nlp(corrected)
        simplified = []
        
        for token in doc:
            # Preserve proper nouns and entities
            if token.ent_type_ or token.is_punct:
                simplified.append(token.text)
                continue
            
            # Use simple dictionary
            simple_word = SIMPLIFY_DICT.get(token.text.lower(), token.text)
            
            # Get synonyms for long words
            if len(token.text) > 8 and not token.like_num:
                syns = nltk.corpus.wordnet.synsets(token.text)
                if syns:
                    simple_word = syns[0].lemmas()[0].name().replace('_', ' ')
            
            simplified.append(simple_word)
        
        # Stage 4: Sentence reconstruction
        text = " ".join(simplified)
        text = re.sub(r'\s([?.!,](?:\s|$))', r'\1', text)
        
        # Stage 5: Final grammar check
        final_output = tool.correct(text)
        
        # Stage 6: Naturalization
        return make_conversational(final_output)
    
    except Exception as e:
        return f"Error processing text: {str(e)}"

def make_conversational(text):
    """Add natural speaking patterns"""
    # Convert to simple contractions
    replacements = {
        "do not": "don't",
        "does not": "doesn't",
        "is not": "isn't",
        "cannot": "can't"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    
    # Add sentence variety
    sentences = text.split('. ')
    modified = []
    for i, sent in enumerate(sentences):
        if i % 2 == 0 and len(sent) > 0:
            sent = f"Did you know? {sent[0].lower()}{sent[1:]}"
        modified.append(sent)
    
    return ". ".join(modified)

# --- Streamlit Interface ---
st.set_page_config(page_title="Kid Text Expert", page_icon="👧")
st.title("👧 Smart Text Simplifier")

input_text = st.text_area("Enter your text:", height=150, 
                         placeholder="Paste your text here...")

if st.button("Simplify Text"):
    if input_text.strip():
        with st.spinner("Creating kid-friendly version..."):
            output = simplify_text(input_text)
            st.subheader("Simple Version")
            st.write(output)
            
            # Show original comparison
            with st.expander("See Original vs Simple"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Original**")
                    st.write(input_text)
                with col2:
                    st.write("**Simple Version**")
                    st.write(output)
    else:
        st.warning("Please enter some text first!")

st.markdown("---")
st.info("💡 Tip: Use short paragraphs (3-4 sentences) for best results!")
