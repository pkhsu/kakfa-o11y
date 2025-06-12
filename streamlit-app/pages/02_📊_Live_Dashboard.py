import streamlit as st
import requests
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import os

st.set_page_config(
    page_title="Live Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Live System Dashboard")
st.markdown("### Real-time Monitoring & Metrics")

# Configuration
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")
GRAFANA_URL = os.getenv("GRAFANA_URL", "http://localhost:3000")

def query_prometheus(query, timeout=10):
    """Query Prometheus for metrics"""
    try:
        url = f"{PROMETHEUS_URL}/api/v1/query"
        params = {'query': query}
        response = requests.get(url, params=params, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success' and data['data']['result']:
                return data['data']['result']
        return None
    except Exception as e:
        st.error(f"Failed to query Prometheus: {e}")
        return None

def query_prometheus_range(query, start_time, end_time, step='15s'):
    """Query Prometheus for time series data"""
    try:
        url = f"{PROMETHEUS_URL}/api/v1/query_range"
        params = {
            'query': query,
            'start': start_time.isoformat(),
            'end': end_time.isoformat(),
            'step': step
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success' and data['data']['result']:
                return data['data']['result']
        return None
    except Exception as e:
        st.error(f"Failed to query Prometheus range: {e}")
        return None

# Language selection
language = st.selectbox("Language / 語言:", ["English", "繁體中文"])

# Auto-refresh option
auto_refresh = st.checkbox("Auto-refresh (30s)" if language == "English" else "自動更新 (30秒)")
if auto_refresh:
    time.sleep(30)
    st.experimental_rerun()

# Service status indicators
st.markdown("---")
if language == "繁體中文":
    st.markdown("### 🚥 服務狀態")
else:
    st.markdown("### 🚥 Service Status")

col1, col2, col3, col4 = st.columns(4)

with col1:
    # Check Prometheus
    try:
        prometheus_status = requests.get(f"{PROMETHEUS_URL}/-/ready", timeout=5).status_code == 200
        status_color = "🟢" if prometheus_status else "🔴"
        st.metric("Prometheus", f"{status_color} {'Running' if language == 'English' else '運行中'}" if prometheus_status else f"{status_color} {'Down' if language == 'English' else '離線'}")
    except:
        st.metric("Prometheus", "🔴 Down" if language == "English" else "🔴 離線")

with col2:
    # Check Grafana
    try:
        grafana_status = requests.get(f"{GRAFANA_URL}/api/health", timeout=5).status_code == 200
        status_color = "🟢" if grafana_status else "🔴"
        st.metric("Grafana", f"{status_color} {'Running' if language == 'English' else '運行中'}" if grafana_status else f"{status_color} {'Down' if language == 'English' else '離線'}")
    except:
        st.metric("Grafana", "🔴 Down" if language == "English" else "🔴 離線")

with col3:
    # Check OTel Collector
    try:
        otel_status = requests.get("http://localhost:13133/health", timeout=5).status_code == 200
        status_color = "🟢" if otel_status else "🔴"
        st.metric("OTel Collector", f"{status_color} {'Running' if language == 'English' else '運行中'}" if otel_status else f"{status_color} {'Down' if language == 'English' else '離線'}")
    except:
        st.metric("OTel Collector", "🔴 Down" if language == "English" else "🔴 離線")

with col4:
    # Kafka status (check via metrics)
    kafka_up = query_prometheus('up{job="kafka"}')
    if kafka_up and kafka_up[0]['value'][1] == '1':
        st.metric("Kafka", "🟢 Running" if language == "English" else "🟢 運行中")
    else:
        st.metric("Kafka", "🔴 Down" if language == "English" else "🔴 離線")

# Key metrics dashboard
st.markdown("---")
if language == "繁體中文":
    st.markdown("### 📈 關鍵指標")
else:
    st.markdown("### 📈 Key Metrics")

# Create tabs for different metric categories
if language == "繁體中文":
    metric_tabs = st.tabs(["訊息吞吐量", "延遲指標", "系統資源", "錯誤率"])
else:
    metric_tabs = st.tabs(["Message Throughput", "Latency Metrics", "System Resources", "Error Rates"])

with metric_tabs[0]:
    # Message throughput
    col1, col2 = st.columns(2)
    
    with col1:
        if language == "繁體中文":
            st.markdown("#### 📤 生產者吞吐量")
        else:
            st.markdown("#### 📤 Producer Throughput")
        
        # Query producer metrics
        python_producer = query_prometheus('rate(kafka_messages_sent_total[1m])')
        go_producer = query_prometheus('rate(go_producer_messages_sent[1m])')
        
        if python_producer or go_producer:
            throughput_data = []
            
            if python_producer:
                for result in python_producer:
                    throughput_data.append({
                        'Service': 'Python Producer',
                        'Rate (msg/s)': float(result['value'][1])
                    })
            
            if go_producer:
                for result in go_producer:
                    throughput_data.append({
                        'Service': 'Go Producer', 
                        'Rate (msg/s)': float(result['value'][1])
                    })
            
            if throughput_data:
                df = pd.DataFrame(throughput_data)
                fig = px.bar(df, x='Service', y='Rate (msg/s)', 
                           title='Current Throughput' if language == 'English' else '當前吞吐量')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No throughput data available" if language == "English" else "無吞吐量資料")
        else:
            st.info("No producer metrics found" if language == "English" else "找不到生產者指標")
    
    with col2:
        if language == "繁體中文":
            st.markdown("#### 📥 消費者延遲")
        else:
            st.markdown("#### 📥 Consumer Lag")
        
        # Query consumer lag
        consumer_lag = query_prometheus('kafka_consumer_lag_sum')
        
        if consumer_lag:
            lag_value = float(consumer_lag[0]['value'][1])
            
            # Create gauge chart for lag
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = lag_value,
                title = {'text': "Consumer Lag" if language == "English" else "消費者延遲"},
                delta = {'reference': 0},
                gauge = {
                    'axis': {'range': [None, 1000]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 100], 'color': "lightgray"},
                        {'range': [100, 500], 'color': "yellow"},
                        {'range': [500, 1000], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 500
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No consumer lag data" if language == "English" else "無消費者延遲資料")

with metric_tabs[1]:
    # Latency metrics
    if language == "繁體中文":
        st.markdown("#### ⏱️ 網路請求延遲")
    else:
        st.markdown("#### ⏱️ Network Request Latency")
    
    # Query request latency
    request_latency = query_prometheus('kafka_network_request_total_time_ms_mean')
    
    if request_latency:
        latency_value = float(request_latency[0]['value'][1])
        
        # Time series for the last hour
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=1)
        
        latency_series = query_prometheus_range(
            'kafka_network_request_total_time_ms_mean',
            start_time, end_time
        )
        
        if latency_series:
            timestamps = []
            values = []
            
            for point in latency_series[0]['values']:
                timestamps.append(datetime.fromtimestamp(float(point[0])))
                values.append(float(point[1]))
            
            df = pd.DataFrame({
                'Time': timestamps,
                'Latency (ms)': values
            })
            
            fig = px.line(df, x='Time', y='Latency (ms)',
                         title='Request Latency (Last Hour)' if language == 'English' else '請求延遲 (過去一小時)')
            st.plotly_chart(fig, use_container_width=True)
        
        st.metric("Current Latency" if language == "English" else "當前延遲", f"{latency_value:.2f} ms")
    else:
        st.info("No latency data available" if language == "English" else "無延遲資料")

with metric_tabs[2]:
    # System resources
    col1, col2 = st.columns(2)
    
    with col1:
        if language == "繁體中文":
            st.markdown("#### 💾 JVM 記憶體使用量")
        else:
            st.markdown("#### 💾 JVM Memory Usage")
        
        # Query JVM memory
        jvm_memory = query_prometheus('jvm_memory_used_bytes{area="heap"}')
        
        if jvm_memory:
            memory_values = []
            for result in jvm_memory:
                service = result['metric'].get('job', 'Unknown')
                memory_mb = float(result['value'][1]) / (1024 * 1024)
                memory_values.append({
                    'Service': service,
                    'Memory (MB)': memory_mb
                })
            
            if memory_values:
                df = pd.DataFrame(memory_values)
                fig = px.bar(df, x='Service', y='Memory (MB)',
                           title='JVM Heap Usage' if language == 'English' else 'JVM 堆積使用量')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No JVM memory data" if language == "English" else "無 JVM 記憶體資料")
    
    with col2:
        if language == "繁體中文":
            st.markdown("#### 🖥️ CPU 使用率")
        else:
            st.markdown("#### 🖥️ CPU Usage")
        
        # Query CPU usage
        cpu_usage = query_prometheus('rate(process_cpu_seconds_total[1m]) * 100')
        
        if cpu_usage:
            cpu_values = []
            for result in cpu_usage:
                service = result['metric'].get('job', 'Unknown')
                cpu_percent = float(result['value'][1])
                cpu_values.append({
                    'Service': service,
                    'CPU (%)': cpu_percent
                })
            
            if cpu_values:
                df = pd.DataFrame(cpu_values)
                fig = px.bar(df, x='Service', y='CPU (%)',
                           title='CPU Usage by Service' if language == 'English' else '各服務 CPU 使用率')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No CPU data available" if language == "English" else "無 CPU 資料")

with metric_tabs[3]:
    # Error rates
    if language == "繁體中文":
        st.markdown("#### ❌ 錯誤率監控")
    else:
        st.markdown("#### ❌ Error Rate Monitoring")
    
    # Query error rates
    error_rate = query_prometheus('rate(application_errors_total[5m])')
    
    if error_rate:
        error_data = []
        for result in error_rate:
            service = result['metric'].get('service_name', 'Unknown')
            rate = float(result['value'][1])
            error_data.append({
                'Service': service,
                'Error Rate': rate
            })
        
        if error_data:
            df = pd.DataFrame(error_data)
            fig = px.bar(df, x='Service', y='Error Rate',
                       title='Error Rates by Service' if language == 'English' else '各服務錯誤率',
                       color='Error Rate',
                       color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("No errors detected" if language == "English" else "未偵測到錯誤")
    else:
        st.info("No error rate data" if language == "English" else "無錯誤率資料")

# Quick actions
st.markdown("---")
if language == "繁體中文":
    st.markdown("### 🔧 快速操作")
else:
    st.markdown("### 🔧 Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔗 Open Grafana" if language == "English" else "🔗 開啟 Grafana"):
        st.markdown(f"[Open Grafana Dashboard]({GRAFANA_URL})")
        st.info("Default login: admin/admin")

with col2:
    if st.button("📈 Open Prometheus" if language == "English" else "📈 開啟 Prometheus"):
        st.markdown(f"[Open Prometheus]({PROMETHEUS_URL})")

with col3:
    if st.button("🔄 Manual Refresh" if language == "English" else "🔄 手動更新"):
        st.experimental_rerun()

# Footer with last update time
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}") 