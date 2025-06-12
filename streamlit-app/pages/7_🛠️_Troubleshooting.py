import streamlit as st
import sys
import os

# Add project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import initialize_language
from content.translations import get_text

st.set_page_config(
    page_title="Troubleshooting",
    page_icon="🛠️",
    layout="wide"
)

# Initialize session state for language if it doesn't exist
if 'language' not in st.session_state:
    st.session_state['language'] = "English"

language = initialize_language()

st.title(get_text(language, "troubleshooting_title"))
    
st.markdown(f"### {get_text(language, 'troubleshooting_header')}")

with st.expander(get_text(language, "issue_services_fail_header")):
    st.markdown(get_text(language, "issue_services_fail_content"))
    
with st.expander(get_text(language, "issue_no_data_header")):
    st.markdown(get_text(language, "issue_no_data_content"))
    
with st.expander(get_text(language, "issue_streamlit_error_header")):
    st.markdown(get_text(language, "issue_streamlit_error_content"))
    
st.info(get_text(language, "troubleshooting_info")) 