import os


try:
    from dotenv import load_dotenv
    load_dotenv()

    MODEL_NAME = os.environ.get("GOOGLE_GENAI_MODEL", "gemini-2.0-flash")
except ImportError:
    print("Warning: python-dotenv not installed. Ensure API key is set")
    MODEL_NAME = "gemini-2.0-flash"


#imports
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import GoogleGenerativeAI

from langchain_google_genai import ChatGoogleGenerativeAI
#import google.generativeai as genai
#Load the models
GOOGLE_API_KEY= os.environ.get("GEMINI_API_KEY")
#genai.configure(api_key=GOOGLE_API_KEY)

#llm = GoogleGenerativeAI("models/gemini-2.0-flash",google_api_key=GOOGLE_API_KEY)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",google_api_key=GOOGLE_API_KEY,temperature=0)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=GOOGLE_API_KEY)

