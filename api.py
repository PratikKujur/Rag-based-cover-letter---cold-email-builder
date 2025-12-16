from fastapi import FastAPI
from pydantic import BaseModel
from main import LLMResponseGenerator

class CoverLetterAPI(BaseModel):
    resume_path:str
    response_type:str
    job_description:str

api=FastAPI()

@api.post("/")
def generate_response(user_input:CoverLetterAPI):
    gererate_contex=LLMResponseGenerator(resume_pdf_path=user_input.resume_path,response_type=user_input.response_type)
    
    if not user_input.response_type:
        return "Not able to fetch response"
    elif user_input.response_type=="Cold Email":
        return gererate_contex.generate_response(query=f"""Generate a short and crisp {user_input.response_type} for this following job description-->Job Description:{user_input.job_description} in 250 words""")
    elif user_input.response_type=="Cover Letter":
        return gererate_contex.generate_response(query=f"""Generate a short and crisp {user_input.response_type} for this following job description-->Job Description:{user_input.job_description}""")
    else:
        return {
            'cover_letter_response':gererate_contex.generate_response(query=f"""Generate a short and crisp {user_input.response_type} for this following job description-->Job Description:{user_input.job_description}"""),
            'cold_email_response':gererate_contex.generate_response(query=f"""Generate a short and crisp {user_input.response_type} for this following job description-->Job Description:{user_input.job_description} in 250 words""")
        }
