import streamlit as st
import os
from pathlib import Path

# Function to load markdown content from a file
def load_markdown(filepath):
    # This is a placeholder. In a working version, this would read the file.
    # For this subtask, we are just ensuring app.py is valid.
    # The actual content files will be created empty by this subtask.
    placeholder_content = {
        "welcome.md": "Welcome content placeholder.",
        "start_environment.md": "Start environment placeholder.",
        "using_producers_consumers.md": "Producers/consumers placeholder.",
        "observing_grafana.md": "Observing Grafana placeholder.",
        "grafana_dashboard.md": "Grafana dashboard section placeholder.",
        "grafana_prometheus.md": "Grafana Prometheus section placeholder.",
        "grafana_loki.md": "Grafana Loki section placeholder.",
        "grafana_tempo.md": "Grafana Tempo section placeholder."
    }
    # Simulate file path construction for the app's logic
    file_key = Path(filepath).name
    if Path(filepath).parent.name == "content":
        return placeholder_content.get(file_key, f"Content for {file_key} will be here.")
    return f"Placeholder for {filepath}"


CONTENT_DIR = Path("content") # Simplified for this stage

GRAFANA_URL = os.getenv("GRAFANA_URL_BROWSER_ACCESS", "http://localhost:3000")

def get_service_log_command(service_name):
    return f"docker compose logs -f {service_name}"

st.set_page_config(page_title="Kafka O11y Tutorial", layout="wide")
st.title("Apache Kafka & OpenTelemetry (O11y) Tutorial")
st.caption("A hands-on demonstration (Content is currently placeholder).")

st.sidebar.header("Tutorial Navigation")
page_options = {
    "1. Welcome & Setup": "welcome.md",
    "2. Start the Environment": "start_environment.md",
    "3. Using Producers & Consumers": "using_producers_consumers.md",
    "4. Observing Telemetry in Grafana": "observing_grafana.md"
}
page_selection = st.sidebar.radio("Choose a section:", list(page_options.keys()))

selected_content_filename = page_options[page_selection]

st.header(page_selection)
# Simulate loading content. The actual files will be empty for now.
st.markdown(load_markdown(str(CONTENT_DIR / selected_content_filename)))

if page_selection == "1. Welcome & Setup":
    st.subheader("Project Directory Structure (Example)")
    # This st.code block is known to cause issues in subtasks.
    # Omitting it for this minimal version to ensure app.py creation.
    # It would ideally show the directory tree.
    st.text("Directory structure would be shown here.")

elif page_selection == "2. Start the Environment":
    st.code("./start.sh", language="bash")
    st.info("Run the start script to launch services.")

elif page_selection == "3. Using Producers & Consumers":
    log_lang = st.selectbox("Choose a language to see log commands:", ["Java", "Python", "Go"])
    st.code(get_service_log_command(f"{log_lang.lower()}-producer"), language="bash")

elif page_selection == "4. Observing Telemetry in Grafana":
    st.markdown(f"Access Grafana directly: [{GRAFANA_URL}]({GRAFANA_URL})")
    st.markdown(load_markdown(str(CONTENT_DIR / "grafana_dashboard.md")))
    st.markdown(load_markdown(str(CONTENT_DIR / "grafana_prometheus.md")))
    st.markdown(load_markdown(str(CONTENT_DIR / "grafana_loki.md")))
    st.markdown(load_markdown(str(CONTENT_DIR / "grafana_tempo.md")))

st.sidebar.info("Tutorial v0.3 (Minimal Content)")
