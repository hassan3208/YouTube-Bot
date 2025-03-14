import streamlit as st
import time
from gtts import gTTS
import os
import methods as M
import re


# Set up Streamlit page
st.set_page_config(page_title="Youtube Chatbot", page_icon="▶️")
st.title("Youtube Chatbot ▶️")
st.write("A simple chatbot that accepts Youtube video links.")

# Sidebar for document uploads and URL input
with st.sidebar:
    st.header("🌍 Enter YouTube URL")

    if st.button("Clear Chat History"):
        st.session_state.messages = [{"role": "assistant", "content": "Chat history cleared! Let's start again."}]
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Let's start chatting! 👇"}]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if link := st.chat_input("Paste your video link here..."):
    st.session_state.messages.append({"role": "user", "content": link})
    with st.chat_message("user"):
        st.markdown(link)

    # Progress bar for fetching transcript
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(1, 101, 10):  # Simulating progress
        time.sleep(0.1)
        progress_bar.progress(i)
        status_text.text(f"Fetching transcript... {i}%")
    
    transcript = M.get_transcript_vedio(link)
    progress_bar.empty()  # Remove progress bar after completion
    status_text.text("Transcript fetched! ✅")

    # Sidebar shows the original transcript
    st.sidebar.write(f"📜 **Original Transcript:** {transcript}")

    # Progress bar for bot response
    progress_bar = st.progress(0)
    status_text.text("Generating response...")

    bot_response = M.get_bot_response(transcript)
    bot_response = clean_text = re.sub(r"<think>.*?</think>\s*", "", bot_response, flags=re.DOTALL)
    
    for i in range(1, 101, 10):
        time.sleep(0.1)
        progress_bar.progress(i)
    
    progress_bar.empty()  # Remove progress bar
    status_text.text("Response ready! ✅")

    # Display bot response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for word in bot_response.split():
            full_response += word + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Convert response to speech and play audio
    tts = gTTS(text=full_response, lang='en')
    audio_path = "response.mp3"
    tts.save(audio_path)
    st.audio(audio_path, format="audio/mp3")
    os.remove(audio_path)
