import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import docker
import psutil
import os
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import yaml
import json

# Page configuration
st.set_page_config(
    page_title="Kafka APM & Observability Demo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for language if it doesn't exist
if 'language' not in st.session_state:
    st.session_state['language'] = "English"

def set_language():
    """Callback function to update language in session state"""
    st.session_state.language = st.session_state.lang_selector

# Constants
GRAFANA_URL = os.getenv("GRAFANA_URL", "http://localhost:3000")
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")
OTEL_COLLECTOR_URL = os.getenv("OTEL_COLLECTOR_URL", "http://localhost:13133")

def get_docker_status():
    """Check Docker services status"""
    try:
        client = docker.from_env()
        containers = client.containers.list()
        services = {}
        for container in containers:
            name = container.name
            status = container.status
            services[name] = {
                'status': status,
                'image': container.image.tags[0] if container.image.tags else 'unknown',
                'ports': container.ports,
                'created': container.attrs['Created']
            }
        return services
    except Exception as e:
        return {"error": str(e)}

def check_service_health(url, timeout=5):
    """Check if a service is responding"""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except:
        return False

def get_system_metrics():
    """Get basic system metrics"""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        'cpu_percent': cpu_percent,
        'memory_percent': memory.percent,
        'memory_available': memory.available / (1024**3),  # GB
        'disk_percent': disk.percent,
        'disk_free': disk.free / (1024**3)  # GB
    }

# Sidebar navigation
st.sidebar.title("�� Demo Navigation")

# Language selection in the sidebar
st.sidebar.selectbox(
    "Language / 語言:", 
    ["English", "繁體中文"], 
    key='lang_selector', 
    on_change=set_language
)

st.sidebar.markdown("---")

pages = {
    "🏠 Overview": "overview",
    "🏗️ Architecture": "architecture", 
    "🔧 Tech Stack": "tech_stack",
    "📊 Monitoring Guide": "monitoring",
    "🎮 Demo Scenarios": "scenarios",
    "📈 Live Status": "status",
    "🔗 API Reference": "api",
    "🛠️ Troubleshooting": "troubleshooting"
}

selected_page = st.sidebar.radio("Select a page:", list(pages.keys()))
page_key = pages[selected_page]

# Use language from session state
language = st.session_state.language

# Main content area
if page_key == "overview":
    if language == "繁體中文":
        st.title("Kafka APM 與可觀測性解決方案示範")
        st.markdown("### Apache Kafka 環境的應用程式效能監控 (APM) 與可觀測性模式示範")
        
        st.info("⚠️ **注意：** 這是一個概念驗證的示範專案，供學習與評估使用，若要用於正式環境需要進行大幅度的修改。")
        
        st.markdown("#### 🎯 示範價值")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            - **端到端可見性** - 涵蓋生產者、消費者、代理伺服器和基礎設施
            - **快速問題解決** - 透過關聯的指標、日誌和追蹤縮短修復時間
            """)
        with col2:
            st.markdown("""
            - **主動監控** - 提早偵測效能衰退和容量問題
            - **多語言支援** - 跨 Java、Python 和 Go 應用程式的統一可觀測性
            """)
    else:
        st.title("Kafka APM & Observability Solution Demo")
        st.markdown("### A demonstration of Application Performance Monitoring (APM) and observability patterns for Apache Kafka environments")
        
        st.info("⚠️ **Note:** This is a proof-of-concept demo project for learning and evaluation purposes, not intended for production use without significant modifications.")
        
        st.markdown("#### 🎯 Demo Value")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            - **End-to-End Visibility** - Full observability across producers, consumers, brokers, and infrastructure
            - **Rapid Problem Resolution** - Reduce MTTR from hours to minutes with correlated telemetry
            """)
        with col2:
            st.markdown("""
            - **Proactive Monitoring** - Early detection of performance degradation and capacity issues
            - **Multi-Language Support** - Unified observability across Java, Python, and Go applications
            """)
    
    # Quick Start section
    st.markdown("---")
    if language == "繁體中文":
        st.markdown("### 🚀 快速開始")
        
        with st.expander("📋 前置需求檢查"):
            st.code("""
# 驗證 Docker 和 Compose 安裝
docker --version          # 應為 20.10+
docker compose version     # 應為 v2.x+

# 檢查系統資源
free -h                    # 驗證可用 RAM (需要 4GB+)
df -h                      # 驗證磁碟空間 (需要 5GB+)
            """, language="bash")
        
        with st.expander("🔄 部署步驟"):
            st.code("""
# 1. 複製與設定
git clone <repository_url>
cd kakfa-o11y
chmod +x start.sh

# 2. 啟動環境
./start.sh

# 3. 驗證部署
docker compose ps
            """, language="bash")
    else:
        st.markdown("### 🚀 Quick Start")
        
        with st.expander("📋 Prerequisites Check"):
            st.code("""
# Verify Docker and Compose installation
docker --version          # Should be 20.10+
docker compose version     # Should be v2.x+

# Check system resources
free -h                    # Verify available RAM (4GB+ needed)
df -h                      # Verify disk space (5GB+ needed)
            """, language="bash")
        
        with st.expander("🔄 Deployment Steps"):
            st.code("""
# 1. Clone and Setup
git clone <repository_url>
cd kakfa-o11y
chmod +x start.sh

# 2. Start the Environment
./start.sh

# 3. Verify Deployment
docker compose ps
            """, language="bash")

