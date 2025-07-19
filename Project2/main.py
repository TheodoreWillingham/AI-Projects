import streamlit as st #for creating web app integrated with AI
import PyPDF2 #for reading PDF
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() #change back to load_dotenv


# created the overall configuration of the main page name = AI Resume Critiquer
st.set_page_config(page_title="AI Resume Critiquer", page_icon="🗒️", layout="centered")

st.title("AI Resume Cririquer") #title text
st.markdown("Upload your resume and get AI-powered feedback tailored to your needs!") #markdown text

