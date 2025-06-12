import streamlit as st
import subprocess
import time
import pandas as pd
import os
from datetime import datetime

st.set_page_config(
    page_title="Demo Scenarios",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 Interactive Demo Scenarios")
st.markdown("### Hands-on Learning Scenarios")

# Initialize session state for language if it doesn't exist (for direct page access)
if 'language' not in st.session_state:
    st.session_state['language'] = "English"

# Get language from session state
language = st.session_state.language

def run_command(command, timeout=30):
    """Execute shell command and return output"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

# Scenario selection
if language == "繁體中文":
    st.markdown("### 🎯 選擇學習情境")
    scenario_options = {
        "情境 A: 正常營運監控": "scenario_a",
        "情境 B: 效能故障排除": "scenario_b", 
        "情境 C: 故障復原": "scenario_c",
        "情境 D: 擴展營運": "scenario_d"
    }
else:
    st.markdown("### 🎯 Choose Learning Scenario")
    scenario_options = {
        "Scenario A: Normal Operations Monitoring": "scenario_a",
        "Scenario B: Performance Troubleshooting": "scenario_b",
        "Scenario C: Failure Recovery": "scenario_c", 
        "Scenario D: Scaling Operations": "scenario_d"
    }

selected_scenario = st.selectbox(
    "Select a scenario:" if language == "English" else "選擇情境:",
    list(scenario_options.keys())
)

scenario_key = scenario_options[selected_scenario]

# Scenario A: Normal Operations Monitoring
if scenario_key == "scenario_a":
    if language == "繁體中文":
        st.markdown("## 🎯 情境 A: 正常營運監控")
        st.markdown("### 學習目標")
        st.markdown("""
        1. 🚀 啟動完整的可觀測性環境
        2. 📊 了解基準效能指標
        3. 🔍 探索 Grafana 儀表板
        4. 🚨 設定基本告警規則
        """)
        
        st.markdown("### 📝 逐步指導")
        
        with st.expander("步驟 1: 環境啟動"):
            st.markdown("**目標**: 啟動所有服務並驗證狀態")
            
            if st.button("🚀 啟動環境", key="start_env_zh"):
                with st.spinner("正在啟動服務..."):
                    returncode, stdout, stderr = run_command("cd .. && docker compose up -d")
                    if returncode == 0:
                        st.success("✅ 環境啟動成功!")
                        st.code(stdout)
                    else:
                        st.error(f"❌ 啟動失敗: {stderr}")
            
            st.code("""
# 手動啟動指令
cd kakfa-o11y
./start.sh

# 或使用 Docker Compose
docker compose up -d
            """, language="bash")
        
        with st.expander("步驟 2: 服務狀態檢查"):
            st.markdown("**目標**: 確認所有服務正常運行")
            
            if st.button("🔍 檢查服務狀態", key="check_status_zh"):
                with st.spinner("檢查服務中..."):
                    returncode, stdout, stderr = run_command("cd .. && docker compose ps")
                    st.code(stdout)
                    
                    # Check individual services
                    services = ["kafka", "zookeeper", "prometheus", "grafana", "otel-collector"]
                    status_data = []
                    
                    for service in services:
                        returncode, stdout, stderr = run_command(f"cd .. && docker compose ps {service}")
                        status = "Running" if "Up" in stdout else "Down"
                        status_data.append({"服務": service, "狀態": status})
                    
                    st.dataframe(pd.DataFrame(status_data))
        
        with st.expander("步驟 3: 觀察生產者/消費者活動"):
            st.markdown("**目標**: 觀察訊息流和基準指標")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📤 觀察 Python Producer", key="python_prod_zh"):
                    with st.spinner("獲取日誌..."):
                        returncode, stdout, stderr = run_command("cd .. && docker compose logs --tail=20 python-producer")
                        st.code(stdout)
            
            with col2:
                if st.button("📥 觀察 Go Consumer", key="go_cons_zh"):
                    with st.spinner("獲取日誌..."):
                        returncode, stdout, stderr = run_command("cd .. && docker compose logs --tail=20 go-consumer")
                        st.code(stdout)
        
        with st.expander("步驟 4: Grafana 儀表板探索"):
            st.markdown("**目標**: 熟悉監控介面")
            
            st.markdown("📊 **存取資訊**:")
            st.markdown("- URL: http://localhost:3000")
            st.markdown("- 帳號: admin")
            st.markdown("- 密碼: admin")
            
            if st.button("🔗 開啟 Grafana", key="open_grafana_zh"):
                st.markdown("[點擊開啟 Grafana](http://localhost:3000)")
                st.info("💡 首次登入後請更改預設密碼")
    
    else:
        st.markdown("## 🎯 Scenario A: Normal Operations Monitoring")
        st.markdown("### Learning Objectives")
        st.markdown("""
        1. 🚀 Launch complete observability environment
        2. 📊 Understand baseline performance metrics
        3. 🔍 Explore Grafana dashboards
        4. 🚨 Set up basic alerting rules
        """)
        
        st.markdown("### 📝 Step-by-Step Guide")
        
        with st.expander("Step 1: Environment Launch"):
            st.markdown("**Goal**: Start all services and verify status")
            
            if st.button("🚀 Start Environment", key="start_env_en"):
                with st.spinner("Starting services..."):
                    returncode, stdout, stderr = run_command("cd .. && docker compose up -d")
                    if returncode == 0:
                        st.success("✅ Environment started successfully!")
                        st.code(stdout)
                    else:
                        st.error(f"❌ Failed to start: {stderr}")
            
            st.code("""
# Manual start commands
cd kakfa-o11y
./start.sh

# Or use Docker Compose directly
docker compose up -d
            """, language="bash")
        
        with st.expander("Step 2: Service Status Check"):
            st.markdown("**Goal**: Confirm all services are running properly")
            
            if st.button("🔍 Check Service Status", key="check_status_en"):
                with st.spinner("Checking services..."):
                    returncode, stdout, stderr = run_command("cd .. && docker compose ps")
                    st.code(stdout)
                    
                    # Check individual services
                    services = ["kafka", "zookeeper", "prometheus", "grafana", "otel-collector"]
                    status_data = []
                    
                    for service in services:
                        returncode, stdout, stderr = run_command(f"cd .. && docker compose ps {service}")
                        status = "Running" if "Up" in stdout else "Down"
                        status_data.append({"Service": service, "Status": status})
                    
                    st.dataframe(pd.DataFrame(status_data))
        
        with st.expander("Step 3: Observe Producer/Consumer Activity"):
            st.markdown("**Goal**: Watch message flow and baseline metrics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📤 Watch Python Producer", key="python_prod_en"):
                    with st.spinner("Fetching logs..."):
                        returncode, stdout, stderr = run_command("cd .. && docker compose logs --tail=20 python-producer")
                        st.code(stdout)
            
            with col2:
                if st.button("📥 Watch Go Consumer", key="go_cons_en"):
                    with st.spinner("Fetching logs..."):
                        returncode, stdout, stderr = run_command("cd .. && docker compose logs --tail=20 go-consumer")
                        st.code(stdout)
        
        with st.expander("Step 4: Grafana Dashboard Exploration"):
            st.markdown("**Goal**: Familiarize with monitoring interface")
            
            st.markdown("📊 **Access Information**:")
            st.markdown("- URL: http://localhost:3000")
            st.markdown("- Username: admin")
            st.markdown("- Password: admin")
            
            if st.button("🔗 Open Grafana", key="open_grafana_en"):
                st.markdown("[Click to Open Grafana](http://localhost:3000)")
                st.info("💡 Please change default password after first login")

# Scenario B: Performance Troubleshooting
elif scenario_key == "scenario_b":
    if language == "繁體中文":
        st.markdown("## 🔧 情境 B: 效能故障排除")
        st.markdown("### 學習目標")
        st.markdown("""
        1. 🐛 引入人工延遲和錯誤
        2. 📉 觀察指標衰退
        3. 🔍 使用日誌識別根本原因
        4. 🔗 追蹤請求流程
        """)
        
        with st.expander("步驟 1: 模擬網路問題"):
            st.markdown("**目標**: 暫停 Kafka 服務並觀察影響")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("⏸️ 暫停 Kafka", key="pause_kafka_zh"):
                    with st.spinner("暫停 Kafka 服務..."):
                        returncode, stdout, stderr = run_command("cd .. && docker compose pause kafka")
                        if returncode == 0:
                            st.success("✅ Kafka 已暫停")
                            st.warning("⚠️ 生產者和消費者將開始報錯")
                        else:
                            st.error(f"❌ 暫停失敗: {stderr}")
            
            with col2:
                if st.button("▶️ 恢復 Kafka", key="resume_kafka_zh"):
                    with st.spinner("恢復 Kafka 服務..."):
                        returncode, stdout, stderr = run_command("cd .. && docker compose unpause kafka")
                        if returncode == 0:
                            st.success("✅ Kafka 已恢復")
                        else:
                            st.error(f"❌ 恢復失敗: {stderr}")
        
        with st.expander("步驟 2: 觀察錯誤日誌"):
            st.markdown("**目標**: 查看應用程式如何處理連線錯誤")
            
            if st.button("📋 檢視 Consumer 錯誤", key="consumer_errors_zh"):
                with st.spinner("獲取錯誤日誌..."):
                    returncode, stdout, stderr = run_command("cd .. && docker compose logs --tail=30 python-consumer | grep -i error")
                    if stdout:
                        st.code(stdout)
                    else:
                        st.info("目前沒有錯誤日誌")
    
    else:
        st.markdown("## 🔧 Scenario B: Performance Troubleshooting")
        st.markdown("### Learning Objectives")
        st.markdown("""
        1. 🐛 Introduce artificial latency and errors
        2. 📉 Observe metric degradation
        3. 🔍 Use logs to identify root cause
        4. 🔗 Trace request flow
        """)
        
        with st.expander("Step 1: Simulate Network Issues"):
            st.markdown("**Goal**: Pause Kafka service and observe impact")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("⏸️ Pause Kafka", key="pause_kafka_en"):
                    with st.spinner("Pausing Kafka service..."):
                        returncode, stdout, stderr = run_command("cd .. && docker compose pause kafka")
                        if returncode == 0:
                            st.success("✅ Kafka paused")
                            st.warning("⚠️ Producers and consumers will start reporting errors")
                        else:
                            st.error(f"❌ Failed to pause: {stderr}")
            
            with col2:
                if st.button("▶️ Resume Kafka", key="resume_kafka_en"):
                    with st.spinner("Resuming Kafka service..."):
                        returncode, stdout, stderr = run_command("cd .. && docker compose unpause kafka")
                        if returncode == 0:
                            st.success("✅ Kafka resumed")
                        else:
                            st.error(f"❌ Failed to resume: {stderr}")
        
        with st.expander("Step 2: Observe Error Logs"):
            st.markdown("**Goal**: See how applications handle connection errors")
            
            if st.button("📋 Check Consumer Errors", key="consumer_errors_en"):
                with st.spinner("Fetching error logs..."):
                    returncode, stdout, stderr = run_command("cd .. && docker compose logs --tail=30 python-consumer | grep -i error")
                    if stdout:
                        st.code(stdout)
                    else:
                        st.info("No error logs found currently")

# Scenario C: Failure Recovery
elif scenario_key == "scenario_c":
    if language == "繁體中文":
        st.markdown("## 🔄 情境 C: 故障復原")
        st.markdown("### 學習目標")
        st.markdown("""
        1. 🚨 模擬完整的服務故障
        2. 📊 監控叢集復原過程
        3. ⚖️ 分析消費者重新平衡
        4. ✅ 驗證資料一致性
        """)
        
        with st.expander("步驟 1: 服務重啟"):
            st.markdown("**目標**: 重啟服務並觀察復原")
            
            if st.button("🔄 重啟 Kafka", key="restart_kafka_zh"):
                with st.spinner("重啟 Kafka..."):
                    # Stop and start Kafka
                    run_command("cd .. && docker compose stop kafka")
                    time.sleep(5)
                    returncode, stdout, stderr = run_command("cd .. && docker compose start kafka")
                    if returncode == 0:
                        st.success("✅ Kafka 重啟完成")
                    else:
                        st.error(f"❌ 重啟失敗: {stderr}")
        
        with st.expander("步驟 2: 健康檢查"):
            if st.button("🩺 執行健康檢查", key="health_check_zh"):
                with st.spinner("檢查健康狀態..."):
                    # Check Kafka topics
                    returncode, stdout, stderr = run_command("cd .. && docker compose exec kafka kafka-topics --bootstrap-server localhost:9092 --list")
                    st.markdown("**Kafka Topics:**")
                    st.code(stdout)
    
    else:
        st.markdown("## 🔄 Scenario C: Failure Recovery")
        st.markdown("### Learning Objectives")
        st.markdown("""
        1. 🚨 Simulate complete service failure
        2. 📊 Monitor cluster recovery process
        3. ⚖️ Analyze consumer rebalancing
        4. ✅ Validate data consistency
        """)
        
        with st.expander("Step 1: Service Restart"):
            st.markdown("**Goal**: Restart services and observe recovery")
            
            if st.button("🔄 Restart Kafka", key="restart_kafka_en"):
                with st.spinner("Restarting Kafka..."):
                    # Stop and start Kafka
                    run_command("cd .. && docker compose stop kafka")
                    time.sleep(5)
                    returncode, stdout, stderr = run_command("cd .. && docker compose start kafka")
                    if returncode == 0:
                        st.success("✅ Kafka restart completed")
                    else:
                        st.error(f"❌ Restart failed: {stderr}")
        
        with st.expander("Step 2: Health Check"):
            if st.button("🩺 Run Health Check", key="health_check_en"):
                with st.spinner("Checking health..."):
                    # Check Kafka topics
                    returncode, stdout, stderr = run_command("cd .. && docker compose exec kafka kafka-topics --bootstrap-server localhost:9092 --list")
                    st.markdown("**Kafka Topics:**")
                    st.code(stdout)

# Scenario D: Scaling Operations
elif scenario_key == "scenario_d":
    if language == "繁體中文":
        st.markdown("## 📈 情境 D: 擴展營運")
        st.markdown("### 學習目標")
        st.markdown("""
        1. 📊 增加訊息負載
        2. 🔍 監控資源使用率
        3. ⚡ 動態擴展消費者
        4. 📈 觀察效能改善
        """)
        
        with st.expander("步驟 1: 擴展生產者"):
            st.markdown("**目標**: 增加生產者實例數量")
            
            scale_count = st.slider("Python Producer 實例數", 1, 5, 2)
            
            if st.button(f"📈 擴展到 {scale_count} 個實例", key="scale_prod_zh"):
                with st.spinner(f"擴展到 {scale_count} 個實例..."):
                    returncode, stdout, stderr = run_command(f"cd .. && docker compose up -d --scale python-producer={scale_count}")
                    if returncode == 0:
                        st.success(f"✅ 已擴展到 {scale_count} 個 Python Producer 實例")
                    else:
                        st.error(f"❌ 擴展失敗: {stderr}")
        
        with st.expander("步驟 2: 監控擴展效果"):
            if st.button("📊 檢查容器狀態", key="check_scaling_zh"):
                with st.spinner("檢查容器..."):
                    returncode, stdout, stderr = run_command("cd .. && docker compose ps | grep python-producer")
                    st.code(stdout)
    
    else:
        st.markdown("## 📈 Scenario D: Scaling Operations")
        st.markdown("### Learning Objectives")
        st.markdown("""
        1. 📊 Increase message load
        2. 🔍 Monitor resource utilization
        3. ⚡ Dynamically scale consumers
        4. 📈 Observe performance improvements
        """)
        
        with st.expander("Step 1: Scale Producers"):
            st.markdown("**Goal**: Increase producer instance count")
            
            scale_count = st.slider("Python Producer Instances", 1, 5, 2)
            
            if st.button(f"📈 Scale to {scale_count} instances", key="scale_prod_en"):
                with st.spinner(f"Scaling to {scale_count} instances..."):
                    returncode, stdout, stderr = run_command(f"cd .. && docker compose up -d --scale python-producer={scale_count}")
                    if returncode == 0:
                        st.success(f"✅ Scaled to {scale_count} Python Producer instances")
                    else:
                        st.error(f"❌ Scaling failed: {stderr}")
        
        with st.expander("Step 2: Monitor Scaling Effects"):
            if st.button("📊 Check Container Status", key="check_scaling_en"):
                with st.spinner("Checking containers..."):
                    returncode, stdout, stderr = run_command("cd .. && docker compose ps | grep python-producer")
                    st.code(stdout)

# Common utilities section
st.markdown("---")
if language == "繁體中文":
    st.markdown("### 🛠️ 常用工具")
else:
    st.markdown("### 🛠️ Common Utilities")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📋 All Logs" if language == "English" else "📋 所有日誌"):
        with st.spinner("Fetching all logs..." if language == "English" else "獲取所有日誌..."):
            returncode, stdout, stderr = run_command("cd .. && docker compose logs --tail=50")
            st.code(stdout[-5000:])  # Limit output size

with col2:
    if st.button("🔄 Restart All" if language == "English" else "🔄 重啟全部"):
        with st.spinner("Restarting all services..." if language == "English" else "重啟所有服務..."):
            returncode, stdout, stderr = run_command("cd .. && docker compose restart")
            if returncode == 0:
                st.success("✅ All services restarted" if language == "English" else "✅ 所有服務已重啟")
            else:
                st.error(f"❌ Restart failed: {stderr}")

with col3:
    if st.button("🧹 Clean Up" if language == "English" else "🧹 清理環境"):
        with st.spinner("Cleaning up..." if language == "English" else "清理中..."):
            returncode, stdout, stderr = run_command("cd .. && docker compose down")
            if returncode == 0:
                st.success("✅ Environment cleaned up" if language == "English" else "✅ 環境已清理")
            else:
                st.error(f"❌ Cleanup failed: {stderr}")

# Tips and best practices
st.markdown("---")
if language == "繁體中文":
    st.markdown("### 💡 提示與最佳實務")
    st.info("""
    **學習提示:**
    - 🎯 每個情境都有明確的學習目標，按順序完成效果最佳
    - 📊 在執行操作前後檢查 Grafana 儀表板
    - 📝 記錄觀察到的指標變化
    - 🔄 重複練習以加深理解
    """)
else:
    st.markdown("### 💡 Tips & Best Practices")
    st.info("""
    **Learning Tips:**
    - 🎯 Each scenario has clear learning objectives - follow them in order
    - 📊 Check Grafana dashboards before and after operations
    - 📝 Record the metric changes you observe
    - 🔄 Repeat exercises to deepen understanding
    """)

st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}") 