elif page_key == "architecture":
    if language == "繁體中文":
        st.title("🏗️ 系統架構")
        st.markdown("### 可觀測性架構概覽")
    else:
        st.title("🏗️ System Architecture")
        st.markdown("### Observability Architecture Overview")
    
    # Mermaid diagram
    st.markdown("""
    ```mermaid
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
    ```
    """)
    
    # Architecture principles
    if language == "繁體中文":
        st.markdown("### 🎯 關鍵架構原則")
        principles = [
            ("集中化收集", "使用單一 OpenTelemetry Collector 收集所有遙測資料"),
            ("廠商中立性", "基於標準的 OpenTelemetry 實作"),
            ("可擴展性", "具備持久化儲存的水平可擴展元件"),
            ("安全性", "可配置的認證與加密支援"),
            ("高可用性", "具備健康檢查和自動復原的彈性設計")
        ]
    else:
        st.markdown("### 🎯 Key Architecture Principles")
        principles = [
            ("Centralized Collection", "Single OpenTelemetry Collector for all telemetry data"),
            ("Vendor Neutrality", "Standards-based OpenTelemetry implementation"),
            ("Scalability", "Horizontally scalable components with persistent storage"),
            ("Security", "Configurable authentication and encryption support"),
            ("High Availability", "Resilient design with health checks and automatic recovery")
        ]
    
    for title, description in principles:
        st.markdown(f"**{title}:** {description}")

