from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import os
load_dotenv()

def process(x:str):

    pdf_path = Path(__file__).parent / f"uploads/{x}"
    loader = PyPDFLoader(pdf_path)

    docs = loader.load()

## split docs into smaller chunks

    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 400
)

    chunks = text_splitter.split_documents(documents=docs)
    embedding_model= GoogleGenerativeAIEmbeddings(
        api_key=os.getenv('GEMINI_API_KEY'),
      model="gemini-embedding-001",
)

    vector_store = QdrantVectorStore.from_documents(    
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name = "company"
)
    return [{"content": chunk.page_content} for chunk in chunks]