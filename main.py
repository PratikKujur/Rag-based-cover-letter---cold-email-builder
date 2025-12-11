import os
from google import genai
from dotenv import load_dotenv
from pathlib import Path
from src.utils import process_pdf_or_text_files, generate_chunks
from src.Retrive import Ragpipeline
from src.vectorstore import vectorStore
from src.embeddingsGenerator import embeddingsGenerator

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

class LLMResponseGenerator:
    def __init__(self, resume_pdf_path):
        self.client = genai.Client(api_key=api_key)
        self.resume_pdf_path = resume_pdf_path

    def generate_response(self, query: str) -> str:
        # Gather docs and create chunks
        all_docs = process_pdf_or_text_files(self.resume_pdf_path)
        doc_chunks = generate_chunks(all_docs)

        # Generate embeddings for chunks
        embedder = embeddingsGenerator()
        embeddings = embedder.generate_embeddings(doc_chunks)

        # Persist embeddings to vector store
        vector_store = vectorStore(dir="D:/Projects/Rag-based-cover-letter---cold-email-builder/vectorstore")
        vector_store.add_embeddings(doc_chunks=doc_chunks, embeddings=embeddings)

        # Build a retrieval pipeline and query it
        response_pipeline = Ragpipeline(vector_store, embedder)
        retrieved = response_pipeline.query(query_text=query, top_k=3)

        # retrieved is list of (doc_text, score); join doc_texts for context
        context= "\n\n".join([doc for doc, _ in retrieved])
        # print("context--->",context)

        prompt = f"Context: {context}\n\nQuestion: {query}\n\nResponce_body:Start with introducing yourself,mention recent experience, mention highest qualification and finally mention your works and skils to prove why you are the best fit for this role. in paragraph \n\n Don't: mention the from where we get to know about this job opening." 

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    
if __name__ == "__main__":
    get_cover_letter=LLMResponseGenerator(resume_pdf_path="D:/Projects/Rag-based-cover-letter---cold-email-builder/data")
    job_discription=input("Enter the job description for which you want to generate cover letter: ")
    cover_letter=get_cover_letter.generate_response(query=f"""Generate a short and crisp cover letter for this following job description-->Job Description:
{job_discription}
""")
    
    
    print("Generated Cover Letter:\n", cover_letter)