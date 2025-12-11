import os
import time
from google import genai
from google.api_core import exceptions
from dotenv import load_dotenv
from pathlib import Path
from src.utils import process_pdf_or_text_files, generate_chunks
from src.Retrive import Ragpipeline
from src.vectorstore import vectorStore
from src.embeddingsGenerator import embeddingsGenerator

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

class LLMResponseGenerator:
    def __init__(self, resume_pdf_path,response_type):
        self.client = genai.Client(api_key=api_key)
        self.resume_pdf_path = resume_pdf_path
        self.response_type = response_type

    def generate_response(self, query: str) -> str:
        # Gather docs and create chunks
        all_docs = process_pdf_or_text_files(self.resume_pdf_path)
        doc_chunks = generate_chunks(all_docs)

        # Generate embeddings for chunks
        embedder = embeddingsGenerator()
        embeddings = embedder.generate_embeddings(doc_chunks)

        # Persist embeddings to vector store
        vector_store = vectorStore(
            dir="D:/Projects/Rag-based-cover-letter---cold-email-builder/vectorstore"
        )
        vector_store.add_embeddings(doc_chunks=doc_chunks, embeddings=embeddings)

        # Build a retrieval pipeline and query it
        response_pipeline = Ragpipeline(vector_store, embedder)
        retrieved = response_pipeline.query(query_text=query, top_k=3)

        # retrieved is list of (doc_text, score); join doc_texts for context
        context = "\n\n".join([doc for doc, _ in retrieved])
        # print("context--->",context)

        prompt = f"""
        Context: {context}

        Question: {query}

        Response_body:
        Write a concise, compelling {self.response_type} in one paragraph. 
        Start by introducing yourself, highlight your most recent industry experience, 
        and mention your highest qualification. Then briefly showcase relevant projects, 
        skills, and technical strengths that clearly demonstrate why you are an excellent 
        fit for this specific role.

        Do NOT mention where the job opening was found or how you came across it.
        """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text


if __name__ == "__main__":
    job_description: str = None
    response_type: str = None  # cover letter or cold email
    get_cover_letter = LLMResponseGenerator(
        resume_pdf_path="D:/Projects/Rag-based-cover-letter---cold-email-builder/data",
        response_type=None,
    )

    cover_letter = get_cover_letter.generate_response(
        query=f"""Generate a short and crisp {response_type} for this following job description-->Job Description:
{job_description}
"""
    )

    print("Generated Cover Letter:\n", cover_letter)
