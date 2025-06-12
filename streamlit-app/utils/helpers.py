import streamlit as st
from content.translations import get_text

def initialize_language():
    if 'language' not in st.session_state:
        st.session_state['language'] = 'English'

    with st.sidebar:
        st.title("🌍 Language")
        
        def update_language():
            st.session_state.language = st.session_state.lang_selector
        
        selected_language = st.radio(
            get_text(st.session_state.get('language', 'English'), "language_select"),
            ('English', '繁體中文'),
            key='lang_selector',
            on_change=update_language,
            index=0 if st.session_state.get('language') == 'English' else 1
        )
    
    return st.session_state.language 