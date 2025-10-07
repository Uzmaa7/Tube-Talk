from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint, HuggingFaceEndpointEmbeddings
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser



load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id =  "openai/gpt-oss-20b",
    task = "text-generation"
)

model = ChatHuggingFace(llm=llm)

embedding_model = HuggingFaceEndpointEmbeddings(model ='sentence-transformers/all-MiniLM-L6-v2')

parser = StrOutputParser()

# result = model.invoke("what is the time")
# print(result.content)
