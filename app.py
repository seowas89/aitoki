import streamlit as st
import re
import random

# Function to simplify text
def simplify_text(text):
    # Replace complex words with simpler ones
    word_replacements = {
        "utilize": ["use", "make use of", "take advantage of"],
        "demonstrate": ["show", "prove", "illustrate"],
        "comprehend": ["understand", "get", "grasp"],
        "facilitate": ["help", "assist", "make easier"],
        "terminate": ["end", "stop", "finish"]
    }
    
    # Replace complex words with randomized options
    for word, replacements in word_replacements.items():
        text = re.sub(rf"\b{word}\b", random.choice(replacements), text, flags=re.IGNORECASE)
    
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
    
    # Add conversational tone and variability
    simplified_text = simplified_text.replace("It is", random.choice(["It's", "This is", "That is"]))
    simplified_text = simplified_text.replace("You are", random.choice(["You're", "You are", "You happen to be"]))
    
    # Add filler words and contractions for natural flow
    simplified_text = simplified_text.replace("very", random.choice(["super", "really", "pretty"]))
    simplified_text = simplified_text.replace("important", random.choice(["key", "crucial", "vital", "a big deal"]))
    
    return simplified_text

# Streamlit App
st.title("Human-Like Text Simplifier")

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
