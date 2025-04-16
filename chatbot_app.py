# chatbot_app.py

import streamlit as st
import pandas as pd
from catboost import CatBoostClassifier

# Load pre-trained model
model = CatBoostClassifier()
model.load_model(r"C:\Users\elkha999\model\teststep_selector.cbm")

# Chatbot title
st.title("🤖 Chaimaa_GPT - Smart Teststep Assistant")

# Use Streamlit's session state to store chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Upload CSV section
st.subheader("📂 Upload Your Teststep CSV")
uploaded_file = st.file_uploader("Upload a CSV with 'Teststep Number' column", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if 'Teststep Number' in df.columns:
        st.success("✅ File uploaded and recognized!")

        # Prediction
        X = df[['Teststep Number']]
        df['prediction'] = model.predict(X)
        df['prediction'] = df['prediction'].map({0: 'keep', 1: 'remove'})

        st.write("📊 Prediction Results:")
        st.dataframe(df[['Teststep Number', 'prediction']])

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Results", data=csv, file_name="prediction_results.csv", mime='text/csv')
    else:
        st.error("⚠️ Your CSV must include a column named 'Teststep Number'.")

# --- Chatbot Section ---
st.subheader("💬 Chat with Chaimaa_GPT")

# User input
user_input = st.text_input("Type your question or instruction here...")

# Bot response logic
def get_bot_response(message):
    message = message.lower()
    if "hello" in message or "hi" in message:
        return "Hello 👋! You can upload a CSV to get predictions. How can I assist you today?"
    elif "predict" in message:
        return "Please upload a CSV file above. I’ll process it and give you a list of steps to keep or remove."
    elif "thank" in message:
        return "You're welcome! 😊"
    else:
        return "I'm still learning! Ask me anything about your test protocol or predictions."

# When user sends a message
if user_input:
    # Add to chat history
    st.session_state.chat_history.append(("You", user_input))
    bot_reply = get_bot_response(user_input)
    st.session_state.chat_history.append(("Chaimaa_GPT", bot_reply))

# Display chat history
for sender, message in st.session_state.chat_history:
    with st.chat_message(sender):
        st.markdown(message)
