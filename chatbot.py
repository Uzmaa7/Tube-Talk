from data_loader import *
from llm import *
from preprocessing import *
import streamlit as st
from langchain_community.vectorstores import Chroma
from prompt_template import *
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough


st.title("TubeTalk")


if "video_id" not in st.session_state:
    st.session_state.video_id = None
    st.session_state.full_transcript = None
    st.session_state.language_code = None
    st.session_state.main_chain = None
    st.session_state.vector_store = None
    st.session_state.retriever = None
    st.session_state.chat_history = [{"role" : "assistant", "content" : "Hello! I'm TubeTalk, your AI assistant. Please share a YouTube URL to get started."}]

for msg in st.session_state.chat_history:
    if(msg["role"] == "assistant"):
        with st.chat_message('assistant'):
            st.markdown(msg["content"])
    elif (msg["role"] == "user"):
        with st.chat_message('user'):
            st.markdown(msg["content"])


user_input = st.chat_input("Enter a valid url")

if user_input:
    video_id = get_youtube_id(user_input)

    st.session_state.chat_history.append({"role" : "user", "content" : user_input})
    with st.chat_message('user'):
        st.markdown(user_input)
    
    if video_id != None and video_id != st.session_state.video_id:

        try:
            full_transcript, language_code = get_transcript(video_id)
            st.session_state.full_transcript = full_transcript
            st.session_state.language_code = language_code

            chunks = text_splitter(full_transcript)

            vector_store = Chroma.from_documents(chunks, embedding_model)
            st.session_state.vector_store = vector_store

            retriever = vector_store.as_retriever(search_type = "similarity" , search_kwargs ={"k" : 4})
            st.session_state.retriever = retriever

            # query = "What is Lapalace Transform"

            # retrieved_docs = retriever.invoke(query)

            # final_text = format_docs(retrieved_docs=retrieved_docs)


            parallel_chain = RunnableParallel({
                "context" : retriever | RunnableLambda(format_docs),
                "question" : RunnablePassthrough()
                
            })

            main_chain = parallel_chain | template | model | parser
            st.session_state.main_chain = main_chain

            # response = main_chain.invoke(query)
            # st.write(response)

            st.session_state.chat_history.append({"role": "assistant", "content": "Transcript fetched and processed! You can now ask questions related to the video."})

            with st.chat_message('assistant'):
                st.markdown("Transcript fetched and processed! You can now ask questions related to the video.")

        except NoTranscriptFound:
            st.write("❌ No captions found for this video.")
            
        except TranscriptsDisabled:
            st.write("❌ Captions are disabled for this video.")

    else:
        if st.session_state.main_chain == None :
            st.session_state.chat_history.append({"role" : "assistant", "content" : "Please share a valid YouTube URL with captions to get started."})
            with st.chat_message('assistant'):
                st.markdown("Please share a valid YouTube URL with captions to get started.")
        else:
            response = st.session_state.main_chain.invoke(user_input)

            st.session_state.chat_history.append({"role" : "assistant" , "content" : response})

            with st.chat_message('assistant'):
                st.markdown(response)
