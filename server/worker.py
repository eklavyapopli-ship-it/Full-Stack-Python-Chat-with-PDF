from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
load_dotenv()

def process(x:str):


    loader = PyPDFLoader(file_path=f'server/uploads/{x}')
    docs = loader.load()

## split docs into smaller chunks

    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 400
)

    chunks = text_splitter.split_documents(documents=docs)
    return [{"content": chunk.page_content} for chunk in chunks]