elif page_key == "tech_stack":
    if language == "繁體中文":
        st.title("🔧 技術堆疊")
    else:
        st.title("🔧 Technology Stack")
    
    # Technology stack tables
    if language == "繁體中文":
        st.markdown("### 📱 應用程式監測層")
        app_data = {
            "元件": ["Java Apps", "Python Apps", "Go Apps"],
            "技術": ["OpenTelemetry Java Agent", "OpenTelemetry Python SDK", "OpenTelemetry Go SDK"],
            "用途": ["自動監測", "手動監測", "手動監測"],
            "主要特色": [
                "零程式碼監測、JVM 指標、Kafka 客戶端追蹤",
                "自訂指標、結構化日誌、非同步支援",
                "高效能追蹤、自訂指標、低負擔"
            ]
        }
        
        st.markdown("### 📨 訊息串流平台")
        kafka_data = {
            "元件": ["Apache Kafka", "Zookeeper", "JMX Exporters"],
            "技術": ["Confluent Platform", "Apache Zookeeper", "Prometheus JMX Exporter"],
            "用途": ["訊息代理伺服器", "協調服務", "指標收集"],
            "主要特色": [
                "高吞吐量、耐久性、基於分區的擴展",
                "叢集協調、配置管理",
                "代理伺服器指標、JVM 統計、主題指標"
            ]
        }
        
        st.markdown("### 👁️ 可觀測性基礎設施")
        obs_data = {
            "元件": ["OpenTelemetry Collector", "Prometheus", "Loki", "Tempo", "Grafana"],
            "技術": ["OTEL Collector Contrib", "Prometheus TSDB", "Grafana Loki", "Grafana Tempo", "Grafana"],
            "用途": ["遙測管道", "指標儲存", "日誌聚合", "追蹤儲存", "視覺化"],
            "主要特色": [
                "資料收集、處理、路由、匯出",
                "時間序列資料庫、PromQL 查詢、告警",
                "日誌索引、LogQL 查詢、標籤組織",
                "分散式追蹤、追蹤關聯、取樣",
                "儀表板、告警、資料探索"
            ]
        }
    else:
        st.markdown("### 📱 Application Instrumentation Layer")
        app_data = {
            "Component": ["Java Apps", "Python Apps", "Go Apps"],
            "Technology": ["OpenTelemetry Java Agent", "OpenTelemetry Python SDK", "OpenTelemetry Go SDK"],
            "Purpose": ["Auto-instrumentation", "Manual instrumentation", "Manual instrumentation"],
            "Key Features": [
                "Zero-code instrumentation, JVM metrics, Kafka client tracing",
                "Custom metrics, structured logging, async support",
                "High-performance tracing, custom metrics, low overhead"
            ]
        }
        
        st.markdown("### 📨 Message Streaming Platform")
        kafka_data = {
            "Component": ["Apache Kafka", "Zookeeper", "JMX Exporters"],
            "Technology": ["Confluent Platform", "Apache Zookeeper", "Prometheus JMX Exporter"],
            "Purpose": ["Message Broker", "Coordination Service", "Metrics Collection"],
            "Key Features": [
                "High throughput, durability, partition-based scaling",
                "Cluster coordination, configuration management",
                "Broker metrics, JVM stats, topic metrics"
            ]
        }
        
        st.markdown("### 👁️ Observability Infrastructure")
        obs_data = {
            "Component": ["OpenTelemetry Collector", "Prometheus", "Loki", "Tempo", "Grafana"],
            "Technology": ["OTEL Collector Contrib", "Prometheus TSDB", "Grafana Loki", "Grafana Tempo", "Grafana"],
            "Purpose": ["Telemetry Pipeline", "Metrics Storage", "Log Aggregation", "Trace Storage", "Visualization"],
            "Key Features": [
                "Data collection, processing, routing, export",
                "Time-series database, PromQL queries, alerting",
                "Log indexing, LogQL queries, label-based organization",
                "Distributed tracing, trace correlation, sampling",
                "Dashboards, alerting, data exploration"
            ]
        }
    
    st.dataframe(pd.DataFrame(app_data), use_container_width=True)
    st.dataframe(pd.DataFrame(kafka_data), use_container_width=True)
    st.dataframe(pd.DataFrame(obs_data), use_container_width=True)

elif page_key == "monitoring":
    if language == "繁體中文":
        st.title("📊 監控與可觀測性指南")
        st.markdown("### 預建儀表板與監控場景")
    else:
        st.title("📊 Monitoring & Observability Guide")
        st.markdown("### Pre-Built Dashboards & Monitoring Scenarios")
    
    # Dashboard access
    st.markdown("#### 🎛️ Dashboard Access")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔗 Grafana Dashboard"):
            st.markdown(f"[Open Grafana]({GRAFANA_URL})")
            st.info("Default credentials: admin/admin")
    
    with col2:
        if st.button("📈 Prometheus"):
            st.markdown(f"[Open Prometheus]({PROMETHEUS_URL})")
    
    with col3:
        if st.button("🔍 OTel Collector"):
            st.markdown(f"[Health Check]({OTEL_COLLECTOR_URL}/health)")
    
    # Key metrics
    if language == "繁體中文":
        st.markdown("#### 📋 需要觀察的關鍵指標")
        metrics_data = {
            "指標名稱": [
                "kafka_messages_sent_total",
                "go.producer.messages_sent", 
                "kafka_network_request_total_time_ms_mean",
                "jvm_memory_used_bytes{area=\"heap\"}"
            ],
            "描述": [
                "Python 生產者吞吐量",
                "Go 生產者吞吐量",
                "請求延遲",
                "記憶體使用量"
            ],
            "查詢": [
                "rate(kafka_messages_sent_total[1m])",
                "rate(go_producer_messages_sent[1m])",
                "kafka_network_request_total_time_ms_mean",
                "jvm_memory_used_bytes{area=\"heap\"}"
            ]
        }
    else:
        st.markdown("#### 📋 Key Metrics to Watch")
        metrics_data = {
            "Metric Name": [
                "kafka_messages_sent_total",
                "go.producer.messages_sent", 
                "kafka_network_request_total_time_ms_mean",
                "jvm_memory_used_bytes{area=\"heap\"}"
            ],
            "Description": [
                "Python producer throughput",
                "Go producer throughput",
                "Request latency",
                "Memory usage"
            ],
            "Query": [
                "rate(kafka_messages_sent_total[1m])",
                "rate(go_producer_messages_sent[1m])",
                "kafka_network_request_total_time_ms_mean",
                "jvm_memory_used_bytes{area=\"heap\"}"
            ]
        }
    
    st.dataframe(pd.DataFrame(metrics_data), use_container_width=True)

