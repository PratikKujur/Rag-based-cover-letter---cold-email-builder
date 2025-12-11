# RAG-Based Cover Letter & Cold Email Builder

An intelligent application that generates personalized cover letters and cold emails using Retrieval-Augmented Generation (RAG) technology. This tool analyzes your resume and job descriptions to create tailored, compelling application documents powered by Google's Gemini AI.

## Features

- **AI-Powered Document Generation**: Uses Google Gemini 2.5 Flash to generate contextual, compelling cover letters and cold emails
- **RAG Pipeline**: Implements Retrieval-Augmented Generation using:
  - ChromaDB for vector storage
  - Sentence Transformers for embeddings
  - FAISS for semantic search
- **Resume Analysis**: Automatically extracts and indexes relevant information from your PDF resume
- **Job Description Matching**: Matches your qualifications to specific job requirements
- **Multiple Output Types**: Generate cover letters, cold emails, or both
- **User-Friendly Interface**: Built with Streamlit for easy interaction
- **Retry & Timeout Handling**: Robust error handling with automatic retries for API resilience

## Tech Stack

- **Frontend**: Streamlit
- **LLM**: Google Gemini API (gemini-2.5-flash)
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Search**: FAISS
- **Document Processing**: PyPDF, LangChain
- **Language**: Python 3.11+

## Installation

### Prerequisites
- Python 3.11 or higher
- Google Gemini API Key

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd Rag-based-cover-letter---cold-email-builder
```

2. **Create a virtual environment** (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

## Usage

### Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### How to Use

1. **Upload Resume**: Click the file uploader and select your PDF resume
2. **Select Document Type**: Choose between:
   - Cover Letter
   - Cold Email
   - Both
3. **Enter Job Description**: Paste the job description or requirements
4. **Generate**: Click the "Generate Cover Letter / Cold Email" button
5. **Review & Copy**: The generated document will appear below for review

## Project Structure

```
├── app.py                      # Streamlit UI application
├── main.py                     # Core LLM response generator
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Project configuration
├── README.md                  # This file
├── src/
│   ├── embeddingsGenerator.py # Embedding generation using Sentence Transformers
│   ├── Retrive.py            # RAG pipeline for document retrieval
│   ├── vectorstore.py         # ChromaDB vector store management
│   └── utils.py              # PDF processing and text chunking utilities
├── data/                      # Sample data directory
├── experiments/               # Jupyter notebooks for experimentation
│   └── exp.ipynb
└── vectorstore/              # Persistent vector database storage
```

## How It Works

### RAG Pipeline

1. **Resume Processing**: Your PDF resume is loaded and processed
2. **Text Chunking**: Content is split into manageable chunks using RecursiveCharacterTextSplitter
3. **Embedding Generation**: Chunks are converted to embeddings using Sentence Transformers
4. **Vector Storage**: Embeddings are stored in ChromaDB for fast retrieval
5. **Query Retrieval**: When you provide a job description, relevant resume sections are retrieved
6. **Context Augmentation**: Retrieved context is combined with the job description
7. **Content Generation**: Google Gemini generates a personalized cover letter/email using the context

### Key Components

- **LLMResponseGenerator**: Orchestrates the entire pipeline from resume processing to response generation
- **embeddingsGenerator**: Creates vector embeddings from text chunks
- **Ragpipeline**: Retrieves relevant resume content based on job description queries
- **vectorStore**: Manages ChromaDB operations for storing and querying embeddings
- **utils.py**: Handles PDF extraction and text chunking

## Error Handling

The application includes robust error handling:
- **Timeout Protection**: 10-second timeout on API calls
- **Retry Logic**: Automatic retries (up to 3 attempts) for server overload errors (503)
- **Resume Validation**: Checks for empty resumes before processing
- **Input Validation**: Ensures job description is provided before generation

## Configuration

### Customizable Parameters

In `src/utils.py`:
- `chunk_size`: Text chunk size (default: 1000)
- `chunk_overlap`: Overlap between chunks (default: 200)

In `src/Retrive.py`:
- `top_k`: Number of document chunks to retrieve (default: 3)

In `main.py`:
- Model: Currently set to `gemini-2.5-flash`
- Timeout: 10 seconds
- Max retries: 3

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Your Google Gemini API key |

## Dependencies

Key packages:
- `google-genai`: Google Gemini API client
- `streamlit`: Web UI framework
- `chromadb`: Vector database
- `sentence-transformers`: Embedding generation
- `faiss-cpu`: Vector similarity search
- `langchain`: Document processing and text splitting
- `pypdf`: PDF parsing

See `requirements.txt` for the complete list.

## Troubleshooting

### "ValueError: Expected Embeddings to be non-empty list"
- **Cause**: Resume file not being read properly
- **Solution**: Ensure the PDF is valid and contains text content

### "503 UNAVAILABLE" Error
- **Cause**: Google Gemini API is overloaded
- **Solution**: The application automatically retries up to 3 times. If it persists, wait a moment and try again.

### "GEMINI_API_KEY not found"
- **Cause**: Environment variable not set
- **Solution**: Create a `.env` file with your API key

## Future Enhancements

- Support for multiple resume formats (DOCX, TXT)
- Customizable prompt templates
- Document history and comparison
- Batch processing for multiple job descriptions
- Integration with job platforms (LinkedIn, Indeed)
- Resume optimization suggestions

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please open an issue on the repository.