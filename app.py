import sys
#import pysqlite3
#sys.modules["sqlite3"] = pysqlite3
import pandas as pd
import os
import shutil
import streamlit as st
from PIL import Image
from streamlit_lottie import st_lottie
import requests
from process_files import process_uploaded_files
from process_query import process_query
from vector_store import vector_store_init, add_candidates
from llm_config import llm, embeddings



# Page Config
favicon = Image.open("favicon.png")
st.set_page_config(page_title="Smart Recruiter", page_icon=favicon, layout="centered")

# Load Lottie Animations
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# home_animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_t9gkkhz4.json")
home_animation  = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_z01bika0.json")
about_animation = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_jcikwtux.json")
contact_animation = load_lottie_url("https://assets1.lottiefiles.com/packages/lf20_jtbfg2nb.json")
cv_animation = load_lottie_url("https://lottie.host/2d71eafc-3a74-46e4-ba0c-c039e299795b/aqdRlRoslP.json")

##Sidebar
with st.sidebar:
    st.image("favicon.png", width=150)
    st.markdown('<div class="sidebar-title" style="text-align:center;">Menu</div>', unsafe_allow_html=True)

    ## Navigation buttons
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"
    if st.button("ℹ️ About", use_container_width=True):
        st.session_state.page = "About"
    if st.button("📬 Contact", use_container_width=True):
        st.session_state.page = "Contact"

    st.markdown("---")
    st.markdown("""
        <div style=" padding-bottom: 10px; text-align: center;font-size: 24px;font-weight: bold;font-family:Comic Sans MS">
            Made with 💙💙
        </div>
    """, unsafe_allow_html=True)
    
##Custom Sidebar Styling
st.markdown("""
    <style>
    .sidebar-title {
        font-size: 24px;
        font-weight: bold;
        font-family: Comic Sans MS;
        padding-bottom: 20px;
    }

    button {
        background-color: #ffffff;      
        color: #0000FF;          
        border: 2px solid #FF4B4B;      
        border-radius: 12px;
        font-weight: bold;
        margin-bottom: 12px;
        text-align: left;
        padding-left: 16px;
        transition: all 0.3s ease-in-out;
    }

    button:hover {
        background-color: white;       
        color: black;                   
    }

    button:focus {
        background-color: white !important; 
        color: #808080 !important;           
    }
    </style>
""", unsafe_allow_html=True)

primary_color = "#4b6cb7"  # Gradient start
secondary_color = "#182848"  # Gradient end

