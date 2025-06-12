import streamlit as st
import pandas as pd
import sys
import os

# Add project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import initialize_language
from content.translations import get_text

st.set_page_config(
    page_title="Technology Stack",
    page_icon="🔧",
    layout="wide"
)

language = initialize_language()

st.title(get_text(language, "tech_stack_title"))

def display_table(header_key, data):
    st.markdown(f"### {get_text(language, header_key)}")
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

# Application Instrumentation Layer
app_data = {
    get_text(language, "tech_component"): [
        get_text(language, "tech_java_apps"), 
        get_text(language, "tech_python_apps"), 
        get_text(language, "tech_go_apps")
    ],
    get_text(language, "tech_technology"): [
        get_text(language, "tech_java_agent"), 
        get_text(language, "tech_python_sdk"), 
        get_text(language, "tech_go_sdk")
    ],
    get_text(language, "tech_purpose"): [
        get_text(language, "tech_auto_instrument"), 
        get_text(language, "tech_manual_instrument"), 
        get_text(language, "tech_manual_instrument")
    ],
    get_text(language, "tech_features"): [
        get_text(language, "tech_java_features"),
        get_text(language, "tech_python_features"),
        get_text(language, "tech_go_features")
    ]
}
display_table("tech_app_layer", app_data)

# Message Streaming Platform
kafka_data = {
    get_text(language, "tech_component"): [
        get_text(language, "tech_kafka"), 
        get_text(language, "tech_zookeeper"), 
        get_text(language, "tech_jmx")
    ],
    get_text(language, "tech_technology"): [
        get_text(language, "tech_confluent"), 
        get_text(language, "tech_apache_zookeeper"), 
        get_text(language, "tech_prometheus_jmx")
    ],
    get_text(language, "tech_purpose"): [
        get_text(language, "tech_broker"), 
        get_text(language, "tech_coordination"), 
        get_text(language, "tech_metrics_collection")
    ],
    get_text(language, "tech_features"): [
        get_text(language, "tech_kafka_features"),
        get_text(language, "tech_zookeeper_features"),
        get_text(language, "tech_jmx_features")
    ]
}
display_table("tech_streaming_platform", kafka_data)

# Observability Infrastructure
obs_data = {
    get_text(language, "tech_component"): [
        get_text(language, "tech_otel_collector"), 
        get_text(language, "tech_prometheus"), 
        get_text(language, "tech_loki"), 
        get_text(language, "tech_tempo"), 
        get_text(language, "tech_grafana")
    ],
    get_text(language, "tech_technology"): [
        get_text(language, "tech_otel_contrib"), 
        get_text(language, "tech_prometheus_tsdb"), 
        get_text(language, "tech_grafana_loki"), 
        get_text(language, "tech_grafana_tempo"), 
        get_text(language, "tech_grafana_viz")
    ],
    get_text(language, "tech_purpose"): [
        get_text(language, "tech_pipeline"), 
        get_text(language, "tech_metrics_storage"), 
        get_text(language, "tech_log_aggregation"), 
        get_text(language, "tech_trace_storage"), 
        get_text(language, "tech_visualization")
    ],
    get_text(language, "tech_features"): [
        get_text(language, "tech_otel_features"),
        get_text(language, "tech_prometheus_features"),
        get_text(language, "tech_loki_features"),
        get_text(language, "tech_tempo_features"),
        get_text(language, "tech_grafana_features")
    ]
}
display_table("tech_obs_infra", obs_data) 