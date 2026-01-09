from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from google import genai
from google.genai import types
import os
load_dotenv()


def reply(query:str):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# vector embedding
    embedding_model= GoogleGenerativeAIEmbeddings(
      model="gemini-embedding-001",
)

    vector_db = QdrantVectorStore.from_existing_collection(
    url = "http://localhost:6333",
    collection_name="company",
    embedding=embedding_model
)
    search_results= vector_db.similarity_search(
    query=query,
    k=8
)
    contexts = []

    for result in search_results:
        contexts.append(
        f"""
Page Content:
{result.page_content}

Page Number: {result.metadata.get('page_label')}
Source File: {result.metadata.get('source')}
"""
    )

    context = "\n\n---\n\n".join(contexts)
    SYSTEMPROMPT = f"""
You are a PDF Question Answering AI.

STRICT RULES:
- You MUST answer ONLY from the provided context.
- If the answer is not present, say: "The information is not available in the provided document."
- ALWAYS mention the page number in your answer.
- Do NOT use external knowledge.
- Do NOT hallucinate.

Context:
{context}
"""
    response = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    contents=[query],
     config=types.GenerateContentConfig(
        system_instruction=SYSTEMPROMPT),
)
    return response.text
