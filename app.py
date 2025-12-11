import streamlit as st
import os
from main import LLMResponseGenerator

st.title("Cover Letter/ Cold Email Generator")

st.file_uploader("Upload your Resume (PDF format)", type=["pdf"], key="resume_uploader")
st.selectbox("Select the type of document to generate:", options=["Cover Letter", "Cold Email","Both"], key="doc_type")
job_description = st.text_area("Enter the Job Description for which you want to generate a cover letter/cold email:")


if st.button("Generate Cover Letter/ Cold Email"):
    if "resume_uploader" not in st.session_state or not st.session_state["resume_uploader"]:
        st.error("Please upload your resume in PDF format.")
    elif not job_description.strip():
        st.error("Please enter a job description.")
    else:
        resume_file = st.session_state["resume_uploader"]
        with open("temp_resume.pdf", "wb") as f:
            f.write(resume_file.getbuffer())
        
        

        if st.session_state["doc_type"] == "Cover Letter":
            generator = LLMResponseGenerator(resume_pdf_path="temp_resume.pdf",response_type="cover letter")
            response_type="cover letter"
            cover_letter = generator.generate_response(query=f"""Generate a short and crisp {response_type} for this following job description-->Job Description:{job_description}""")
            st.text_area("Generated Cover Letter:", value=cover_letter, height=300)
        elif st.session_state["doc_type"] == "Cold Email":
            generator = LLMResponseGenerator(resume_pdf_path="temp_resume.pdf",response_type="cold email")
            response_type="cold email"
            cold_email = generator.generate_response(query=f"""Generate a short and crisp {response_type} for this following job description-->Job Description:{job_description}""")
            st.text_area("Generated Cold Email:", value=cold_email, height=200)
        else:
            generator = LLMResponseGenerator(resume_pdf_path="temp_resume.pdf",response_type="cover letter")
            cover_letter=generator.generate_response(query=f"""Generate a short and crisp Cover letter for this following job description-->Job Description:{job_description}""")
            st.text_area("Generated Cover Letter:", value=cover_letter, height=300)
            generator = LLMResponseGenerator(resume_pdf_path="temp_resume.pdf",response_type="cold email")
            cold_email=generator.generate_response(query=f"""Generate a short and crisp cold email for this following job description-->Job Description:{job_description}""")
            st.text_area("Generated Cold Email:", value=cold_email, height=200)
        # Clean up temporary file
        os.remove("temp_resume.pdf")