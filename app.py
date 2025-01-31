import streamlit as st
import re

# Function to simplify text
def simplify_text(text):
    # Replace complex words with simpler ones
    word_replacements = {
        "utilize": "use",
        "demonstrate": "show",
        "comprehend": "understand",
        "facilitate": "help",
        "terminate": "end"
    }
    
    # Replace complex words
    for word, replacement in word_replacements.items():
        text = re.sub(rf"\b{word}\b", replacement, text, flags=re.IGNORECASE)
    
    # Break down long sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    simplified_sentences = []
    for sentence in sentences:
        if len(sentence.split()) > 15:  # If sentence is too long
            parts = re.split(r',|;', sentence)
            simplified_sentences.extend(parts)
        else:
            simplified_sentences.append(sentence)
    
    # Join sentences back together
    simplified_text = " ".join(simplified_sentences)
    
    # Add conversational tone
    simplified_text = simplified_text.replace("It is", "It's").replace("You are", "You're")
    
    return simplified_text

# Streamlit App
st.title("Text Simplifier")

# Input text area
input_text = st.text_area("Enter your text here:", height=150)

# Simplify button
if st.button("Simplify"):
    if input_text.strip() == "":
        st.warning("Please enter some text to simplify.")
    else:
        # Simplify the text
        simplified_text = simplify_text(input_text)
        
        # Display the simplified text
        st.subheader("Simplified Text:")
        st.write(simplified_text)
