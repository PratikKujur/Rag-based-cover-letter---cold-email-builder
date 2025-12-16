import streamlit as st
import os
from main import LLMResponseGenerator
import json
import requests

st.title("Cover Letter/ Cold Email Generator")

st.file_uploader("Upload your Resume (PDF format)", type=["pdf"], key="resume_uploader")
response_type=st.selectbox("Select the type of document to generate:", options=["Cover Letter", "Cold Email","Both"], key="doc_type")
job_description = st.text_area("Enter the Job Description for which you want to generate a cover letter/cold email:")

if st.button("Generate Cover Letter/ Cold Email", key="generate_covercold_btn"):
    if "resume_uploader" not in st.session_state or not st.session_state["resume_uploader"]:
        st.error("Please upload your resume in PDF format.")
    elif not job_description.strip():
        st.error("Please enter a job description.")
    else:
        resume_file = st.session_state["resume_uploader"]
        with open("temp_resume.pdf", "wb") as f:
            f.write(resume_file.getbuffer())

        inputs={
            "resume_path":"temp_resume.pdf",
            "response_type":response_type,
            "job_description":job_description
        }

        try:
            response = requests.post(url="http://127.0.0.1:9999/", json=inputs, timeout=60)
        except Exception as e:
            st.error(f"Failed to send request: {e}")
            if os.path.exists("temp_resume.pdf"):
                os.remove("temp_resume.pdf")
        else:
            if response.status_code != 200:
                st.error(f"Request failed: {response.status_code} - {response.text}")
            else:
                # Try to parse JSON response, fall back to plain text
                try:
                    data = response.json()
                except Exception:
                    st.text_area("Response", value=response.text, height=300)
                else:
                    # If API returns both responses
                    if isinstance(data, dict):
                        if "cover_letter_response" in data:
                            st.text_area("Generated Cover Letter:", value=data["cover_letter_response"], height=300)
                        if "cold_email_response" in data:
                            st.text_area("Generated Cold Email:", value=data["cold_email_response"], height=200)
                        # If the API returns a single-string field
                        if not ("cover_letter_response" in data or "cold_email_response" in data):
                            st.text_area("Response (JSON)", value=json.dumps(data, indent=2), height=300)
                    else:
                        st.text_area("Response", value=str(data), height=300)

            # Ensure temporary file cleanup
            if os.path.exists("temp_resume.pdf"):
                os.remove("temp_resume.pdf")
