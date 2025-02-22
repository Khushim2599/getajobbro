import streamlit as st
from pymongo import MongoClient

# MongoDB Connection
try:
    client = MongoClient("mongodb+srv://Yateeka:hacklytics@hackalytics.warwu.mongodb.net/")
    db = client['job_data']
    job_collection = db['job_listings']
except Exception as e:
    st.error(f"Database connection failed: {e}")

# Initialize session state for login and navigation
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Sign In"

# Authentication Functions
def sign_in():
    st.subheader("Sign In")
    username = st.text_input("Username", key="signin_username")
    password = st.text_input("Password", type="password", key="signin_password")
    if st.button("Sign In"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.current_page = "Job Search"  # Redirect to Job Search
            st.success(f"Welcome back, {username}!")
            st.rerun()
        else:
            st.error("Please enter valid credentials.")

def sign_up():
    st.subheader("Sign Up")
    username = st.text_input("New Username", key="signup_username")
    password = st.text_input("New Password", type="password", key="signup_password")
    if st.button("Sign Up"):
        st.success("Account created successfully!")
        st.session_state.current_page = "Sign In"  # Redirect to Sign In
        st.rerun()  # 🚀 Auto-redirect


def change_password():
    st.subheader("Change Password")
    username = st.text_input("Username", key="change_user")
    old_password = st.text_input("Old Password", type="password", key="old_pass")
    new_password = st.text_input("New Password", type="password", key="new_pass")
    if st.button("Change Password"):
        st.success("Password changed successfully!")

def job_search():
    st.subheader("Job Search")
    
    # Dropdown for Job Title selection
    job_title_input = st.selectbox(
        "Select Job Title", 
        options=["Select", 
                 "Software Engineer", 
                 "Data Scientist", 
                 "Product Manager", 
                 "Registered Nurse", 
                 "HR Specialist", 
                 "Financial Analyst", 
                 "Construction Manager", 
                 "Investment Banker", 
                 "Teacher", 
                 "Event Planner", 
                 "Customer Service Representative"],  # List of job titles
        index=0  # Default to 'Select'
    )
    
    # Dropdown for Employment Type selection
    employment_type_input = st.selectbox(
        "Select Employment Type", 
        options=["Select", "Intern", "Full-time", "Part-time"],  # Default option is 'Select'
        index=0  # By default, 'Select' will be the first option
    )

    if st.button("Search Jobs"):
        # Only proceed if valid selections are made
        if job_title_input == "Select":
            st.error("Please select a valid job title.")
            return
        if employment_type_input == "Select":
            st.error("Please select a valid employment type.")
            return

        # Process the job search based on the selected job title and employment type
        query = {
            'job_title': {'$regex': job_title_input, '$options': 'i'}
        }

        if employment_type_input != "Select":
            query['employment_type'] = {'$regex': employment_type_input, '$options': 'i'}  # Case-insensitive match for employment_type

        try:
            matching_jobs = list(job_collection.find(query))

            st.subheader("Search Results")
            if matching_jobs:
                for job in matching_jobs:
                    st.write(f"**{job.get('job_title', 'N/A')}** at {job.get('company_name', 'N/A')}")
                    st.write(f"📍 Location: {job.get('location', 'N/A')}")
                    st.write(f"💼 Employment Type: {job.get('employment_type', 'N/A')}")
                    st.write(f"🛠️ Required Skills: {', '.join(job.get('required_skills', []))}")
                    st.write(f"📝 Description: {job.get('job_description', 'N/A')}")
                    st.write(f"📝 Salary: {job.get('salary_range', 'N/A')}")
                    st.write("---")
            else:
                st.warning("No matching jobs found. Try different keywords or employment type.")
        except Exception as e:
            st.error(f"Error fetching data: {e}")


def upload_resume():
    st.subheader("Upload Resume")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx"])
    if uploaded_file is not None:
        st.success(f"Uploaded: {uploaded_file.name}")

def sign_out():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.current_page = "Sign In"
    st.success("Signed out successfully!")
    st.rerun()

def main():
    #st.title("MongoDB Job Search App")

    # Dynamic menu based on login status
    if st.session_state.logged_in:
        menu = ["Job Search", "Upload Resume", "Sign Out"]
    else:
        menu = ["Sign In", "Sign Up", "Change Password"]

    # Sidebar navigation
    choice = st.sidebar.radio("Navigation", menu, index=menu.index(st.session_state.current_page))

    # Update session state if navigation changes
    if st.session_state.current_page != choice:
        st.session_state.current_page = choice

    # Conditional rendering based on current page
    if st.session_state.current_page == "Sign In":
        sign_in()
    elif st.session_state.current_page == "Sign Up":
        sign_up()
    elif st.session_state.current_page == "Change Password":
        change_password()
    elif st.session_state.current_page == "Job Search":
        job_search()
    elif st.session_state.current_page == "Upload Resume":
        upload_resume()
    elif st.session_state.current_page == "Sign Out":
        sign_out()

if __name__ == "__main__":
    main()