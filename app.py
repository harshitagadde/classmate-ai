import os
import io
import time
import datetime
import streamlit as st
from dotenv import load_dotenv
from google import genai
import pypdf
from pptx import Presentation
import pandas as pd
from PIL import Image

# Load environment variables
load_dotenv()

# Page Setup
st.set_page_config(page_title="Classmate AI", page_icon="📚", layout="wide")

# Track Session Metrics & Activity Logs Real-Time
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "notes_processed" not in st.session_state:
    st.session_state.notes_processed = 0
if "quizzes_generated" not in st.session_state:
    st.session_state.quizzes_generated = 0
if "concepts_explained" not in st.session_state:
    st.session_state.concepts_explained = 0
if "messages" not in st.session_state:
    st.session_state.messages = []
if "exam_schedule" not in st.session_state:
    st.session_state.exam_schedule = []
if "todo_list" not in st.session_state:
    st.session_state.todo_list = [
        {"task": "Revise Chapter 1 Notes", "done": False},
        {"task": "Solve Practice Quiz on Math", "done": True}
    ]
if "user_activity_log" not in st.session_state:
    st.session_state.user_activity_log = []

# Activity Logger Helper Function
def log_activity(user_name, user_email, action, details=""):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.user_activity_log.insert(0, {
        "Timestamp": timestamp,
        "Student Name": user_name,
        "Email": user_email,
        "Action Performed": action,
        "Details": details
    })

# Student Accounts Database Simulation
if "student_db" not in st.session_state:
    st.session_state.student_db = {"harshita@student.com": {"password": "123", "name": "Harshita Gadde"}}

# Primary Admin Credentials
if "admin_db" not in st.session_state:
    st.session_state.admin_db = {
        "harshitagadde04@gmail.com": {
            "password": "Honey@peppa2008",
            "name": "Harshita Gadde (Primary Admin)"
        }
    }

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
if "user_role" not in st.session_state:
    st.session_state.user_role = "Student"