elif page_key == "scenarios":
    if language == "繁體中文":
        st.title("🎮 示範情境")
        st.markdown("### 指導式逐步說明")
    else:
        st.title("🎮 Demo Scenarios")
        st.markdown("### Guided Walkthrough")
    
    # Scenario tabs
    if language == "繁體中文":
        scenario_tabs = st.tabs(["情境A: 正常營運監控", "情境B: 效能故障排除", "情境C: 故障復原", "情境D: 擴展營運"])
    else:
        scenario_tabs = st.tabs(["Scenario A: Normal Operations", "Scenario B: Performance Troubleshooting", "Scenario C: Failure Recovery", "Scenario D: Scaling Operations"])
    
    with scenario_tabs[0]:
        if language == "繁體中文":
            st.markdown("#### 🎯 學習目標")
            st.markdown("1. 啟動環境並觀察基準指標")
            st.markdown("2. 瀏覽 Grafana 儀表板")
            st.markdown("3. 了解正常效能模式")
            st.markdown("4. 設定基本告警規則")
            
            st.markdown("#### 📝 操作步驟")
            st.code("""
# 產生負載並觀察
docker compose logs -f python-producer
            """, language="bash")
        else:
            st.markdown("#### 🎯 Learning Objectives")
            st.markdown("1. Start the environment and observe baseline metrics")
            st.markdown("2. Navigate through Grafana dashboards")
            st.markdown("3. Understand normal performance patterns")
            st.markdown("4. Set up basic alerting rules")
            
            st.markdown("#### 📝 Steps")
            st.code("""
# Generate load and observe
docker compose logs -f python-producer
            """, language="bash")
    
    with scenario_tabs[1]:
        if language == "繁體中文":
            st.markdown("#### 🎯 學習目標")
            st.markdown("1. 引入人工延遲")
            st.markdown("2. 觀察指標衰退")
            st.markdown("3. 使用日誌識別根本原因")
            st.markdown("4. 追蹤請求在系統中的流程")
            
            st.markdown("#### 📝 操作步驟")
            st.code("""
# 模擬網路問題
docker compose pause kafka
docker compose logs python-consumer
docker compose unpause kafka
            """, language="bash")
        else:
            st.markdown("#### 🎯 Learning Objectives")
            st.markdown("1. Introduce artificial latency")
            st.markdown("2. Observe metric degradation")
            st.markdown("3. Use logs to identify root cause")
            st.markdown("4. Trace request flow through system")
            
            st.markdown("#### 📝 Steps")
            st.code("""
# Simulate network issues
docker compose pause kafka
docker compose logs python-consumer
docker compose unpause kafka
            """, language="bash")

elif page_key == "status":
    if language == "繁體中文":
        st.title("📈 即時系統狀態")
    else:
        st.title("📈 Live System Status")
    
    # Real-time status monitoring
    col1, col2 = st.columns(2)
    
    with col1:
        if language == "繁體中文":
            st.markdown("#### 🐳 Docker 服務狀態")
        else:
            st.markdown("#### 🐳 Docker Services Status")
        
        if st.button("🔄 Refresh Status"):
            services = get_docker_status()
            if "error" in services:
                st.error(f"Error: {services['error']}")
            else:
                status_data = []
                for name, info in services.items():
                    status_data.append({
                        "Service": name,
                        "Status": info['status'],
                        "Image": info['image'][:30] + "..." if len(info['image']) > 30 else info['image']
                    })
                st.dataframe(pd.DataFrame(status_data), use_container_width=True)
    
    with col2:
        if language == "繁體中文":
            st.markdown("#### 🖥️ 系統指標")
        else:
            st.markdown("#### 🖥️ System Metrics")
        
        if st.button("📊 Check System"):
            metrics = get_system_metrics()
            
            # Create gauge charts
            fig_cpu = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = metrics['cpu_percent'],
                title = {'text': "CPU Usage (%)"},
                gauge = {'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [{'range': [0, 50], 'color': "lightgray"},
                                 {'range': [50, 80], 'color': "yellow"},
                                 {'range': [80, 100], 'color': "red"}],
                        'threshold': {'line': {'color': "red", 'width': 4},
                                     'thickness': 0.75, 'value': 90}}))
            fig_cpu.update_layout(height=300)
            st.plotly_chart(fig_cpu, use_container_width=True)
            
            st.metric("Memory Available", f"{metrics['memory_available']:.1f} GB", f"{metrics['memory_percent']:.1f}%")
            st.metric("Disk Free", f"{metrics['disk_free']:.1f} GB", f"{metrics['disk_percent']:.1f}%")

