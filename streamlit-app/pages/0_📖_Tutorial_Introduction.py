import streamlit as st
import sys
import os

# Add project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import initialize_language
from content.translations import get_text

def main():
    st.set_page_config(
        page_title="Tutorial Introduction",
        page_icon="📖",
        layout="wide"
    )
    language = initialize_language()

    st.title(f"📖 {get_text(language, 'intro_title')}")
    st.markdown(get_text(language, 'intro_markdown'))

    st.info(get_text(language, 'intro_info'))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(get_text(language, 'intro_structure_header'))
        st.markdown(get_text(language, 'intro_structure_content'))

    with col2:
        st.subheader(get_text(language, 'intro_prereq_header'))
        st.markdown(get_text(language, 'intro_prereq_content'))

if __name__ == "__main__":
    main() 