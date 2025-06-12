import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="System Architecture",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ System Architecture")
st.markdown("### Detailed Architecture Overview")

# Language selection
language = st.selectbox("Language / 語言:", ["English", "繁體中文"])

if language == "繁體中文":
    st.markdown("### 🎯 架構層級")
    
    tab1, tab2, tab3, tab4 = st.tabs(["應用程式層", "Kafka 叢集", "可觀測性管道", "儲存與視覺化"])
    
    with tab1:
        st.markdown("#### 📱 應用程式監測層")
        st.markdown("""
        - **Java 應用程式**: 使用 OpenTelemetry Java Agent 進行自動監測
        - **Python 應用程式**: 使用 OpenTelemetry Python SDK 進行手動監測  
        - **Go 應用程式**: 使用 OpenTelemetry Go SDK 進行高效能監測
        """)
        
        st.code("""
        # Java 自動監測範例
        java -javaagent:opentelemetry-javaagent.jar \\
             -Dotel.service.name=kafka-producer \\
             -jar producer.jar
        """, language="bash")
    
    with tab2:
        st.markdown("#### 🔄 Kafka 叢集層")
        st.markdown("""
        - **Kafka Broker**: 訊息代理伺服器，處理生產者和消費者請求
        - **Zookeeper**: 叢集協調服務，管理 broker 狀態和配置
        - **JMX Exporters**: 將 JMX 指標轉換為 Prometheus 格式
        """)
        
        st.info("💡 此示範使用單一 broker 配置，適用於學習和測試目的")
    
    with tab3:
        st.markdown("#### 🔍 可觀測性管道")
        st.markdown("""
        **OpenTelemetry Collector** 作為中央收集點：
        - 接收來自所有應用程式的 OTLP 資料
        - 處理和路由遙測資料到適當的後端
        - 支援多種匯出器和處理器
        """)
        
        st.code("""
        # OTLP 配置範例
        receivers:
          otlp:
            protocols:
              grpc:
                endpoint: 0.0.0.0:4317
              http:
                endpoint: 0.0.0.0:4318
        """, language="yaml")
    
    with tab4:
        st.markdown("#### 📊 儲存與視覺化")
        st.markdown("""
        - **Prometheus**: 時間序列指標儲存
        - **Loki**: 日誌聚合和查詢
        - **Tempo**: 分散式追蹤儲存
        - **Grafana**: 統一視覺化和告警平台
        """)

else:
    st.markdown("### 🎯 Architecture Layers")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Application Layer", "Kafka Cluster", "Observability Pipeline", "Storage & Visualization"])
    
    with tab1:
        st.markdown("#### 📱 Application Instrumentation Layer")
        st.markdown("""
        - **Java Applications**: Auto-instrumentation using OpenTelemetry Java Agent
        - **Python Applications**: Manual instrumentation using OpenTelemetry Python SDK
        - **Go Applications**: High-performance instrumentation using OpenTelemetry Go SDK
        """)
        
        st.code("""
        # Java auto-instrumentation example
        java -javaagent:opentelemetry-javaagent.jar \\
             -Dotel.service.name=kafka-producer \\
             -jar producer.jar
        """, language="bash")
    
    with tab2:
        st.markdown("#### 🔄 Kafka Cluster Layer")
        st.markdown("""
        - **Kafka Broker**: Message broker handling producer and consumer requests
        - **Zookeeper**: Cluster coordination service managing broker state and configuration
        - **JMX Exporters**: Convert JMX metrics to Prometheus format
        """)
        
        st.info("💡 This demo uses a single broker configuration suitable for learning and testing")
    
    with tab3:
        st.markdown("#### 🔍 Observability Pipeline")
        st.markdown("""
        **OpenTelemetry Collector** serves as the central collection point:
        - Receives OTLP data from all applications
        - Processes and routes telemetry data to appropriate backends
        - Supports multiple exporters and processors
        """)
        
        st.code("""
        # OTLP configuration example
        receivers:
          otlp:
            protocols:
              grpc:
                endpoint: 0.0.0.0:4317
              http:
                endpoint: 0.0.0.0:4318
        """, language="yaml")
    
    with tab4:
        st.markdown("#### 📊 Storage & Visualization")
        st.markdown("""
        - **Prometheus**: Time-series metrics storage
        - **Loki**: Log aggregation and querying
        - **Tempo**: Distributed tracing storage
        - **Grafana**: Unified visualization and alerting platform
        """)

# Data flow diagram
st.markdown("---")
if language == "繁體中文":
    st.markdown("### 🌊 資料流架構")
else:
    st.markdown("### 🌊 Data Flow Architecture")

st.markdown("""
```mermaid
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
```
""")

# Performance characteristics
st.markdown("---")
if language == "繁體中文":
    st.markdown("### ⚡ 效能特性")
    
    perf_data = {
        "元件": ["Java Producer", "Python Producer", "Go Producer"],
        "預期吞吐量": ["5,000-10,000 msg/sec", "1,000-2,000 msg/sec", "8,000-15,000 msg/sec"],
        "延遲 (P95)": ["< 50ms", "< 100ms", "< 30ms"],
        "記憶體使用": ["~500MB", "~200MB", "~100MB"]
    }
else:
    st.markdown("### ⚡ Performance Characteristics")
    
    perf_data = {
        "Component": ["Java Producer", "Python Producer", "Go Producer"],
        "Expected Throughput": ["5,000-10,000 msg/sec", "1,000-2,000 msg/sec", "8,000-15,000 msg/sec"],
        "Latency (P95)": ["< 50ms", "< 100ms", "< 30ms"],
        "Memory Usage": ["~500MB", "~200MB", "~100MB"]
    }

st.dataframe(pd.DataFrame(perf_data), use_container_width=True) 