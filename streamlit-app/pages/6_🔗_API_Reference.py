import streamlit as st
import sys
import os

# Add project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import initialize_language
from content.translations import get_text

st.set_page_config(
    page_title="API Reference",
    page_icon="🔗",
    layout="wide"
)

# Initialize session state for language if it doesn't exist
if 'language' not in st.session_state:
    st.session_state['language'] = "English"

language = initialize_language()

st.title(get_text(language, "api_ref_title"))
st.markdown(get_text(language, "api_ref_header"))

st.markdown(f"### {get_text(language, 'api_ref_obs_header')}")
st.markdown(get_text(language, "api_ref_obs_content"))

st.markdown(f"### {get_text(language, 'api_ref_kafka_header')}")
st.markdown(get_text(language, "api_ref_kafka_content"))

st.markdown(f"### {get_text(language, 'api_ref_otel_header')}")
st.markdown(get_text(language, "api_ref_otel_content")) 