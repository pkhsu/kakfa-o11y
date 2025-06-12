import streamlit as st
import sys
import os
import pandas as pd
import docker
import psutil
import plotly.graph_objects as go
from utils.helpers import initialize_language
from content.translations import get_text

# Add project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- Page Configuration ---
st.set_page_config(
    page_title="Kafka Observability Demo",
    page_icon="🚦",
    layout="wide"
)

# Initialize session state for language
if 'language' not in st.session_state:
    st.session_state['language'] = 'English'

# --- Sidebar for Language Selection ---
with st.sidebar:
    st.title("🌍 Language")
    
    # Use on_change to update session state
    def update_language():
        st.session_state.language = st.session_state.lang_selector
    
    selected_language = st.radio(
        "Choose a language:",
        ('English', '繁體中文'),
        key='lang_selector',
        on_change=update_language
    )

language = st.session_state.language

# --- Main Page Content (Overview) ---

st.title(get_text(language, "app_title"))
st.header(get_text(language, "welcome_header"))
st.markdown(get_text(language, "welcome_intro"))

st.markdown(f"### {get_text(language, 'project_goals_header')}")
st.markdown(get_text(language, "project_goals_content"))

st.success(get_text(language, "ready_message"))

st.markdown("---")

st.markdown(f"### {get_text(language, 'before_you_begin_header')}")
st.info(get_text(language, "before_you_begin_content"))
