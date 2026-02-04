import os
import re
import numpy as np
from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# 1. Load document safely
def load_document():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "hr_policy.txt")

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# 2. Split into semantic chunks
def split_chunks(text):
    """
    FIXED VERSION (IMPORTANT)

    Why?
    Your HR file has multi-line sentences.
    Line splitting breaks meaning.

    This:
    - joins lines
    - splits by sentences
    - keeps each rule complete
    """

    # join broken lines
    text = text.replace("\n", " ")

    # split by sentences
    chunks = re.split(r'\.\s+', text)

    # clean
    chunks = [c.strip() + "." for c in chunks if c.strip()]

    return chunks


# 3. Gemini embedding
def get_embedding(text):
    response = client.models.embed_content(
        model="text-embedding-004",
        contents=text
    )
    return response.embeddings[0].values


# 4. Cosine similarity
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))



# 5. Retrieve BEST chunk
def retrieve_context(query, chunks):

    query_emb = get_embedding(query)

    best_score = -1
    best_chunk = ""

    for c in chunks:
        emb = get_embedding(c)
        score = cosine_similarity(query_emb, emb)

        if score > best_score:
            best_score = score
            best_chunk = c

    return best_chunk


# 6. Final Answer (RAG)
def generate_answer(query):

    document = load_document()

    chunks = split_chunks(document)

    answer = retrieve_context(query, chunks)

    if answer:
        return answer

    return "I don't know based on the document."