# ---------------------------------------------------------
# DYNAMIC ADAPTIVE CSS FOR BOTH LIGHT & DARK THEMES
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Global App Adaptive Background & Text */
    .stApp { 
        background-color: var(--background-color) !important; 
        color: var(--text-color) !important; 
    }
    
    section[data-testid="stSidebar"] { 
        background-color: var(--secondary-background-color) !important; 
        border-right: 1px solid rgba(128, 128, 128, 0.2) !important; 
    }
    
    /* Login Form Container */
    .login-container {
        padding-top: 10px;
    }
    .login-title {
        font-size: 3rem !important;
        font-weight: 800 !important;
        color: var(--text-color) !important;
        margin-bottom: 2px !important;
    }
    .login-sub {
        color: var(--text-color) !important;
        opacity: 0.8;
        font-size: 1.1rem !important;
        margin-bottom: 20px !important;
        font-weight: 500;
    }

    /* Force all text elements, labels, and markdown to follow active theme color */
    .stMarkdown, p, span, label, div[data-testid="stWidgetLabel"], h1, h2, h3, h4, h5, h6 {
        color: var(--text-color) !important;
        font-weight: 600 !important;
    }
    
    /* Input Fields & Text Areas Adaptive Theme */
    .stTextInput input, .stTextArea textarea {
        background-color: var(--secondary-background-color) !important;
        border: 1.5px solid rgba(128, 128, 128, 0.3) !important;
        border-radius: 8px !important;
        color: var(--text-color) !important;
        font-size: 1.05rem !important;
        padding: 10px !important;
    }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: var(--text-color) !important;
        opacity: 0.6 !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #9333ea !important;
        box-shadow: 0 0 0 2px rgba(147, 51, 234, 0.3) !important;
    }

    /* Selectbox Dropdowns Visibility Fix */
    div[data-baseweb="select"] > div {
        background-color: var(--secondary-background-color) !important;
        color: var(--text-color) !important;
        border: 1.5px solid rgba(128, 128, 128, 0.3) !important;
        border-radius: 8px !important;
    }
    
    /* Radio Option Buttons Container */
    div[data-testid="stRadio"] > div {
        background-color: var(--secondary-background-color) !important;
        padding: 8px 12px;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        margin-bottom: 10px;
    }
    div[data-testid="stRadio"] label span {
        color: var(--text-color) !important;
        font-weight: 700 !important;
    }

    /* Right Purple Hero Card (Vibrant Accent in Both Themes) */
    .purple-hero-card {
        background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%) !important;
        padding: 45px;
        border-radius: 28px;
        color: #ffffff !important;
        box-shadow: 0 20px 40px rgba(124, 58, 237, 0.3);
        height: 100%;
        min-height: 480px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .purple-hero-title {
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        line-height: 1.1;
        margin-bottom: 12px;
    }
    .purple-hero-sub {
        color: #e9d5ff !important;
        font-size: 1.25rem !important;
        margin-bottom: 20px;
    }

    /* Buttons Override */
    div.stButton > button {
        background-color: #9333ea !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        border: none !important;
        padding: 0.7rem 1.2rem !important;
        box-shadow: 0 4px 12px rgba(147, 51, 234, 0.4);
    }
    div.stButton > button:hover {
        background-color: #7e22ce !important;
    }

    /* Logged In Workspace & Dashboard Cards */
    .welcome-card, .dashboard-card, .workspace-container {
        background-color: var(--secondary-background-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        padding: 22px; 
        border-radius: 14px; 
        margin-bottom: 16px; 
    }
    .welcome-title, .card-title { 
        font-size: 2.2rem !important; 
        font-weight: 800 !important; 
        color: var(--text-color) !important; 
    }
    .welcome-subtitle { 
        color: var(--text-color) !important; 
        opacity: 0.8;
        font-size: 1.05rem !important; 
    }
    .card-subtext { 
        color: #9333ea !important; 
        font-weight: 700 !important; 
        font-size: 0.95rem; 
    }
    </style>
""", unsafe_allow_html=True)

# API Query Function using Gemini 3.6 Flash
def query_gemini(contents):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise Exception("API Key missing! Ensure GEMINI_API_KEY is set in your .env file.")
    
    client = genai.Client(api_key=api_key)
    candidate_models = ['gemini-3.6-flash', 'gemini-2.5-flash']
    
    last_err = None
    for model_name in candidate_models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=contents
            )
            return response.text
        except Exception as e:
            last_err = e
            continue
            
    raise Exception(f"Gemini API Error: {str(last_err)}")

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("# 📚 Classmate AI")
    st.caption("Universal Learning & Admin Console")
    st.divider()

    if st.session_state.logged_in_user is not None:
        user_info = st.session_state.logged_in_user
        st.success(f"Logged in: **{user_info['name']}** ({st.session_state.user_role})")
        if st.button("Sign Out"):
            log_activity(user_info['name'], st.session_state.logged_in_email, "User Sign Out", "User signed out of portal")
            st.session_state.logged_in_user = None
            st.session_state.logged_in_email = None
            st.rerun()
            
        st.divider()
        if st.session_state.user_role == "Student":
            st.markdown("### 📌 Student Navigation")
            nav = st.radio(
                "Go To:",
                ["🎓 AI Study Assistant", "📋 Custom Study Plan", "💬 Buddy (AI Chatbot)", "📅 Exam Schedule", "📊 Real Study Analytics"]
            )

# ---------------------------------------------------------
# LANDING / LOGIN PORTAL
# ---------------------------------------------------------
if st.session_state.logged_in_user is None:
    
    col_login, col_hero = st.columns([0.9, 1.1], gap="large")

    # Left Form Column
    with col_login:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">Login</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-sub">Enter your account details</div>', unsafe_allow_html=True)
        
        portal_type = st.radio("Select Portal Access:", ["Student Portal", "Admin Portal"], horizontal=True)

        if portal_type == "Student Portal":
            auth_mode = st.radio("Action:", ["Sign In", "Create Account"], horizontal=True)

            if auth_mode == "Sign In":
                login_email = st.text_input("Username / Email:", placeholder="student@example.com")
                login_pass = st.text_input("Password:", type="password")
                
                st.write("")
                if st.button("Login"):
                    if login_email in st.session_state.student_db and st.session_state.student_db[login_email]["password"] == login_pass:
                        st.session_state.logged_in_user = st.session_state.student_db[login_email]
                        st.session_state.logged_in_email = login_email
                        st.session_state.user_role = "Student"
                        log_activity(st.session_state.logged_in_user["name"], login_email, "Portal Login", "Student logged into the Student Portal")
                        st.rerun()
                    else:
                        st.error("Invalid student email or password!")
            else:
                reg_name = st.text_input("Full Name:")
                reg_email = st.text_input("Register Email:")
                reg_pass = st.text_input("Register Password:", type="password")
                
                st.write("")
                if st.button("Sign up"):
                    if reg_name and reg_email and reg_pass:
                        st.session_state.student_db[reg_email] = {"password": reg_pass, "name": reg_name}
                        log_activity(reg_name, reg_email, "Account Registration", "New student account created")
                        st.success("Student account created successfully! Switch to 'Sign In'.")
                    else:
                        st.warning("Please fill in all registration fields.")

        else: # Admin Portal Selected
            st.info("🔒 Admin Access is restricted. Pre-authorized admin credentials required.")
            admin_email = st.text_input("Admin Email Address:", placeholder="admin@example.com")
            admin_pass = st.text_input("Admin Password:", type="password")
            
            st.write("")
            if st.button("Login to Admin Console"):
                if admin_email in st.session_state.admin_db and st.session_state.admin_db[admin_email]["password"] == admin_pass:
                    st.session_state.logged_in_user = st.session_state.admin_db[admin_email]
                    st.session_state.logged_in_email = admin_email
                    st.session_state.user_role = "Admin"
                    log_activity(st.session_state.logged_in_user["name"], admin_email, "Admin Console Login", "Admin logged into the console")
                    st.rerun()
                else:
                    st.error("Access Denied! Invalid credentials or no Admin privileges.")
                    
        st.markdown('</div>', unsafe_allow_html=True)

    # Right Purple Card with Vector Graphic
    with col_hero:
        st.markdown("""
            <div class="purple-hero-card">
                <div>
                    <div class="purple-hero-title">Welcome to<br>Classmate AI</div>
                    <div class="purple-hero-sub">Login to access your personalized learning workspace</div>
                </div>
                <div style="text-align: center; margin-top: 20px;">
                    <svg width="260" height="200" viewBox="0 0 200 160" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M40 120 C40 80, 160 80, 160 120 Z" fill="#6d28d9" opacity="0.4"/>
                        <rect x="50" y="40" width="100" height="70" rx="8" fill="#ffffff" stroke="#1e2025" stroke-width="3"/>
                        <line x1="65" y1="58" x2="115" y2="58" stroke="#7c3aed" stroke-width="4" stroke-linecap="round"/>
                        <line x1="65" y1="72" x2="135" y2="72" stroke="#94a3b8" stroke-width="3" stroke-linecap="round"/>
                        <line x1="65" y1="84" x2="105" y2="84" stroke="#94a3b8" stroke-width="3" stroke-linecap="round"/>
                        <circle cx="125" cy="110" r="18" fill="#a855f7"/>
                        <path d="M120 110 L124 114 L132 104" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW 1: STUDENT DASHBOARD
# ---------------------------------------------------------
elif st.session_state.user_role == "Student":
    user_name = st.session_state.logged_in_user["name"]
    user_email = st.session_state.logged_in_email
    elapsed_minutes = int((time.time() - st.session_state.start_time) / 60)

    st.markdown(f"""
        <div class="welcome-card">
            <div class="welcome-title">Hi, {user_name}! 🎓📖</div>
            <div class="welcome-subtitle">Classmate AI Student Portal — Solve doubts with <b>Buddy</b>, summarize notes, and track real progress.</div>
        </div>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        st.markdown(f'<div class="dashboard-card"><div class="card-title">⏱️ Active Study Time</div><div class="card-subtext">{elapsed_minutes} Minutes</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown(f'<div class="dashboard-card"><div class="card-title">📝 Notes Summarized</div><div class="card-subtext">{st.session_state.notes_processed} Processed</div></div>', unsafe_allow_html=True)
    with col_c:
        st.markdown(f'<div class="dashboard-card"><div class="card-title">❓ Quizzes Generated</div><div class="card-subtext">{st.session_state.quizzes_generated} Sets</div></div>', unsafe_allow_html=True)
    with col_d:
        st.markdown(f'<div class="dashboard-card"><div class="card-title">📅 Exams Scheduled</div><div class="card-subtext">{len(st.session_state.exam_schedule)} Scheduled</div></div>', unsafe_allow_html=True)

    st.write("")

    if nav == "🎓 AI Study Assistant":
        st.markdown("### 🛠️ AI Study Assistant Workspace")
        col1, col2 = st.columns([1, 1], gap="large")

        with col1:
            st.markdown('<div class="workspace-container">', unsafe_allow_html=True)
            st.markdown("#### 📝 Study Material Input")
            
            feature = st.selectbox(
                "Select Action:",
                ["Summarize Notes", "Generate Practice Quiz", "Explain Concept Simply"]
            )

            input_mode = st.radio("Input Method:", ["Paste Text", "Upload Document/Image"])
            extracted_text = ""
            uploaded_file = None

            if input_mode == "Paste Text":
                extracted_text = st.text_area("Enter study material or notes:", height=180, placeholder="Paste study notes or text on any topic...")
            else:
                uploaded_file = st.file_uploader("Upload File (PDF, PPT, Excel, Image):", type=["pdf", "pptx", "xlsx", "xls", "csv", "png", "jpg", "jpeg", "txt"])
                if uploaded_file is not None:
                    file_type = uploaded_file.name.split(".")[-1].lower()
                    try:
                        if file_type == "pdf":
                            reader = pypdf.PdfReader(uploaded_file)
                            for page in reader.pages:
                                text = page.extract_text()
                                if text: extracted_text += text + "\n"
                        elif file_type == "pptx":
                            prs = Presentation(uploaded_file)
                            for slide in prs.slides:
                                for shape in slide.shapes:
                                    if hasattr(shape, "text"): extracted_text += shape.text + "\n"
                        elif file_type in ["xlsx", "xls", "csv"]:
                            df = pd.read_csv(uploaded_file) if file_type == "csv" else pd.read_excel(uploaded_file)
                            extracted_text = df.to_string()
                        elif file_type == "txt":
                            extracted_text = uploaded_file.read().decode("utf-8")
                        elif file_type in ["png", "jpg", "jpeg"]:
                            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
                            image_input = Image.open(uploaded_file)
                            
                        st.success(f"Parsed: {uploaded_file.name}")
                    except Exception as e:
                        st.error(f"Error parsing file: {str(e)}")

            generate_btn = st.button("🚀 Process with AI")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="workspace-container">', unsafe_allow_html=True)
            st.markdown("#### 💡 AI Output")
            
            if generate_btn:
                if input_mode == "Paste Text" and not extracted_text.strip():
                    st.warning("⚠️ Please provide text before submitting!")
                elif input_mode == "Upload Document/Image" and uploaded_file is None:
                    st.warning("⚠️ Please upload a file first!")
                else:
                    if feature == "Summarize Notes":
                        prompt = f"Summarize the following study text into clear, structured bullet points with headers:\n\n{extracted_text}"
                        st.session_state.notes_processed += 1
                    elif feature == "Generate Practice Quiz":
                        prompt = f"Create 3 practice multiple-choice questions (A-D) with correct answers and explanations based on this study text:\n\n{extracted_text}"
                        st.session_state.quizzes_generated += 1
                    else:
                        prompt = f"Explain the main concepts in this text in simple terms with examples:\n\n{extracted_text}"
                        st.session_state.concepts_explained += 1

                    try:
                        with st.spinner("Classmate AI processing..."):
                            contents = [image_input, prompt] if (input_mode == "Upload Document/Image" and uploaded_file.name.split(".")[-1].lower() in ["png", "jpg", "jpeg"]) else prompt
                            res = query_gemini(contents)
                            st.markdown(res)
                            log_activity(user_name, user_email, f"Used AI Assistant: {feature}", f"Mode: {input_mode}")
                    except Exception as e:
                        st.error(f"❌ {str(e)}")
            else:
                st.info("AI generated output will appear here.")
            st.markdown('</div>', unsafe_allow_html=True)

    elif nav == "📋 Custom Study Plan":
        st.subheader("📋 Custom Study Plan (To-Do List)")
        col_td1, col_td2 = st.columns([1, 1], gap="large")

        with col_td1:
            st.markdown('<div class="workspace-container">', unsafe_allow_html=True)
            st.markdown("### ➕ Add New Task")
            new_task = st.text_input("Enter study goal or topic:", placeholder="e.g. Read Physics Chapter 3")
            if st.button("Add to Study Plan"):
                if new_task.strip():
                    st.session_state.todo_list.append({"task": new_task, "done": False})
                    log_activity(user_name, user_email, "Added Study Plan Task", f"Task: {new_task}")
                    st.success("Task added!")
                    st.rerun()
                else:
                    st.warning("Please enter a task name.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_td2:
            st.markdown('<div class="workspace-container">', unsafe_allow_html=True)
            st.markdown("### 📌 Active Tasks")
            if st.session_state.todo_list:
                for idx, item in enumerate(st.session_state.todo_list):
                    col_chk, col_btn = st.columns([4, 1])
                    with col_chk:
                        done = st.checkbox(item["task"], value=item["done"], key=f"task_{idx}")
                        if done != item["done"]:
                            st.session_state.todo_list[idx]["done"] = done
                            status_str = "Completed" if done else "Marked Incomplete"
                            log_activity(user_name, user_email, f"Updated Study Task ({status_str})", f"Task: {item['task']}")
                    with col_btn:
                        if st.button("❌", key=f"del_task_{idx}"):
                            removed_item = st.session_state.todo_list.pop(idx)
                            log_activity(user_name, user_email, "Deleted Study Task", f"Task: {removed_item['task']}")
                            st.rerun()
            else:
                st.info("No study tasks added yet!")
            st.markdown('</div>', unsafe_allow_html=True)

    elif nav == "💬 Buddy (AI Chatbot)":
        st.subheader("💬 Buddy — Universal Doubt Clearing Chatbot")
        st.write("Ask Buddy any doubt regarding **any subject or topic** (Math, Science, History, Coding, Languages, etc.)!")

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        active_prompt = st.chat_input("Ask Buddy a question about any subject...")

        if active_prompt:
            st.session_state.messages.append({"role": "user", "content": active_prompt})
            with st.chat_message("user"):
                st.markdown(active_prompt)

            with st.chat_message("assistant"):
                try:
                    with st.spinner("Buddy is answering..."):
                        chat_prompt = f"You are Buddy, a friendly expert tutor for all academic subjects. Answer the student's question clearly and step-by-step.\n\nStudent Question: {active_prompt}"
                        reply_text = query_gemini(chat_prompt)
                        st.markdown(reply_text)
                        st.session_state.messages.append({"role": "assistant", "content": reply_text})
                        log_activity(user_name, user_email, "Asked Buddy (Chatbot)", f"Prompt: {active_prompt[:60]}...")
                except Exception as e:
                    st.error(f"Chatbot Error: {str(e)}")

    elif nav == "📅 Exam Schedule":
        st.subheader("📅 Dynamic Exam Schedule Manager")
        col_sch1, col_sch2 = st.columns([1, 1], gap="large")
        
        with col_sch1:
            st.markdown('<div class="workspace-container">', unsafe_allow_html=True)
            st.markdown("### ➕ Add Exam / Task")
            new_subject = st.text_input("Exam Name:", placeholder="e.g. Physics Midterm")
            new_date = st.date_input("Exam Date:")
            
            if st.button("Save Exam"):
                if new_subject.strip():
                    st.session_state.exam_schedule.append({"subject": new_subject, "date": str(new_date)})
                    log_activity(user_name, user_email, "Added Scheduled Exam", f"Exam: {new_subject} on {new_date}")
                    st.success(f"Added **{new_subject}** on `{new_date}`!")
                else:
                    st.warning("Enter an exam name.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_sch2:
            st.markdown('<div class="workspace-container">', unsafe_allow_html=True)
            st.markdown("### 📋 Scheduled Exams")
            if st.session_state.exam_schedule:
                for idx, item in enumerate(st.session_state.exam_schedule):
                    st.markdown(f"**{idx + 1}. {item['subject']}** — 🗓️ `{item['date']}`")
            else:
                st.info("No exams scheduled.")
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.subheader("📊 Real Session Study Analytics")
        st.markdown("Real-time activity stats generated from your current study session:")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Active Session Time", f"{elapsed_minutes} mins")
        col_m2.metric("Notes Summarized", f"{st.session_state.notes_processed}")
        col_m3.metric("Quizzes Completed", f"{st.session_state.quizzes_generated}")

        st.divider()
        st.markdown("**Real Activity Breakdown**")
        activity_data = pd.DataFrame({
            "Activity": ["Summaries", "Quizzes", "Concepts Explained"],
            "Count": [st.session_state.notes_processed, st.session_state.quizzes_generated, st.session_state.concepts_explained]
        })
        st.bar_chart(activity_data.set_index("Activity"))

# ---------------------------------------------------------
# VIEW 2: ADMIN DASHBOARD
# ---------------------------------------------------------
else:
    admin_name = st.session_state.logged_in_user["name"]

    st.markdown(f"""
        <div class="welcome-card">
            <div class="welcome-title">🛡️ Admin Control Console</div>
            <div class="welcome-subtitle">Welcome, <b>{admin_name}</b>. Manage student accounts, monitor live activity logs, grant admin privileges, and manage exams.</div>
        </div>
    """, unsafe_allow_html=True)

    admin_tabs = st.tabs([
        "👥 Student Accounts & Access Control", 
        "📊 Live Student Usage Logs", 
        "🛡️ Active Admin List", 
        "📅 System Exam Manager"
    ])

    # Tab 1: Access Control
    with admin_tabs[0]:
        st.subheader("Manage Registered Students & Grant Admin Access")
        
        if st.session_state.student_db:
            for email, info in list(st.session_state.student_db.items()):
                col_u1, col_u2 = st.columns([3, 1])
                with col_u1:
                    st.write(f"👤 **{info['name']}** (`{email}`)")
                with col_u2:
                    is_admin = email in st.session_state.admin_db
                    if is_admin:
                        st.success("Admin Access Granted")
                    else:
                        if st.button(f"Grant Admin Access", key=f"grant_{email}"):
                            st.session_state.admin_db[email] = {
                                "password": info["password"],
                                "name": f"{info['name']} (Admin)"
                            }
                            st.success(f"Granted Admin privileges to {info['name']}!")
                            st.rerun()
        else:
            st.info("No registered student accounts yet.")

    # Tab 2: Activity Logs View
    with admin_tabs[1]:
        st.subheader("📊 Live Student Usage & Activity Logs")
        st.caption("Track logins, tool usage, chatbot prompts, and study tasks in real-time.")

        if st.session_state.user_activity_log:
            df_logs = pd.DataFrame(st.session_state.user_activity_log)
            st.dataframe(df_logs, use_container_width=True)
        else:
            st.info("No student activity logged yet in this session.")

    # Tab 3: Admin List
    with admin_tabs[2]:
        st.subheader("Active Authorized Admins")
        admins_list = [{"Admin Name": info["name"], "Email": email} for email, info in st.session_state.admin_db.items()]
        st.dataframe(pd.DataFrame(admins_list), use_container_width=True)

    # Tab 4: System Exams
    with admin_tabs[3]:
        st.subheader("Active System Exams")
        if st.session_state.exam_schedule:
            for idx, item in enumerate(st.session_state.exam_schedule):
                col_e1, col_e2 = st.columns([3, 1])
                with col_e1: st.write(f"**{idx+1}. {item['subject']}** (`{item['date']}`)")
                with col_e2:
                    if st.button(f"Delete #{idx+1}", key=f"del_{idx}"):
                        st.session_state.exam_schedule.pop(idx)
                        st.rerun()
        else:
            st.info("No exams in database.")