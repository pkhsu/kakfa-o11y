import streamlit as st
import pandas as pd
import sys
import os
from streamlit_mermaid import st_mermaid

# Add project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import initialize_language
from content.translations import get_text

st.set_page_config(
    page_title="System Architecture",
    page_icon="🏗️",
    layout="wide"
)

# Initialize session state for language if it doesn't exist
if 'language' not in st.session_state:
    st.session_state['language'] = "English"

language = initialize_language()

st.title(get_text(language, "arch_title"))
st.markdown(f"### {get_text(language, 'arch_overview_header')}")

# Mermaid diagram
st_mermaid("""
graph TB
    subgraph "Application Layer"
        JP[Java Producer]
        JC[Java Consumer]
        PP[Python Producer]
        PC[Python Consumer]
        GP[Go Producer]
        GC[Go Consumer]
    end
    
    subgraph "Kafka Cluster"
        K[Kafka Broker]
        Z[Zookeeper]
        JMX1[JMX Exporter - Kafka]
        JMX2[JMX Exporter - Zookeeper]
    end
    
    subgraph "Observability Pipeline"
        OC[OpenTelemetry Collector]
    end
    
    subgraph "Storage & Processing"
        P[Prometheus<br/>Metrics]
        L[Loki<br/>Logs]
        T[Tempo<br/>Traces]
    end
    
    subgraph "Visualization & Alerting"
        G[Grafana<br/>Dashboards & Alerts]
        SA[Streamlit<br/>Demo App]
    end
    
    JP --> |OTLP| OC
    JC --> |OTLP| OC
    PP --> |OTLP| OC
    PC --> |OTLP| OC
    GP --> |OTLP| OC
    GC --> |OTLP| OC
    
    JP -.-> |Kafka Protocol| K
    JC -.-> |Kafka Protocol| K
    PP -.-> |Kafka Protocol| K
    PC -.-> |Kafka Protocol| K
    GP -.-> |Kafka Protocol| K
    GC -.-> |Kafka Protocol| K
    
    JMX1 --> |Prometheus Format| OC
    JMX2 --> |Prometheus Format| OC
    K --> JMX1
    Z --> JMX2
    
    OC --> |Metrics| P
    OC --> |Logs| L
    OC --> |Traces| T
    
    P --> G
    L --> G
    T --> G
    
    G --> SA
""")

# Architecture principles
st.markdown("---")
st.markdown(f"### {get_text(language, 'arch_principles_header')}")

principles = [
    (get_text(language, "arch_principle_central"), get_text(language, "arch_principle_central_desc")),
    (get_text(language, "arch_principle_vendor"), get_text(language, "arch_principle_vendor_desc")),
    (get_text(language, "arch_principle_scale"), get_text(language, "arch_principle_scale_desc")),
    (get_text(language, "arch_principle_security"), get_text(language, "arch_principle_security_desc")),
    (get_text(language, "arch_principle_ha"), get_text(language, "arch_principle_ha_desc"))
]

for title, description in principles:
    st.markdown(f"**{title}:** {description}")

# Data flow diagram
st.markdown("---")
st.markdown(f"### {get_text(language, 'data_flow_header')}")

st_mermaid("""
flowchart LR
    A[Applications] --> B[OTLP]
    B --> C[OpenTelemetry Collector]
    C --> D[Prometheus]
    C --> E[Loki]
    C --> F[Tempo]
    D --> G[Grafana]
    E --> G
    F --> G
    G --> H[Alerts]
    G --> I[Dashboards]
""")

# Performance characteristics
st.markdown("---")
st.markdown(f"### {get_text(language, 'perf_header')}")

perf_data = {
    get_text(language, 'perf_component'): ["Java Producer", "Python Producer", "Go Producer"],
    get_text(language, 'perf_throughput'): ["5,000-10,000 msg/sec", "1,000-2,000 msg/sec", "8,000-15,000 msg/sec"],
    get_text(language, 'perf_latency'): ["< 50ms", "< 100ms", "< 30ms"],
    get_text(language, 'perf_memory'): ["~500MB", "~200MB", "~100MB"]
}

st.dataframe(pd.DataFrame(perf_data), use_container_width=True) 