import streamlit as st
import spacy
from nltk.corpus import wordnet
import random
import openai
import requests  # For QuillBot API

# Initialize NLP
nlp = spacy.load("en_core_web_sm")

# --- App Config ---
st.set_page_config(page_title="Kid-Friendly Text Simplifier", page_icon="🧒")
st.title("🧒 Text Simplifier for Kids")
st.markdown("""
_Converts complex text into easy-to-read language for 9-year-olds!_
""")

# --- Core Functions ---
def simplify_text(text):
    """Main processing pipeline"""
    # Step 1: Preprocess
    doc = nlp(text)
    
    # Step 2: Rule-based simplification
    simplified = []
    for sent in doc.sents:
        simplified_sent = replace_complex_words(sent.text)
        simplified_sent = shorten_sentence(simplified_sent)
        simplified.append(simplified_sent)
    
    # Step 3: LLM Enhancement
    llm_output = call_llm_api(" ".join(simplified))
    
    # Step 4: Humanization
    final_output = humanize_text(llm_output)
    
    # Step 5: Anti-AI processing
    return anti_ai_detection(final_output)

def replace_complex_words(sentence):
    replacements = {
        "utilize": "use", "approximately": "about", 
        "terminate": "end", "acquire": "get",
        "synthesize": "make", "consequently": "so"
    }
    for word, replacement in replacements.items():
        sentence = sentence.replace(word, replacement)
    return sentence

def shorten_sentence(sentence):
    if len(sentence.split()) > 15:
        return ". ".join([s.strip() for s in sentence.split(", ")])
    return sentence

def humanize_text(text):
    # Add conversational elements
    human_touches = ["Wow, ", "You know, ", "Hey! ", "Cool! "]
    if random.random() < 0.3:
        text = random.choice(human_touches) + text.lower()
    
    # Add emojis
    emojis = ["🌞", "✨", "🚀", "🎉", "🤯"]
    if random.random() < 0.2:
        text = text + " " + random.choice(emojis)
    
    return text

def anti_ai_detection(text):
    # Simple paraphrasing
    try:
        return quillbot_paraphrase(text)
    except:
        return text  # Fallback

def quillbot_paraphrase(text):
    # Requires QuillBot API key
    response = requests.post(
        "https://api.quillbot.com/v1/paraphrase",
        headers={"Authorization": f"Bearer {st.secrets['QUILLBOT_KEY']}"},
        json={"text": text, "strength": 3}
    )
    return response.json()['data']['paraphrased']

def call_llm_api(text):
    openai.api_key = st.secrets["OPENAI_KEY"]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": """Rewrite this for a 9-year-old. Rules:
            - 3rd grade vocabulary
            - Max 12-word sentences
            - Use jokes/questions
            - Sound like a fun aunt/uncle"""
        }, {
            "role": "user",
            "content": text
        }]
    )
    return response.choices[0].message.content

# --- UI Components ---
input_text = st.text_area("Paste your complex text here:", height=150)
col1, col2 = st.columns([1, 3])
with col1:
    if st.button("✨ Simplify!"):
        with st.spinner("Making it kid-friendly..."):
            try:
                output = simplify_text(input_text)
                st.session_state.output = output
            except Exception as e:
                st.error(f"Oops! Error: {str(e)}")

with col2:
    if st.button("🔄 Reset"):
        st.session_state.output = ""
        input_text = ""

if 'output' in st.session_state:
    st.subheader("Simplified Text")
    st.write(st.session_state.output)
    st.download_button("📥 Download", st.session_state.output)

# --- Optional Sidebar ---
with st.sidebar:
    st.markdown("## Settings ⚙️")
    emoji_level = st.slider("🎉 Fun Level", 1, 5, 3)
    complexity = st.selectbox("Reading Level", ["Grade 3", "Grade 4"])