## Define page content
def home():
    st.markdown(f"""
        <div style='text-align: center; font-family: Comic Sans MS; margin-bottom: 0.5em;'>
            <span style='font-size: 3em;'>🤖</span>
            <span style='
                background: -webkit-linear-gradient(90deg, {primary_color}, {secondary_color});
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 2.5em; 
                font-weight: bold;
                display: inline-block;
            '>
                Welcome to Smart Recruiter
            </span>
        </div>
    """, unsafe_allow_html=True)

    # Add animation
    st_lottie(home_animation, height=300, key="home-animation")

    # Intro description
    st.markdown("""
    <div style='
        padding: 20px; 
        background-color: #f9f9f9; 
        border-radius: 12px;
        font-family: "Segoe UI", sans-serif;
        font-size: 18px;
        color: #333;
        line-height: 1.6;
        margin-top: 20px;
    '>
        <p>
            <strong>Smart Recruiter</strong> is your intelligent hiring partner 🤖. 
            Whether you're a recruiter, HR manager, or a hiring enthusiast, this AI-powered assistant helps you:
        </p>
        <ul>
            <li>🧠 Analyze CVs & extract candidate skills</li>
            <li>✅ Score candidates for job fit</li>
            <li>📝 Summarize long interview transcripts</li>
            <li>⚙️ Customize recruitment workflows with AI</li>
        </ul>
        <p>
            <em>Say goodbye to time-consuming hiring tasks, and hello to smarter decisions! 🎯</em>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Add CSS for button
    st.markdown("""
        <style>
        button[kind="primary"] {
            display: flex;
            justify-content: center;
            margin-top: 30px;
        }
        button[kind="primary"] {
            background-color: #182848;
            color: white;
            border: solid 1px black;
            padding: 14px 14px;
            font-size: 16px;
            border-radius: 12px;
            cursor: pointer;
            font-weight: bold;
            font-family: 'Segoe UI', sans-serif;
            transition: background-color 0.3s ease-in-out;
        }
        button[kind="primary"]:hover {
            background-color: #4b6cb7;
        }
        </style>
    """, unsafe_allow_html=True)

    # Display native Streamlit button inside styled container
    col1, col2, col3 = st.columns([2, 2, 2])
    with col2:
        if st.button("🚀 Start Recruiting Smarter", key="start_button",type="primary"):
            st.session_state.page = "CV Parser"

##########################################

def cv_parser():
    # Title section with gradient style
    st.markdown("""
        <div style='text-align: center; font-family: Comic Sans MS; margin-bottom: 0.5em;'>
            <span style='font-size: 3em;'>📄</span>
            <span style='
                background: -webkit-linear-gradient(90deg,{primary_color}, {secondary_color});
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 2.5em; 
                font-weight: bold;
                display: inline-block;
            '>
                CV Parser
            </span>
        </div>
    """, unsafe_allow_html=True)

    # Load Lottie animation
    st_lottie(cv_animation, height=280, key="cv-parser-animation")

    # Description box
    st.markdown("""
        <div style='
            padding: 20px; 
            background-color: #f0f8ff; 
            border-radius: 12px;
            font-family: "Segoe UI", sans-serif;
            font-size: 17px;
            color: #333;
            line-height: 1.6;
            margin-top: 20px;
        '>
            Upload candidate CVs in <strong>PDF</strong> or <strong>DOCX</strong> or <strong>TXT</strong> format and let Smart Recruiter do the heavy lifting for you 💼. 
            The assistant will analyze, extract skills, and summarize relevant information.
        </div>
    """, unsafe_allow_html=True)

    # Upload field
    uploaded_files = st.file_uploader(
        "📤 Upload one or more CV files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )
    
    user_query = st.text_input(
        "🧠 What would you like the AI to do with the uploaded CVs?",
        placeholder="e.g., Who has good experience in Time Series?"
    )

    # Display uploaded files summary
    if uploaded_files:
        file_info = []
        for file in uploaded_files:
            file_info.append({
                "File Name": file.name,
                "Size (KB)": round(len(file.getvalue()) / 1024, 2),
                "Type": os.path.splitext(file.name)[1][1:]
            })
        
        file_df = pd.DataFrame(file_info)
        st.markdown("### 📄 Uploaded Files Summary")
        st.dataframe(file_df, use_container_width=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        process_clicked = st.button("🚀 Process Query")

    # Processing logic
    if process_clicked:
        if not uploaded_files:
            st.warning("⚠️ Please upload files before processing.")
            return
            
        temp_dir = "temp_cv_files"
        os.makedirs(temp_dir, exist_ok=True)
        temp_paths = []
        
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Step 1: Save files to temporary directory
        status_text.text("💾 Saving files...")
        for i, file in enumerate(uploaded_files):
            progress = (i + 1) / len(uploaded_files)
            progress_bar.progress(progress)
            
            temp_path = os.path.join(temp_dir, file.name)
            with open(temp_path, "wb") as f:
                f.write(file.getbuffer())
            temp_paths.append(temp_path)

        # Step 2: Process files through your function
        status_text.text("🔍 Processing files with AI...")
        chunks, _ = process_uploaded_files(temp_paths)
        
        # Step 3: Initialize vector store and add candidates
        status_text.text("🧠 Initializing knowledge base...")
        vector_store = vector_store_init()
        add_candidates(vector_store, chunks)
        
        # Step 4: Process user query
        status_text.text("💬 Generating response...")
        response = process_query(user_query,llm=llm,file_paths=temp_paths)
        
        
        
        # Step 5: Clean up temporary files
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        # Step 6: Display results
        progress_bar.empty()
        status_text.success("✅ Processing complete!")
        
        # Display the response in a visually appealing way
        if user_query and user_query.lower().startswith("find"):
            st.subheader("🔍 Search Results")

            
            for item in response: # list of dict
                if isinstance(item, dict):
                    title = item.get("title", "Job Opportunity")
                    url = item.get("url", "#")
                    st.markdown(f"- [{title}]({url})")


        else:        
            st.markdown("### 🤖 AI Response")
            st.markdown(f"""
                <div style='
                    padding: 20px; 
                    background-color: #f0f8ff;
                    border-radius: 12px;
                    border-left: 5px solid #4B9CD3;
                    font-family: "Segoe UI", sans-serif;
                    font-size: 16px;
                    color: #333;
                    line-height: 1.6;
                    margin-top: 20px;
                '>
                    {response.content}
                </div>
            """, unsafe_allow_html=True)


#### about page.....
def about():
    st.markdown(f"""
        <div style='text-align: center; font-family: Comic Sans MS; margin-bottom: 0.5em;'>
            <span style='font-size: 3em;'>🔎</span>
            <span style='
                background: -webkit-linear-gradient(90deg, {primary_color}, {secondary_color});
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 2.5em; 
                font-weight: bold;
                display: inline-block;
            '>
                About Smart Recruiter
            </span>
        </div>
    """, unsafe_allow_html=True)


    st_lottie(about_animation, height=300, speed=1, reverse=False, loop=True, quality="high", key="about-lottie")

    st.markdown("""
    <style>
    .about-section {
        padding: 20px 30px;
        background-color: #f5f5f5;
        border-radius: 16px;
        font-family: 'Segoe UI', sans-serif;
        color: #333333;
        margin-bottom: 20px;
    }

    .about-heading {
        font-size: 28px;
        color: #244DA0;
        font-weight: bold;
        margin-bottom: 10px;
        font-family: Comic Sans MS;
    }

    .about-text {
        font-size: 18px;
        line-height: 1.6;
    }

    .team-footer {
        text-align: center;
        font-size: 0.9em;
        color: gray;
        margin-top: 30px;
    }

    .team-footer a {
        color: #244DA0;
        text-decoration: none;
        font-weight: 600;
    }

    </style>

    <div class="about-section">
        <div class="about-heading">What is Smart Recruiter?</div>
        <div class="about-text">
            Smart Recruiter is an intelligent recruitment assistant powered by AI, designed to streamline your hiring process and enhance candidate evaluation. 
            Whether you're screening CVs, extracting candidate skills, or summarizing interviews, Smart Recruiter makes it faster and more accurate.
        </div>
    </div>

    <div class="about-section">
        <div class="about-heading">💡 Key Features</div>
        <div class="about-text">
            <ul>
                <li>🔍 AI-based resume analysis and parsing</li>
                <li>📄 Automatic job-fit scoring</li>
                <li>📊 Summarized candidate profiles</li>
                <li>🎯 Customizable evaluation criteria</li>
            </ul>
        </div>
    </div>

    <div class="about-section">
        <div class="about-heading">🎯 Our Mission</div>
        <div class="about-text">
            To empower recruiters and HR teams with AI tools that save time, reduce bias, and help make smarter hiring decisions.
        </div>
    </div>
    """, unsafe_allow_html=True)


def contact():
    st.markdown(f"""
        <div style='text-align: center; font-family: Comic Sans MS; margin-bottom: 0.5em;'>
            <span style='font-size: 3em;'>📬</span>
            <span style='
                background: -webkit-linear-gradient(90deg, {primary_color}, {secondary_color});
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 2.5em; 
                font-weight: bold;
                display: inline-block;
            '>
                Contact Our Team
            </span>
        </div>
    """, unsafe_allow_html=True)

    st_lottie(contact_animation, height=280, key="contact")

    # Friendly intro message
    st.markdown("""
        <div style='text-align: center; font-size: 18px;font-weight:bolder; font-family: Segoe UI, sans-serif; margin-top: 10px; margin-bottom: 20px; color: #444444;'>
            We’re passionate about building smart tools with a touch of creativity and AI magic!<br>
            Get in touch, explore our work, or just say hi 👋
        </div>
    """, unsafe_allow_html=True)

    # GitHub links with icon
    st.markdown("""
        <style>
        .email-list {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 20px;
            font-family: 'Segoe UI', sans-serif;
        }

        .github-link {
            color: #333333;
            text-decoration: none;
            font-size: 1.1em;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: all 0.2s ease-in-out;
        }

        .github-link:hover {
            color: #FF4B4B;
            transform: translateX(5px);
        }

        .github-icon {
            width: 22px;
            height: 22px;
            filter: grayscale(100%);
        }

        .fun-fact {
            text-align: center;
            font-style: italic;
            font-size: 0.95em;
            color: #555555;
            margin-top: 30px;
        }
        </style>

        <div class="email-list">
            <a class="github-link" href="https://github.com/AyaAttia20" target="_blank">
                <img class="github-icon" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg">
                Aya Attia
            </a>
            <a class="github-link" href="https://github.com/yasminkadry" target="_blank">
                <img class="github-icon" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg">
                Yasmin Kadry
            </a>
            <a class="github-link" href="https://github.com/MariamOsama3" target="_blank">
                <img class="github-icon" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg">
                Mariam Osama
            </a>
            <a class="github-link" href="https://github.com/RehamElkasaby" target="_blank">
                <img class="github-icon" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg">
                Reham Elkasaby
            </a>
        </div>

        <div class="fun-fact">
            🚀 Fun Fact: This project was built with coffee, code, and endless curiosity.<br>
            🌱 Keep learning, keep building — your next idea could change the world!
        </div>
    """, unsafe_allow_html=True)

## Session State 
if "page" not in st.session_state:  ## defualt page
    st.session_state.page = "Home"

if st.session_state.page == "Home":
    home()

elif st.session_state.page == "CV Parser":
    cv_parser()

elif st.session_state.page == "About":
    about()

elif st.session_state.page == "Contact":
    contact()

 ## footer   
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    f"""
    <p style='text-align: center; font-size: 0.9em; color: gray;'>
        Built with <a style='color: var(--primary-color); text-decoration: none;' href='https://streamlit.io' target='_blank'>Streamlit</a> | 
        Project by <a style='color: var(--primary-color); text-decoration: none;'href= 'https://github.com/RehamElkasaby/Smart-Recruiter-Assistant-RAG-based' arget='_blank'> | <span style="font-weight: 600; color: #244DA0;">MY Team</span> 💡</a>
    </p>
    """,
    unsafe_allow_html=True
)
