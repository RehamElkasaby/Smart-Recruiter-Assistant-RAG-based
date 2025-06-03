from typing import List
import pdfplumber
from docx import Document
from langchain.schema import Document as LangDocument
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

def read_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            # Improved PDF extraction
            text += page.extract_text(x_tolerance=1, y_tolerance=1) + "\n"
    return text

def read_docs(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def load_documents(file_path): 
    if file_path.endswith('.pdf'):
        text = read_pdf(file_path)
    elif file_path.endswith('.docx'):
        text = read_docs(file_path)
    else:
        with open(file_path, 'r') as f:
            text = f.read()

    return LangDocument(
        page_content=text,
        metadata={"source": os.path.basename(file_path), "document_type": "full_cv"}
    )

def split_documents(doc): 
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    # Create splits with proper metadata
    splits = text_splitter.split_documents([doc])
    cv_name = doc.metadata["source"]
    
    for split in splits:
        split.metadata = {
            "source": cv_name,
            "is_section": True,
            "full_doc_reference": cv_name,
            "document_type": "cv_section"
        }
    return splits

def process_uploaded_files(file_paths):
    all_chunks = []
    for file_path in file_paths:
        full_doc = load_documents(file_path)
        chunks = split_documents(full_doc)
        all_chunks.extend(chunks)
    return all_chunks