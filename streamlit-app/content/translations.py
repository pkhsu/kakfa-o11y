def get_text(language, key):
    # Fallback to English if the key is not found in the selected language
    return TRANSLATIONS.get(language, {}).get(key) or TRANSLATIONS.get("English", {}).get(key, f"Missing translation for {key}")

TRANSLATIONS = {
    "English": {
        # app.py
        "app_title": "Kafka APM & Observability Demo",
        "welcome_header": "Welcome to the Kafka Observability Demo!",
        "welcome_intro": """
This project is designed to showcase how to build a comprehensive monitoring, logging, and tracing solution for Kafka-based applications using the **OpenTelemetry** and **Grafana** ecosystems.

👈 **Select a page from the sidebar to get started.**
""",
        "project_goals_header": "🚀 Project Goals",
        "project_goals_content": """
- **End-to-End Observability**: Achieve full coverage of metrics, logs, and traces from producer to consumer.
- **Polyglot Support**: Demonstrate how to monitor applications written in different languages (Java, Python, Go).
- **Interactive Experience**: Provide a Streamlit application for live monitoring, scenario simulation, and data exploration.
- **Best Practices**: Apply observability design patterns like centralized collection and structured logging.
""",
        "ready_message": "The project is ready to go! All services should be running in Docker.",
        "before_you_begin_header": "✨ Before You Begin",
        "before_you_begin_content": "Make sure you have read the project's `README.md` and have run `docker-compose up -d` to start all services.",
        "language_select": "Choose a language:",

        # 1_Architecture.py
        "arch_title": "🏗️ System Architecture",
        "arch_overview_header": "Observability Architecture Overview",
        "arch_principles_header": "🎯 Key Architecture Principles",
        "arch_principle_central": "Centralized Collection",
        "arch_principle_central_desc": "Single OpenTelemetry Collector for all telemetry data",
        "arch_principle_vendor": "Vendor Neutrality",
        "arch_principle_vendor_desc": "Standards-based OpenTelemetry implementation",
        "arch_principle_scale": "Scalability",
        "arch_principle_scale_desc": "Horizontally scalable components with persistent storage",
        "arch_principle_security": "Security",
        "arch_principle_security_desc": "Configurable authentication and encryption support",
        "arch_principle_ha": "High Availability",
        "arch_principle_ha_desc": "Resilient design with health checks and automatic recovery",
        "data_flow_header": "🌊 Data Flow Architecture",
        "perf_header": "⚡ Performance Characteristics",
        "perf_component": "Component",
        "perf_throughput": "Expected Throughput",
        "perf_latency": "Latency (P95)",
        "perf_memory": "Memory Usage",

        # 0_Tutorial_Introduction.py
        "intro_title": "Tutorial Introduction",
        "intro_markdown": """
This interactive tutorial is designed to guide you through the **Kafka APM & Observability Solution Demo**. 
You will learn about the system architecture, technology stack, and how to use the monitoring tools to troubleshoot performance issues.
""",
        "intro_info": "Please proceed through the pages in the sidebar to complete the tutorial. We recommend starting with the 'Architecture' page.",
        "intro_structure_header": "Tutorial Structure",
        "intro_structure_content": """
- **Architecture**: Understand the overall system design.
- **Tech Stack**: Learn about the technologies used.
- **Live Dashboard**: See the Grafana dashboard in action.
- **Demo Scenarios**: Run interactive scenarios to simulate real-world situations.
- **And more...**
""",
        "intro_prereq_header": "Prerequisites",
        "intro_prereq_content": """
- **Docker**: Ensure Docker and Docker Compose are installed and running.
- **Project Files**: You should have the project files cloned to your local machine.
- **Basic Kafka Knowledge**: Familiarity with basic Kafka concepts is helpful but not required.
""",

        # 2_Tech_Stack.py
        "tech_stack_title": "🔧 Technology Stack",
        "tech_app_layer": "📱 Application Instrumentation Layer",
        "tech_component": "Component",
        "tech_technology": "Technology",
        "tech_purpose": "Purpose",
        "tech_features": "Key Features",
        "tech_java_apps": "Java Apps",
        "tech_python_apps": "Python Apps",
        "tech_go_apps": "Go Apps",
        "tech_java_agent": "OpenTelemetry Java Agent",
        "tech_python_sdk": "OpenTelemetry Python SDK",
        "tech_go_sdk": "OpenTelemetry Go SDK",
        "tech_auto_instrument": "Auto-instrumentation",
        "tech_manual_instrument": "Manual instrumentation",
        "tech_java_features": "Zero-code instrumentation, JVM metrics, Kafka client tracing",
        "tech_python_features": "Custom metrics, structured logging, async support",
        "tech_go_features": "High-performance tracing, custom metrics, low overhead",
        "tech_streaming_platform": "📨 Message Streaming Platform",
        "tech_kafka": "Apache Kafka",
        "tech_zookeeper": "Zookeeper",
        "tech_jmx": "JMX Exporters",
        "tech_confluent": "Confluent Platform",
        "tech_apache_zookeeper": "Apache Zookeeper",
        "tech_prometheus_jmx": "Prometheus JMX Exporter",
        "tech_broker": "Message Broker",
        "tech_coordination": "Coordination Service",
        "tech_metrics_collection": "Metrics Collection",
        "tech_kafka_features": "High throughput, durability, partition-based scaling",
        "tech_zookeeper_features": "Cluster coordination, configuration management",
        "tech_jmx_features": "Broker metrics, JVM stats, topic metrics",
        "tech_obs_infra": "👁️ Observability Infrastructure",
        "tech_otel_collector": "OpenTelemetry Collector",
        "tech_prometheus": "Prometheus",
        "tech_loki": "Loki",
        "tech_tempo": "Tempo",
        "tech_grafana": "Grafana",
        "tech_otel_contrib": "OTEL Collector Contrib",
        "tech_prometheus_tsdb": "Prometheus TSDB",
        "tech_grafana_loki": "Grafana Loki",
        "tech_grafana_tempo": "Grafana Tempo",
        "tech_grafana_viz": "Grafana",
        "tech_pipeline": "Telemetry Pipeline",
        "tech_metrics_storage": "Metrics Storage",
        "tech_log_aggregation": "Log Aggregation",
        "tech_trace_storage": "Trace Storage",
        "tech_visualization": "Visualization",
        "tech_otel_features": "Data collection, processing, routing, export",
        "tech_prometheus_features": "Time-series database, PromQL queries, alerting",
        "tech_loki_features": "Log indexing, LogQL queries, label-based organization",
        "tech_tempo_features": "Distributed tracing, trace correlation, sampling",
        "tech_grafana_features": "Dashboards, alerting, data exploration",

        # 3_Live_Dashboard.py
        "dashboard_title": "📊 Live System Dashboard",
        "dashboard_header": "Real-time Monitoring & Metrics",
        "auto_refresh": "Auto-refresh (30s)",
        "service_status": "🚥 Service Status",
        "prometheus_status": "Prometheus",
        "grafana_status": "Grafana",
        "otel_collector_status": "OTel Collector",
        "kafka_status": "Kafka",
        "running": "Running",
        "down": "Down",
        "key_metrics": "📈 Key Metrics",
        "throughput_tab": "Message Throughput",
        "latency_tab": "Latency Metrics",
        "resources_tab": "System Resources",
        "errors_tab": "Error Rates",
        "producer_throughput_header": "📤 Producer Throughput",
        "python_producer_service": "Python Producer",
        "go_producer_service": "Go Producer",
        "current_throughput_title": "Current Throughput",
        "no_throughput_data": "No throughput data available",
        "no_producer_metrics": "No producer metrics found",
        "consumer_lag_header": "📥 Consumer Lag",
        "consumer_lag_title": "Consumer Lag",
        "no_consumer_lag_data": "No consumer lag data",
        "latency_header": "⏱️ Network Request Latency",
        "latency_chart_title": "Request Latency (Last Hour)",
        "current_latency_metric": "Current Latency",
        "no_latency_data": "No latency data available",
        "resources_cpu_header": "💻 CPU Usage",
        "resources_cpu_chart_title": "CPU Usage (Last Hour)",
        "no_cpu_data": "No CPU usage data available",
        "resources_memory_header": "🧠 Memory Usage",
        "resources_memory_chart_title": "Memory Usage (Last Hour)",
        "no_memory_data": "No memory usage data available",
        "error_rates_header": "🔥 Error Rates",
        "error_rates_chart_title": "Application Error Rate (Last 5m)",
        "no_error_data": "No error rate data available",

        # 4_Demo_Scenarios.py
        "scenarios_title": "🎮 Interactive Demo Scenarios",
        "scenarios_header": "Hands-on Learning Scenarios",
        "choose_scenario": "🎯 Choose Learning Scenario",
        "select_scenario": "Select a scenario:",
        "scenario_a_title": "Scenario A: Normal Operations Monitoring",
        "scenario_b_title": "Scenario B: Performance Troubleshooting",
        "scenario_c_title": "Scenario C: Failure Recovery",
        "scenario_d_title": "Scenario D: Scaling Operations",

        "scenario_a_header": "🎯 Scenario A: Normal Operations Monitoring",
        "scenario_a_objectives_header": "Learning Objectives",
        "scenario_a_objectives_content": """
1.  🚀 Launch complete observability environment
2.  📊 Understand baseline performance metrics
3.  🔍 Explore Grafana dashboards
4.  🚨 Set up basic alerting rules
""",
        "scenario_a_guide_header": "📝 Step-by-Step Guide",
        "scenario_a_step1_header": "Step 1: Environment Launch",
        "scenario_a_step1_goal": "**Goal**: Start all services and verify status",
        "scenario_a_step1_button": "🚀 Start Environment",
        "scenario_a_step1_spinner": "Starting services...",
        "scenario_a_step1_success": "✅ Environment started successfully!",
        "scenario_a_step1_error": "❌ Failed to start:",
        "scenario_a_step1_manual": """
# Manual start commands
cd kakfa-o11y
./start.sh

# Or use Docker Compose directly
docker compose up -d
""",
        "scenario_a_step2_header": "Step 2: Service Status Check",
        "scenario_a_step2_goal": "**Goal**: Confirm all services are running properly",
        "scenario_a_step2_button": "🔍 Check Service Status",
        "scenario_a_step2_spinner": "Checking services...",
        "scenario_a_step2_service_col": "Service",
        "scenario_a_step2_status_col": "Status",
        "scenario_a_step3_header": "Step 3: Observe Producer/Consumer Activity",
        "scenario_a_step3_goal": "**Goal**: Watch message flow and baseline metrics",
        "scenario_a_step3_producer_button": "📤 Watch Python Producer",
        "scenario_a_step3_consumer_button": "📥 Watch Go Consumer",
        "scenario_a_step3_spinner": "Fetching logs...",
        "scenario_a_step4_header": "Step 4: Grafana Dashboard Exploration",
        "scenario_a_step4_goal": "**Goal**: Familiarize with monitoring interface",
        "scenario_a_step4_access_header": "📊 Access Information",
        "scenario_a_step4_url": "- URL: http://localhost:3000",
        "scenario_a_step4_user": "- Username: admin",
        "scenario_a_step4_pass": "- Password: admin",
        "scenario_a_step4_button": "🔗 Open Grafana",
        "scenario_a_step4_link": "[Click to Open Grafana](http://localhost:3000)",
        "scenario_a_step4_info": "💡 Please change default password after first login",

        "scenario_b_header": "🔧 Scenario B: Performance Troubleshooting",
        "scenario_b_objectives_header": "Learning Objectives",
        "scenario_b_objectives_content": """
1.  🐛 Introduce artificial latency and errors
2.  📉 Observe metric degradation
3.  🔍 Use logs to identify root cause
4.  🔗 Trace request flow
""",
        "scenario_b_step1_header": "Step 1: Simulate Network Issues",
        "scenario_b_step1_goal": "**Goal**: Pause Kafka service and observe impact",
        "scenario_b_step1_pause_button": "⏸️ Pause Kafka",
        "scenario_b_step1_pause_spinner": "Pausing Kafka service...",
        "scenario_b_step1_pause_success": "✅ Kafka paused.",
        "scenario_b_step1_pause_error": "❌ Failed to pause Kafka:",
        "scenario_b_step1_unpause_button": "⏯️ Unpause Kafka",
        "scenario_b_step1_unpause_spinner": "Unpausing Kafka service...",
        "scenario_b_step1_unpause_success": "✅ Kafka unpaused.",
        "scenario_b_step1_unpause_error": "❌ Failed to unpause Kafka:",

        "scenario_c_header": "💥 Scenario C: Failure Recovery",
        "scenario_c_objectives_header": "Learning Objectives",
        "scenario_c_objectives_content": """
1.  🔥 Simulate a broker failure
2.  🔄 Monitor cluster recovery
3.  ⚖️ Analyze consumer rebalancing
4.  ✅ Validate data consistency
""",
        "scenario_c_step1_header": "Step 1: Simulate Broker Failure",
        "scenario_c_step1_goal": "**Goal**: Stop the Kafka container and observe recovery",
        "scenario_c_step1_stop_button": "🔥 Stop Kafka Broker",
        "scenario_c_step1_stop_spinner": "Stopping Kafka broker...",
        "scenario_c_step1_stop_success": "✅ Kafka broker stopped.",
        "scenario_c_step1_stop_error": "❌ Failed to stop Kafka:",
        "scenario_c_step1_start_button": "♻️ Restart Kafka Broker",
        "scenario_c_step1_start_spinner": "Restarting Kafka broker...",
        "scenario_c_step1_start_success": "✅ Kafka broker restarted.",
        "scenario_c_step1_start_error": "❌ Failed to restart Kafka:",

        "scenario_d_header": "📈 Scenario D: Scaling Operations",
        "scenario_d_objectives_header": "Learning Objectives",
        "scenario_d_objectives_content": """
1.  📈 Increase message load
2.  📊 Monitor resource utilization
3.  ⚙️ Scale consumers dynamically
4.  🚀 Observe performance improvements
""",
        "scenario_d_step1_header": "Step 1: Scale Consumers",
        "scenario_d_step1_goal": "**Goal**: Increase the number of consumer instances",
        "scenario_d_step1_label": "Number of Python Consumers",
        "scenario_d_step1_button": "⚙️ Scale Consumers",
        "scenario_d_step1_spinner": "Scaling consumers...",
        "scenario_d_step1_success": "✅ Consumers scaled successfully!",
        "scenario_d_step1_error": "❌ Failed to scale consumers:",

        # 6_API_Reference.py
        "api_ref_title": "🔗 API & Endpoint Reference",
        "api_ref_header": "This section provides the main service endpoints used in this demo.",
        "api_ref_obs_header": "👁️ Observability Services",
        "api_ref_obs_content": """
- **Grafana**: [http://localhost:3000](http://localhost:3000)
  - *User*: `admin`
  - *Password*: `grafana`
- **Prometheus**: [http://localhost:9090](http://localhost:9090)
- **Loki**: (Accessed via Grafana)
- **Tempo**: (Accessed via Grafana)
""",
        "api_ref_kafka_header": "📨 Kafka Services",
        "api_ref_kafka_content": """
- **Kafka Broker**: `kafka:9092` (internal to Docker network)
- **Zookeeper**: `zookeeper:2181` (internal to Docker network)
- **JMX Exporter (Kafka)**: `jmx-exporter-kafka:5556`
- **JMX Exporter (Zookeeper)**: `jmx-exporter-zookeeper:5557`
""",
        "api_ref_otel_header": "🔭 OpenTelemetry Collector",
        "api_ref_otel_content": """
- **gRPC Endpoint**: `otel-collector:4317`
- **HTTP Endpoint**: `otel-collector:4318`
""",

        # 7_Troubleshooting.py
        "troubleshooting_title": "🛠️ Troubleshooting",
        "troubleshooting_header": "🚫 Common Issues & Solutions",
        "issue_services_fail_header": "Services fail to start or keep restarting",
        "issue_services_fail_content": """
- **Check Docker Resources**: Ensure Docker Desktop has enough memory allocated (>8GB recommended).
- **Check Port Conflicts**: Make sure ports `3000`, `8501`, `9090`, etc., are not in use.
- **View Logs**: `docker compose logs [service_name]`
- **Prune Old Containers**: `docker compose down -v`
""",
        "issue_no_data_header": "No data in Grafana",
        "issue_no_data_content": """
- **Check Prometheus**: Browse to `http://localhost:9090` and check if targets are up.
- **Check Datasource**: Verify the Prometheus datasource is correctly configured in Grafana (`http://prometheus:9090`).
- **Wait for Data**: Allow a few minutes for applications to generate telemetry.
- **Check Collector Logs**: `docker compose logs otel-collector`
""",
        "issue_streamlit_error_header": "Errors on Streamlit page",
        "issue_streamlit_error_content": """
- **Check Streamlit Logs**: `docker compose logs streamlit-app`
- **Check Dependencies**: Ensure packages in `requirements.txt` were installed successfully.
- **Rebuild the Image**: `docker compose up -d --build streamlit-app`
""",
        "troubleshooting_info": "If problems persist, please open an issue on the project's GitHub repository.",
    },
    "繁體中文": {
        # app.py
        "app_title": "Kafka APM 與可觀測性示範",
        "welcome_header": "歡迎來到 Kafka 可觀測性示範！",
        "welcome_intro": """
本專案旨在展示如何使用 **OpenTelemetry** 與 **Grafana** 生態系，為基於 Kafka 的應用程式建構一個全面的監控、日誌與追蹤解決方案。

👈 **請從側邊欄選擇一個頁面開始。**
""",
        "project_goals_header": "🚀 專案目標",
        "project_goals_content": """
- **端到端可觀測性**: 實現從生產者到消費者的指標、日誌與追蹤全覆蓋。
- **多語言支援**: 展示如何監控以不同語言（Java、Python、Go）編寫的應用程式。
- **互動式體驗**: 提供一個 Streamlit 應用程式，用於即時監控、情境模擬與資料探索。
- **最佳實踐**: 應用可觀測性設計模式，如集中收集與結構化日誌。
""",
        "ready_message": "專案已準備就緒！所有服務應已在 Docker 中運行。",
        "before_you_begin_header": "✨ 開始之前",
        "before_you_begin_content": "請確保您已閱讀專案的 `README.md` 並已執行 `docker-compose up -d` 來啟動所有服務。",
        "language_select": "選擇語言：",

        # 1_Architecture.py
        "arch_title": "🏗️ 系統架構",
        "arch_overview_header": "可觀測性架構總覽",
        "arch_principles_header": "🎯 關鍵架構原則",
        "arch_principle_central": "集中化收集",
        "arch_principle_central_desc": "使用單一 OpenTelemetry Collector 收集所有遙測資料",
        "arch_principle_vendor": "廠商中立性",
        "arch_principle_vendor_desc": "基於標準的 OpenTelemetry 實作",
        "arch_principle_scale": "可擴展性",
        "arch_principle_scale_desc": "具備持久化儲存的水平可擴展元件",
        "arch_principle_security": "安全性",
        "arch_principle_security_desc": "可配置的認證與加密支援",
        "arch_principle_ha": "高可用性",
        "arch_principle_ha_desc": "具備健康檢查和自動復原的彈性設計",
        "data_flow_header": "🌊 資料流架構",
        "perf_header": "⚡ 效能特性",
        "perf_component": "元件",
        "perf_throughput": "預期吞吐量",
        "perf_latency": "延遲 (P95)",
        "perf_memory": "記憶體使用量",

        # 0_Tutorial_Introduction.py
        "intro_title": "教學簡介",
        "intro_markdown": """
本互動式教學旨在引導您完成 **Kafka APM 與可觀測性解決方案示範**。
您將學習系統架構、技術堆疊，以及如何使用監控工具來排解效能問題。
""",
        "intro_info": "請依序瀏覽側邊欄中的頁面以完成教學。我們建議從「架構」頁面開始。",
        "intro_structure_header": "教學結構",
        "intro_structure_content": """
- **架構**: 了解整體系統設計。
- **技術堆疊**: 了解所使用的技術。
- **即時儀表板**: 查看 Grafana 儀表板的實際運作。
- **示範情境**: 執行互動式情境以模擬真實世界的情況。
- **還有更多...**
""",
        "intro_prereq_header": "前置需求",
        "intro_prereq_content": """
- **Docker**: 確保 Docker 與 Docker Compose 已安裝並正在運行。
- **專案檔案**: 您應已將專案檔案複製到本機。
- **基礎 Kafka 知識**: 熟悉基礎 Kafka 概念會有所幫助，但非必要。
""",

        # 2_Tech_Stack.py
        "tech_stack_title": "🔧 技術堆疊",
        "tech_app_layer": "📱 應用程式監測層",
        "tech_component": "元件",
        "tech_technology": "技術",
        "tech_purpose": "用途",
        "tech_features": "主要特色",
        "tech_java_apps": "Java 應用程式",
        "tech_python_apps": "Python 應用程式",
        "tech_go_apps": "Go 應用程式",
        "tech_java_agent": "OpenTelemetry Java Agent",
        "tech_python_sdk": "OpenTelemetry Python SDK",
        "tech_go_sdk": "OpenTelemetry Go SDK",
        "tech_auto_instrument": "自動監測",
        "tech_manual_instrument": "手動監測",
        "tech_java_features": "零程式碼監測、JVM 指標、Kafka 客戶端追蹤",
        "tech_python_features": "自訂指標、結構化日誌、非同步支援",
        "tech_go_features": "高效能追蹤、自訂指標、低負擔",
        "tech_streaming_platform": "📨 訊息串流平台",
        "tech_kafka": "Apache Kafka",
        "tech_zookeeper": "Zookeeper",
        "tech_jmx": "JMX Exporters",
        "tech_confluent": "Confluent Platform",
        "tech_apache_zookeeper": "Apache Zookeeper",
        "tech_prometheus_jmx": "Prometheus JMX Exporter",
        "tech_broker": "訊息代理伺服器",
        "tech_coordination": "協調服務",
        "tech_metrics_collection": "指標收集",
        "tech_kafka_features": "高吞吐量、耐久性、基於分區的擴展",
        "tech_zookeeper_features": "叢集協調、配置管理",
        "tech_jmx_features": "代理伺服器指標、JVM 統計、主題指標",
        "tech_obs_infra": "👁️ 可觀測性基礎設施",
        "tech_otel_collector": "OpenTelemetry Collector",
        "tech_prometheus": "Prometheus",
        "tech_loki": "Loki",
        "tech_tempo": "Tempo",
        "tech_grafana": "Grafana",
        "tech_otel_contrib": "OTEL Collector Contrib",
        "tech_prometheus_tsdb": "Prometheus TSDB",
        "tech_grafana_loki": "Grafana Loki",
        "tech_grafana_tempo": "Grafana Tempo",
        "tech_grafana_viz": "Grafana",
        "tech_pipeline": "遙測管道",
        "tech_metrics_storage": "指標儲存",
        "tech_log_aggregation": "日誌聚合",
        "tech_trace_storage": "追蹤儲存",
        "tech_visualization": "視覺化",
        "tech_otel_features": "資料收集、處理、路由、匯出",
        "tech_prometheus_features": "時間序列資料庫、PromQL 查詢、告警",
        "tech_loki_features": "日誌索引、LogQL 查詢、標籤組織",
        "tech_tempo_features": "分散式追蹤、追蹤關聯、取樣",
        "tech_grafana_features": "儀表板、告警、資料探索",

        # 4_Demo_Scenarios.py
        "scenarios_title": "🎮 互動式示範情境",
        "scenarios_header": "動手學習情境",
        "choose_scenario": "🎯 選擇學習情境",
        "select_scenario": "選擇情境:",
        "scenario_a_title": "情境 A: 正常營運監控",
        "scenario_b_title": "情境 B: 效能故障排除",
        "scenario_c_title": "情境 C: 故障復原",
        "scenario_d_title": "情境 D: 擴展營運",

        "scenario_a_header": "🎯 情境 A: 正常營運監控",
        "scenario_a_objectives_header": "學習目標",
        "scenario_a_objectives_content": """
1.  🚀 啟動完整的可觀測性環境
2.  📊 了解基準效能指標
3.  🔍 探索 Grafana 儀表板
4.  🚨 設定基本告警規則
""",
        "scenario_a_guide_header": "📝 逐步指導",
        "scenario_a_step1_header": "步驟 1: 環境啟動",
        "scenario_a_step1_goal": "**目標**: 啟動所有服務並驗證狀態",
        "scenario_a_step1_button": "🚀 啟動環境",
        "scenario_a_step1_spinner": "正在啟動服務...",
        "scenario_a_step1_success": "✅ 環境啟動成功!",
        "scenario_a_step1_error": "❌ 啟動失敗:",
        "scenario_a_step1_manual": """
# 手動啟動指令
cd kakfa-o11y
./start.sh

# 或使用 Docker Compose
docker compose up -d
""",
        "scenario_a_step2_header": "步驟 2: 服務狀態檢查",
        "scenario_a_step2_goal": "**目標**: 確認所有服務正常運行",
        "scenario_a_step2_button": "🔍 檢查服務狀態",
        "scenario_a_step2_spinner": "檢查服務中...",
        "scenario_a_step2_service_col": "服務",
        "scenario_a_step2_status_col": "狀態",
        "scenario_a_step3_header": "步驟 3: 觀察生產者/消費者活動",
        "scenario_a_step3_goal": "**目標**: 觀察訊息流和基準指標",
        "scenario_a_step3_producer_button": "📤 觀察 Python Producer",
        "scenario_a_step3_consumer_button": "📥 觀察 Go Consumer",
        "scenario_a_step3_spinner": "獲取日誌...",
        "scenario_a_step4_header": "步驟 4: Grafana 儀表板探索",
        "scenario_a_step4_goal": "**目標**: 熟悉監控介面",
        "scenario_a_step4_access_header": "📊 存取資訊:",
        "scenario_a_step4_url": "- URL: http://localhost:3000",
        "scenario_a_step4_user": "- 帳號: admin",
        "scenario_a_step4_pass": "- 密碼: admin",
        "scenario_a_step4_button": "🔗 開啟 Grafana",
        "scenario_a_step4_link": "[點擊開啟 Grafana](http://localhost:3000)",
        "scenario_a_step4_info": "💡 首次登入後請更改預設密碼",

        "scenario_b_header": "🔧 情境 B: 效能故障排除",
        "scenario_b_objectives_header": "學習目標",
        "scenario_b_objectives_content": """
1.  🐛 引入人工延遲和錯誤
2.  📉 觀察指標衰退
3.  🔍 使用日誌識別根本原因
4.  🔗 追蹤請求流程
""",
        "scenario_b_step1_header": "步驟 1: 模擬網路問題",
        "scenario_b_step1_goal": "**目標**: 暫停 Kafka 服務並觀察影響",
        "scenario_b_step1_pause_button": "⏸️ 暫停 Kafka",
        "scenario_b_step1_pause_spinner": "暫停 Kafka 服務...",
        "scenario_b_step1_pause_success": "✅ Kafka 已暫停。",
        "scenario_b_step1_pause_error": "❌ 暫停 Kafka 失敗:",
        "scenario_b_step1_unpause_button": "⏯️ 恢復 Kafka",
        "scenario_b_step1_unpause_spinner": "恢復 Kafka 服務...",
        "scenario_b_step1_unpause_success": "✅ Kafka 已恢復。",
        "scenario_b_step1_unpause_error": "❌ 恢復 Kafka 失敗:",

        "scenario_c_header": "💥 情境 C: 故障復原",
        "scenario_c_objectives_header": "學習目標",
        "scenario_c_objectives_content": """
1.  🔥 模擬代理伺服器故障
2.  🔄 監控叢集復原
3.  ⚖️ 分析消費者重新平衡
4.  ✅ 驗證資料一致性
""",
        "scenario_c_step1_header": "步驟 1: 模擬代理伺服器故障",
        "scenario_c_step1_goal": "**目標**: 停止 Kafka 容器並觀察復原情況",
        "scenario_c_step1_stop_button": "🔥 停止 Kafka 代理伺服器",
        "scenario_c_step1_stop_spinner": "正在停止 Kafka 代理伺服器...",
        "scenario_c_step1_stop_success": "✅ Kafka 代理伺服器已停止。",
        "scenario_c_step1_stop_error": "❌ 停止 Kafka 失敗:",
        "scenario_c_step1_start_button": "♻️ 重啟 Kafka 代理伺服器",
        "scenario_c_step1_start_spinner": "正在重啟 Kafka 代理伺服器...",
        "scenario_c_step1_start_success": "✅ Kafka 代理伺服器已重啟。",
        "scenario_c_step1_start_error": "❌ 重啟 Kafka 失敗:",

        "scenario_d_header": "📈 情境 D: 擴展營運",
        "scenario_d_objectives_header": "學習目標",
        "scenario_d_objectives_content": """
1.  📈 增加訊息負載
2.  📊 監控資源使用率
3.  ⚙️ 動態擴展消費者
4.  🚀 觀察效能改善
""",
        "scenario_d_step1_header": "步驟 1: 擴展消費者",
        "scenario_d_step1_goal": "**目標**: 增加消費者實例的數量",
        "scenario_d_step1_label": "Python 消費者數量",
        "scenario_d_step1_button": "⚙️ 擴展消費者",
        "scenario_d_step1_spinner": "正在擴展消費者...",
        "scenario_d_step1_success": "✅ 消費者擴展成功!",
        "scenario_d_step1_error": "❌ 消費者擴展失敗:",

        # 6_API_Reference.py
        "api_ref_title": "🔗 API & 端點參考",
        "api_ref_header": "此處提供在此示範中使用的主要服務端點。",
        "api_ref_obs_header": "👁️ 可觀測性服務",
        "api_ref_obs_content": """
- **Grafana**: [http://localhost:3000](http://localhost:3000)
  - *使用者*: `admin`
  - *密碼*: `grafana`
- **Prometheus**: [http://localhost:9090](http://localhost:9090)
- **Loki**: (透過 Grafana 存取)
- **Tempo**: (透過 Grafana 存取)
""",
        "api_ref_kafka_header": "📨 Kafka 服務",
        "api_ref_kafka_content": """
- **Kafka 代理伺服器**: `kafka:9092` (Docker 網路內部)
- **Zookeeper**: `zookeeper:2181` (Docker 網路內部)
- **JMX Exporter (Kafka)**: `jmx-exporter-kafka:5556`
- **JMX Exporter (Zookeeper)**: `jmx-exporter-zookeeper:5557`
""",
        "api_ref_otel_header": "🔭 OpenTelemetry Collector",
        "api_ref_otel_content": """
- **gRPC 端點**: `otel-collector:4317`
- **HTTP 端點**: `otel-collector:4318`
""",

        # 7_Troubleshooting.py
        "troubleshooting_title": "🛠️ 問題排解",
        "troubleshooting_header": "🚫 常見問題與解決方案",
        "issue_services_fail_header": "服務無法啟動或持續重啟",
        "issue_services_fail_content": """
- **檢查 Docker 資源**: 確保 Docker Desktop 分配了足夠的記憶體（建議 >8GB）。
- **檢查埠號衝突**: 確保 `3000`, `8501`, `9090` 等埠號未被其他應用程式占用。
- **查看日誌**: `docker compose logs [service_name]`
- **清除舊容器**: `docker compose down -v`
""",
        "issue_no_data_header": "Grafana 中沒有資料",
        "issue_no_data_content": """
- **檢查 Prometheus**: 瀏覽 `http://localhost:9090` 確認目標是否正常。
- **檢查資料來源**: 在 Grafana 中確認 Prometheus 資料來源設定正確 (`http://prometheus:9090`)。
- **等待資料產生**: 啟動後需要幾分鐘時間讓應用程式產生遙測資料。
- **檢查 Collector 日誌**: `docker compose logs otel-collector`
""",
        "issue_streamlit_error_header": "Streamlit 頁面錯誤",
        "issue_streamlit_error_content": """
- **查看 Streamlit 日誌**: `docker compose logs streamlit-app`
- **檢查相依套件**: `requirements.txt` 中的套件是否安裝成功。
- **重建立映像檔**: `docker compose up -d --build streamlit-app`
""",
        "troubleshooting_info": "如果問題仍然存在，請在專案的 GitHub Issues 中提出。",
    }
} 