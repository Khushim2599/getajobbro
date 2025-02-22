import streamlit as st

def apply_custom_style():
    st.markdown(
        """
        <style>
        /* Custom Buttons */
        .stButton > button {
            border-radius: 10px;
            background-color: #4CAF50; 
            color: white;
            padding: 10px 15px;
            font-size: 16px;
            transition: 0.3s;
        }
        .stButton > button:hover {
            background-color: #3e8e41;
        }

        /* Input Fields */
        .stTextInput, .stSelectbox {
            border-radius: 10px;
            border: 1px solid #ddd;
            padding: 5px;
        }

        /* Titles */
        .title {
            font-size: 30px;
            font-weight: bold;
            text-align: center;
            color: #333;
        }

        /* Sidebar */
        .stSidebar {
            background-color: #f8f9fa;
            padding: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
