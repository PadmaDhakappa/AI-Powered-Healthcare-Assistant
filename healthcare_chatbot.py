import streamlit as st
import json

# Load the knowledge base from a JSON file
def load_knowledge_base(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Function to find a response based on user input
def find_response(user_input, knowledge_base):
    user_input = user_input.lower()
    for symptom in knowledge_base["symptoms"]:
        for keyword in symptom["keywords"]:
            if keyword in user_input:
                return symptom["response"]
    return knowledge_base["fallback_response"]

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
                response = find_response(user_input, knowledge_base)
                st.write("**Healthcare Assistant:**", response)
        else:
            st.warning("Please enter a query.")

if __name__ == "__main__":
    main()