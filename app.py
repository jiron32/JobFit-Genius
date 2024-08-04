import streamlit
from openai import OpenAI
import os

# Title and description 
streamlit.title("JobFit Genius🪼")
streamlit.markdown("This app evaluates how well your resume matches a job description. Simply upload your resume, paste the job description, and click the 'Compare' button to see your results.")

#  OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


# Function to compare resume to job description
def compare_resume_to_job_description(resume_text, job_description_text):  
    prompt = f"""Given the following resume and job description, identify the skills and qualifications from both.
    Then, compare them to determine any skill gaps and estimate the individual's qualification level, providing a percentage. 
    Resume: {resume_text}
    Job Description: {job_description_text}
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Function to generate text using OpenAI
def generate_text(text):
    prompt = f"{text}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Get user input for resume and job description
resume_uploader = streamlit.file_uploader("Upload your resume")
job_description_text = streamlit.text_area("Paste job description: ")

# Compare resume to job description
if streamlit.button('Compare'):
    if api_key and resume_uploader and job_description_text:
        with streamlit.spinner('Comparing...'):
            result = compare_resume_to_job_description(resume_uploader, job_description_text)
            streamlit.write(result)
    else:
        streamlit.error("Please enter your API key, resume, and job description.")

