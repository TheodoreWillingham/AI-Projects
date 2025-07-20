import streamlit as st  # type: ignore   || for creating web app integrated with AI
import PyPDF2 # type: ignore || for reading PDF
import io
import os
from openai import OpenAI # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv() #change back to load_dotenv


# created the overall configuration of the main page name = AI Resume Critiquer
st.set_page_config(page_title="AI Resume Critiquer", page_icon="📃", layout="centered")

st.title("AI Resume Critiquer") #title text
st.markdown("Upload your resume and get AI-powered feedback tailored to your needs!") #markdown text

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # gets the open AI key from the enviroment

#this is not an AI agent but we are just utilizing open ai's LLM to critique the resumue

#Input Fields
#when any of these inputs are changed. The whole python script is reran with the values being stored in the state of the page
uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter your target Job Role (Optional)")
analyze = st.button("Analyze Resume")

#Function
def extract_text_from_pdf(pdf):
    pdf_reader = PyPDF2.PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text



def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        #Reads the uploaded file and changes it into Bytes so PyPDF2 can read it
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8") #if not a PDF just read code as utf-8

# def extract_text_from_file(uploaded_file):
#     if uploaded_file.type == "application/pdf":
#         return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
#     return uploaded_file.read().decode("utf-8")

if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file) 
        
        if not file_content.strip():
            st.error("File does not have any content...")
            st.stop()
        
        prompt = f"""Please analyze this resume and rpovide constructive feedback.
        
        Focus on the following aspects:
        1. Content clarity and impact
        2. Skills presentation
        3. Experience descriptions
        4. Specific improvements for {job_role if job_role else 'general job applications'}
        
        Resume content:
        {file_content}
        
        please provide your analysis in a clear, structured format with specific recommendations."""
    
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [
                #LLM does not reply to system message but gets context from it. You tell it what it's supposed to do
                {"role": "system", "content": "You are an expert resume reviewer with years of experience in HR and recruitment."},
                #This where we give it the prompt to respond to
                {"role": "user", "content": prompt}
            ],
            temperature = 0.7,
            max_tokens = 1000 
        )
        
        st.markdown("### Analysis Results")
        #gpt can send multiple responses this just says display the message of the first response
        st.markdown(response.choices[0].message.content)
    except Exception as e:
        st.error(f"An Error has occured: {str(e)}")    
    
    
        
        

