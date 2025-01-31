import streamlit as st
import spacy
import random
import nltk
from textblob import TextBlob
from nltk.corpus import wordnet
import textstat  # For readability metrics

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

# --- Enhanced Simplification Rules ---
SIMPLIFY_DICT = {
    "technology": "tech stuff",
    "environment": "nature",
    "utilize": "use",
    "approximately": "about",
    "communication": "talking",
    "global community": "worldwide friends",
    "analyze": "look at",
    "significant": "important"
}

def simplify_text(text, strength=3):
    """Enhanced simplification with grammar checks"""
    try:
        # Stage 1: Grammar correction
        corrected = str(TextBlob(text).correct())
        
        # Stage 2: Context-aware replacement
        doc = nlp(corrected)
        simplified = []
        for token in doc:
            if token.text.lower() in SIMPLIFY_DICT and strength > 2:
                simplified.append(SIMPLE_WORDS[token.text.lower()])
            else:
                simplified.append(token.text)
        
        # Stage 3: Sentence reconstruction
        text = " ".join(simplified)
        sentences = [sent.text for sent in nlp(text).sents]
        
        # Stage 4: Readability enforcement
        final_output = []
        for sent in sentences:
            if textstat.flesch_reading_ease(sent) < 70 and strength > 1:
                simple_sent = " ".join([get_simple_word(word) for word in sent.split()])
                final_output.append(simple_sent)
            else:
                final_output.append(sent)
        
        # Stage 5: Humanization
        return humanize_text(". ".join(final_output))
    
    except Exception as e:
        return f"Error: {str(e)}"

def get_simple_word(word):
    """Get age-appropriate synonyms"""
    syns = wordnet.synsets(word)
    return syns[0].lemmas()[0].name() if syns else word

def humanize_text(text):
    """Add natural conversational elements"""
    # Add contractions
    text = text.replace("cannot", "can't").replace("does not", "doesn't")
    
    # Add conversational markers
    markers = ["You know,", "Well,", "So,", "Actually,"]
    if random.random() < 0.3:
        text = f"{random.choice(markers)} {text[0].lower()}{text[1:]}"
    
    return text

# --- New Features ---
def text_to_speech(text):
    """Generate audio version (client-side)"""
    from gtts import gTTS
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("output.mp3")
    return open("output.mp3", "rb").read()

def show_readability(text):
    """Display readability metrics"""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Reading Level", f"Grade {textstat.flesch_kincaid_grade(text):.1f}")
    with col2:
        st.metric("Easy to Read", f"{textstat.flesch_reading_ease(text):.0f}/100")
    with col3:
        st.metric("Complex Words", textstat.dale_chall_readability_score(text))

# --- Streamlit Interface ---
st.set_page_config(page_title="Smart Kid Text", page_icon="👧")
st.title("👧 Smart Text Simplifier")

# Sidebar Controls
with st.sidebar:
    st.header("Settings ⚙️")
    strength = st.slider("Simplification Strength", 1, 5, 3)
    show_details = st.checkbox("Show Readability Details", True)

# Main Interface
input_text = st.text_area("Enter your text:", height=150, 
                         placeholder="Paste complex text here...")

col1, col2 = st.columns([1, 3])
with col1:
    if st.button("✨ Simplify"):
        process = True
    else:
        process = False

with col2:
    if st.button("📚 Show Example"):
        input_text = "Technological advancements have revolutionized contemporary communication methodologies, facilitating instantaneous global connectivity through digital platforms."
        process = True

if process and input_text.strip():
    with st.spinner("Making it kid-friendly..."):
        output = simplify_text(input_text, strength)
        
        st.subheader("Simple Version")
        st.write(output)
        
        if show_details:
            show_readability(output)
        
        # Audio Feature
        audio_bytes = text_to_speech(output)
        st.audio(audio_bytes, format="audio/mp3")
        
        # Download Options
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("📥 Download Text", output)
        with col2:
            st.download_button("🔈 Download Audio", audio_bytes, file_name="output.mp3")

elif process:
    st.warning("Please enter some text first!")
