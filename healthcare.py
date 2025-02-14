import streamlit as st
import json
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK data
nltk.download("punkt")
nltk.download("stopwords")

# Load the knowledge base from a JSON file
def load_knowledge_base(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Load a pre-trained Hugging Face model
chatbot = pipeline("text-generation", model="distilgpt2")

# Function to find a response based on user input
def find_response(user_input, knowledge_base):
    user_input = user_input.lower()
    for symptom in knowledge_base["symptoms"]:
        for keyword in symptom["keywords"]:
            if keyword in user_input:
                return symptom["response"]
    return None  # No match found in the knowledge base

# Function to generate a response using the LLM
def generate_llm_response(user_input):
    prompt = f"I recommend consulting a healthcare professional for a proper diagnosis and treatment."
    response = chatbot(prompt, max_length=100, num_return_sequences=1)
    return response[0]["generated_text"]

# Streamlit web app interface
def main():
    st.set_page_config(page_title="Healthcare Assistant Chatbot", page_icon="🩺", layout="centered")
    st.title("🩺 Healthcare Assistant Chatbot")

    st.write("Welcome! How can I assist you today?")
    
    # Load the knowledge base
    knowledge_base = load_knowledge_base("knowledge_base.json")

    user_input = st.text_input("Enter your health-related query:", "")

    if st.button("Submit"):
        if user_input:
            with st.spinner("Processing..."):  # Loading spinner
                st.write("**User:**", user_input)
                
                # Step 1: Check the knowledge base for a predefined response
                response = find_response(user_input, knowledge_base)
                
                # Step 2: If no match is found, use the LLM to generate a response
                if not response:
                    response = generate_llm_response(user_input)
                
                st.write("**Healthcare Assistant:**", response)
        else:
            st.warning("Please enter a query.")

if __name__ == "__main__":
    main()