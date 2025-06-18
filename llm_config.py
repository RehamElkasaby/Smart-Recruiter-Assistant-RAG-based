#imports
import os
import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings


try:
    from dotenv import load_dotenv
    load_dotenv()

    MODEL_NAME = os.environ.get("GOOGLE_GENAI_MODEL", "gemini-2.0-flash")
except ImportError:
    print("Warning: python-dotenv not installed. Ensure API key is set")
    MODEL_NAME = "gemini-2.0-flash"


#Load the models
GOOGLE_API_KEY= os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")


#llm = GoogleGenerativeAI("models/gemini-2.0-flash",google_api_key=GOOGLE_API_KEY)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",google_api_key=GOOGLE_API_KEY,temperature=0)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=GOOGLE_API_KEY)

