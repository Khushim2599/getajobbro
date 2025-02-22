import streamlit as st
from backend import fetch_jobs, extract_text_from_pdf, extract_text_from_docx, get_resume_feedback
from pymongo import MongoClient
from style import apply_custom_style  # Import styling function

# Apply custom styling
apply_custom_style()

# ---------- 🌐 DATABASE CONNECTION ----------
try:
    client = MongoClient("mongodb+srv://Yateeka:hacklytics@hackalytics.warwu.mongodb.net/")
    db = client['job_data']
    job_collection = db['job_listings']
except Exception as e:
    st.error(f"Database connection failed: {e}")

# ---------- 🔐 SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "current_page" not in st.session_state:
    st.session_state.current_page = "Sign In"

# Enable detailed error messages
st.set_option("client.showErrorDetails", True)

# ---------- 🏠 NAVIGATION MENU ----------
st.sidebar.image("https://i.imgur.com/OHdGqkZ.png", use_column_width=True)
st.sidebar.title("🚀 Navigation")

menu = ["Sign In", "Sign Up", "Change Password"]
if st.session_state.logged_in:
    menu = ["Job Search", "Upload Resume", "Sign Out"]

choice = st.sidebar.radio("", menu)

# ---------- 🔑 AUTHENTICATION ----------
def sign_in():
    st.subheader("🔑 Sign In")
    username = st.text_input("Username", key="signin_username")
    password = st.text_input("Password", type="password", key="signin_password", help="Enter your password")

    if st.button("Sign In"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.current_page = "Job Search"
            st.success(f"Welcome back, {username}! 🚀")
            st.rerun()
        else:
            st.error("⚠️ Please enter valid credentials.")

def sign_up():
    st.subheader("🆕 Sign Up")
    username = st.text_input("New Username", key="signup_username")
    password = st.text_input("New Password", type="password", key="signup_password")

    if st.button("Sign Up"):
        st.success("✅ Account created successfully! Please sign in.")
        st.session_state.current_page = "Sign In"
        st.rerun()

def change_password():
    st.subheader("🔄 Change Password")
    username = st.text_input("Username", key="change_user")
    old_password = st.text_input("Old Password", type="password", key="old_pass")
    new_password = st.text_input("New Password", type="password", key="new_pass")

    if st.button("Change Password"):
        st.success("✅ Password changed successfully!")

def sign_out():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.current_page = "Sign In"
    st.success("👋 Signed out successfully!")
    st.rerun()

# ---------- 🔍 JOB SEARCH PAGE ----------
def job_search():
    st.subheader("🔍 Job Search")

    job_title_input = st.selectbox(
        "Select Job Title", 
        ["Select", "Software Engineer", "Data Scientist", "Product Manager", "Registered Nurse", "HR Specialist", 
         "Financial Analyst", "Construction Manager", "Investment Banker", "Teacher", "Event Planner", "Customer Service Representative"],
        index=0
    )

    employment_type_input = st.selectbox(
        "Select Employment Type", 
        ["Select", "Intern", "Full-time", "Part-time"], 
        index=0
    )

    if st.button("🔎 Search Jobs"):
        if job_title_input == "Select" or employment_type_input == "Select":
            st.error("⚠️ Please select both job title and employment type.")
        else:
            query = {"job_title": {"$regex": job_title_input, "$options": "i"}}
            if employment_type_input != "Select":
                query["employment_type"] = {"$regex": employment_type_input, "$options": "i"}

            try:
                matching_jobs = list(job_collection.find(query))
                st.subheader("📋 Job Listings")

                if matching_jobs:
                    for job in matching_jobs:
                        st.markdown(f"**{job.get('job_title', 'N/A')}** at {job.get('company_name', 'N/A')}")
                        st.write(f"📍 Location: {job.get('location', 'N/A')}")
                        st.write(f"💼 Employment Type: {job.get('employment_type', 'N/A')}")
                        st.write(f"📝 Description: {job.get('job_description', 'N/A')}")
                        st.write(f"💰 Salary: {job.get('salary_range', 'N/A')}")
                        st.divider()
                else:
                    st.warning("🚫 No matching jobs found. Try different keywords.")
            except Exception as e:
                st.error(f"⚠️ Error fetching data: {e}")

# ---------- 📄 RESUME UPLOAD PAGE ----------
def upload_resume():
    st.subheader("📄 Upload Resume")
    uploaded_file = st.file_uploader("📂 Choose a file", type=["pdf", "docx"])

    if uploaded_file is not None:
        st.success(f"✅ Uploaded: {uploaded_file.name}")
        with st.spinner("Extracting text..."):
            if uploaded_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text = extract_text_from_docx(uploaded_file)

        if resume_text.strip():
            st.text_area("📑 Extracted Resume Text", resume_text, height=200)
            user_question = st.text_input("🧐 Ask AI for Resume Feedback:")
            if st.button("💬 Get AI Feedback"):
                feedback = get_resume_feedback(resume_text, user_question)
                st.subheader("💡 AI Feedback")
                st.write(feedback)
        else:
            st.error("⚠️ Could not extract any text.")

# ---------- 🚀 MAIN FUNCTION ----------
if choice == "Sign In":
    sign_in()
elif choice == "Sign Up":
    sign_up()
elif choice == "Change Password":
    change_password()
elif choice == "Job Search":
    job_search()
elif choice == "Upload Resume":
    upload_resume()
elif choice == "Sign Out":
    sign_out()
