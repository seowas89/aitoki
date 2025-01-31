import streamlit as st

# --- MUST BE THE VERY FIRST STREAMLIT COMMAND ---
st.set_page_config(
    page_title="Smart Kid Text",
    page_icon="👧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- NOW IMPORT OTHER LIBRARIES ---
import spacy
import nltk
from textblob import TextBlob
import re
import textstat
from transformers import pipeline
from nltk.corpus import wordnet
import random

# --- INITIALIZATION ---
@st.cache_resource
def load_models():
    # SpaCy model
    try:
        nlp = spacy.load("en_core_web_sm")
    except:
        from spacy.cli import download
        download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
    
    # NLTK data
    try:
        nltk.data.find('corpora/wordnet')
    except:
        nltk.download('wordnet')
    
    # T5 model
    simplifier = pipeline("text2text-generation", model="t5-small")
    
    return nlp, simplifier

nlp, simplifier = load_models()

# --- SIMPLIFICATION RULES ---
SIMPLIFY_DICT = {
    "technology": "tech stuff",
    "approximately": "about",
    "utilize": "use",
    "communication": "talking",
    "environment": "nature",
    "global community": "friends worldwide",
    "significant": "important",
    "methodologies": "ways",
    "contemporary": "modern",
    "integral": "important"
}

CONVERSATIONAL_STARTERS = [
    "Did you know?", "Here's something cool!", 
    "Fun fact!", "Guess what?", "Check this out!"
]

# --- PROCESSING FUNCTIONS ---
def enhance_grammar(text):
    """Multi-stage grammar correction"""
    try:
        corrected = str(TextBlob(text).correct())
        corrected = re.sub(r"\bi\b", "I", corrected)
        corrected = re.sub(r"\b(a|an|the)\s+(\w)", lambda m: f"{m.group(1)} {m.group(2).lower()}", corrected)
        return corrected
    except:
        return text

def simplify_text(text, strength=3):
    """Enhanced simplification pipeline"""
    try:
        # Preprocessing
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Grammar correction
        text = enhance_grammar(text)
        
        # AI Simplification
        simplified = simplifier(
            f"simplify: {text}",
            max_length=512,
            num_beams=4,
            early_stopping=True
        )[0]['generated_text']
        
        # Word replacement
        doc = nlp(simplified)
        processed = []
        for token in doc:
            if token.text.lower() in SIMPLIFY_DICT and strength > 2:
                processed.append(SIMPLIFY_DICT[token.text.lower()])
            else:
                processed.append(token.text)
        
        # Post-processing
        text = " ".join(processed)
        text = re.sub(r'\s([?.!,](?:\s|$))', r'\1', text)
        
        # Humanization
        return humanize_text(text)
    
    except Exception as e:
        return f"Error: {str(e)}"

def humanize_text(text):
    """Add natural conversational elements"""
    text = text.replace(" do not ", " don't ").replace(" does not ", " doesn't ")
    
    if random.random() < 0.4:
        starter = random.choice(CONVERSATIONAL_STARTERS)
        text = f"{starter} {text[0].lower()}{text[1:]}"
    
    sentences = text.split('. ')
    if len(sentences) > 3:
        text = ". ".join([s for i, s in enumerate(sentences) if i % 2 == 0])
    
    return text

# --- MAIN APP ---
st.title("👧 Smart Text Simplifier")

# Sidebar Controls
with st.sidebar:
    st.header("Settings ⚙️")
    strength = st.slider("Simplification Strength", 1, 5, 3)
    show_stats = st.checkbox("Show Readability Stats", True)
    example_btn = st.button("Load Example")

# Main Interface
col1, col2 = st.columns([2, 1])

with col1:
    input_text = st.text_area("Input Text:", height=200, 
                            placeholder="Paste your text here...")
    
    if example_btn:
        input_text = ("Technological advancements have revolutionized contemporary " 
                     "communication methodologies, facilitating instantaneous global "
                     "connectivity through digital platforms.")

with col2:
    st.markdown("### Tips 💡")
    st.write("- Use short paragraphs (3-4 sentences)")
    st.write("- Avoid technical jargon")
    st.write("- Break complex ideas into parts")

if st.button("✨ Simplify Text"):
    if input_text.strip():
        with st.spinner("Creating kid-friendly version..."):
            output = simplify_text(input_text, strength)
            
            # Main Output
            with col1:
                st.subheader("Simplified Text")
                st.write(output)
                st.download_button("📥 Download Text", output)
            
            # Statistics
            if show_stats:
                with col2:
                    st.subheader("📊 Readability")
                    st.metric("Grade Level", 
                            f"{textstat.flesch_kincaid_grade(output):.1f}")
                    st.metric("Reading Ease", 
                            f"{textstat.flesch_reading_ease(output):.0f}/100")
    else:
        st.warning("Please enter some text first!")

st.markdown("---")
st.info("Note: Results may vary based on input complexity. For best results, use complete sentences.")
