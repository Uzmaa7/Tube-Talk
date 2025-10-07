from langchain.text_splitter import RecursiveCharacterTextSplitter

def text_splitter(full_transcript):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap = 200)
    chunks = splitter.create_documents([full_transcript])
    return chunks

def format_docs(retrieved_docs):
    return "\n".join(doc.page_content for doc in retrieved_docs)