elif page_key == "api":
    if language == "繁體中文":
        st.title("🔗 API 參考")
    else:
        st.title("🔗 API Reference")
    
    # Service endpoints
    if language == "繁體中文":
        st.markdown("#### 🌐 服務端點")
        endpoints_data = {
            "端點": [
                "http://localhost:4317",
                "http://localhost:4318", 
                "http://localhost:13133/health",
                "http://localhost:3000",
                "http://localhost:9090"
            ],
            "用途": [
                "OTLP gRPC",
                "OTLP HTTP",
                "健康檢查",
                "Grafana 介面",
                "Prometheus 介面"
            ],
            "連接埠": [4317, 4318, 13133, 3000, 9090]
        }
    else:
        st.markdown("#### 🌐 Service Endpoints")
        endpoints_data = {
            "Endpoint": [
                "http://localhost:4317",
                "http://localhost:4318", 
                "http://localhost:13133/health",
                "http://localhost:3000",
                "http://localhost:9090"
            ],
            "Purpose": [
                "OTLP gRPC",
                "OTLP HTTP",
                "Health Check",
                "Grafana Interface",
                "Prometheus Interface"
            ],
            "Port": [4317, 4318, 13133, 3000, 9090]
        }
    
    st.dataframe(pd.DataFrame(endpoints_data), use_container_width=True)
    
    # API examples
    if language == "繁體中文":
        st.markdown("#### 📋 API 使用範例")
    else:
        st.markdown("#### 📋 API Usage Examples")
    
    st.code("""
# Prometheus API - Query metrics
curl "http://localhost:9090/api/v1/query?query=kafka_messages_sent_total"

# Grafana API - Create dashboard
curl -X POST http://admin:admin@localhost:3000/api/dashboards/db \\
  -H "Content-Type: application/json" \\
  -d @dashboard.json
    """, language="bash")

else:  # troubleshooting
    if language == "繁體中文":
        st.title("🛠️ 故障排除")
        st.markdown("### 常見問題與解決方案")
    else:
        st.title("🛠️ Troubleshooting")
        st.markdown("### Common Issues & Solutions")
    
    # Common issues table
    if language == "繁體中文":
        issues_data = {
            "問題": ["高記憶體使用量", "消費者延遲", "網路問題", "儲存增長"],
            "症狀": ["OOM 錯誤、回應緩慢", "處理延遲", "連線逾時", "磁碟空間警告"],
            "解決方案": [
                "增加容器記憶體限制",
                "擴展消費者或最佳化處理",
                "檢查 Docker 網路、防火牆規則",
                "實作保留政策"
            ]
        }
    else:
        issues_data = {
            "Issue": ["High Memory Usage", "Consumer Lag", "Network Issues", "Storage Growth"],
            "Symptoms": ["OOM errors, slow response", "Processing delays", "Connection timeouts", "Disk space warnings"],
            "Solution": [
                "Increase container memory limits",
                "Scale consumers or optimize processing",
                "Check Docker networking, firewall rules",
                "Implement retention policies"
            ]
        }
    
    st.dataframe(pd.DataFrame(issues_data), use_container_width=True)
    
    # Diagnostic commands
    if language == "繁體中文":
        st.markdown("#### 🔍 診斷指令")
    else:
        st.markdown("#### 🔍 Diagnostic Commands")
    
    st.code("""
# View detailed logs
docker compose logs --tail=100 -f [service-name]

# Check resource usage
docker stats

# Kafka cluster status
docker compose exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092
    """, language="bash")

# Footer
st.sidebar.markdown("---")
if language == "繁體中文":
    st.sidebar.info("💡 **提示：** 這是一個教育示範專案，展示現代可觀測性模式")
else:
    st.sidebar.info("💡 **Tip:** This is an educational demo showcasing modern observability patterns")

st.sidebar.markdown(f"**Version:** Demo v1.0")
st.sidebar.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
