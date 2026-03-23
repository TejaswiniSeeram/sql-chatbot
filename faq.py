import os
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

COLLECTION_NAME = "musicstore_faqs"  # 
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

chroma_client = chromadb.Client()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ingest_faq_data(path):
    # Delete collection if it already exists so we always start fresh
    existing = [c.name for c in chroma_client.list_collections()]
    if COLLECTION_NAME in existing:
        chroma_client.delete_collection(COLLECTION_NAME)
    
    collection = chroma_client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef
    )
    df = pd.read_csv(path)
    questions = df["question"].tolist()
    answers = df["answer"].tolist()
    ids = [f"id_{i}" for i in range(len(questions))]
    metadata = [{"answer": ans} for ans in answers]
    collection.add(
        documents=questions,
        metadatas=metadata,
        ids=ids
    )
    print(f"Ingested {len(questions)} FAQs into ChromaDB")

def get_relevant_qa(query):
    collection = chroma_client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=ef
    )
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    return results


def faq_chain(query):
    results = get_relevant_qa(query)
    context = " ".join([r.get("answer") for r in results["metadatas"][0]])

    prompt = f"""You are a helpful customer support assistant for an online bookstore.
Answer the user's question using ONLY the context below.
If the answer is not in the context, say "I don't have that information, please contact support."
Do not make up any details.

# TODO: update the store description above to match your project

CONTEXT: {context}

QUESTION: {query}
"""
    response = groq_client.chat.completions.create(
        model=os.getenv("GROQ_MODEL"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()
