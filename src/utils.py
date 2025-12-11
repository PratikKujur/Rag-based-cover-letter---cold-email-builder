from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_pdf_or_text_files(resume_pdf_path: str):
        all_docs=[]
        resume_pdf_path=Path(resume_pdf_path)

        # Handle both file and directory paths
        if resume_pdf_path.is_file() and resume_pdf_path.suffix == '.pdf':
            # Single PDF file case
            resume_pdf_files = [resume_pdf_path]
        else:
            # Directory case - glob for all PDFs
            resume_pdf_files = list(resume_pdf_path.glob("**/*.pdf"))

        print(f"Found {len(resume_pdf_files)} PDF files to process")

        for pdf in resume_pdf_files:
            try:
                loader=PyPDFLoader(str(pdf))
                docs=loader.load()
                all_docs.extend(docs)

            except Exception as e:
                print(f"got an error--> {e}")

        return all_docs
    
def generate_chunks(docs, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
        separators=["\n\n", "\n", " ", ""],
    )

    if not docs:
        return []

    try:
        if hasattr(docs[0], "page_content"):
            doc_chunks = text_splitter.split_documents(docs)
        else:
            texts = [str(d) for d in docs]
            doc_chunks = text_splitter.create_documents(texts)
    except Exception:
        texts = [d.page_content if hasattr(d, "page_content") else str(d) for d in docs]
        doc_chunks = text_splitter.create_documents(texts)

    return doc_chunks