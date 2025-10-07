from data_loader import *
from llm import *

import streamlit as st

st.title("TubeTalk")
user_input = st.chat_input("Enter a valid url")

if user_input:
    video_id = get_youtube_id(user_input)

    if video_id != None:

        try:
            full_transcript, language_code = get_transcript(video_id)
            st.write(full_transcript, language_code)

        except NoTranscriptFound:
            st.write("❌ No captions found for this video.")
            
        except TranscriptsDisabled:
            st.write("❌ Captions are disabled for this video.")

    else:
        st.write("Enter a valid url")