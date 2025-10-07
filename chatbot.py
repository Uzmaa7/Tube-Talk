from data_loader import *
from llm import *
from preprocessing import *
import streamlit as st
from langchain_community.vectorstores import Chroma

st.title("TubeTalk")
user_input = st.chat_input("Enter a valid url")

if user_input:
    video_id = get_youtube_id(user_input)

    if video_id != None:

        try:
            full_transcript, language_code = get_transcript(video_id)

            chunks = text_splitter(full_transcript)

            vector_store = Chroma.from_documents(chunks, embedding_model)

            retriever = vector_store.as_retriever(search_type = "similarity" , search_kwargs ={"k" : 4})

            query = "What is Lapalace Transform"

            retrieved_docs = retriever.invoke(query)

            final_text = format_docs(retrieved_docs=retrieved_docs)

            st.write(final_text)

        except NoTranscriptFound:
            st.write("❌ No captions found for this video.")
            
        except TranscriptsDisabled:
            st.write("❌ Captions are disabled for this video.")

    else:
        st.write("Enter a valid url")