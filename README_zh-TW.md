# Kafka APM 與可觀測性解決方案示範

> **Apache Kafka 環境的應用程式效能監控 (APM) 與可觀測性模式示範，展示監控、告警與故障排除功能。**

**注意：這是一個概念驗證的示範專案，供學習與評估使用，若要用於正式環境需要進行大幅度的修改。**

## 執行摘要

此專案為 Kafka 營運團隊展示 **APM 解決方案概念**，說明如何實現 **Kafka 微服務架構的完整可見性**。此示範提供：

- **端到端可見性**：涵蓋生產者、消費者、代理伺服器和基礎設施的完整可觀測性
- **快速問題解決**：透過關聯的指標、日誌和追蹤，將平均修復時間從數小時縮短至數分鐘
- **主動監控**：提早偵測效能衰退和容量問題
- **多語言支援**：跨 Java、Python 和 Go 應用程式的統一可觀測性
- **現代可觀測性堆疊**：基於 OpenTelemetry 標準與經過驗證的開源工具

### 示範價值
- **展示縮短**故障排除時間的關聯遙測技術
- **顯示容量規劃**能力，包含趨勢分析和全面的指標
- **說明營運可見性**，提供全面的監控和告警
- **展示可觀測性模式**，用於自動化監控和提早問題偵測

---

## 系統架構

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

### 關鍵架構原則
- **集中化收集**：使用單一 OpenTelemetry Collector 收集所有遙測資料
- **廠商中立性**：基於標準的 OpenTelemetry 實作
- **可擴展性**：具備持久化儲存的水平可擴展元件
- **安全性**：可配置的認證與加密支援
- **高可用性**：具備健康檢查和自動復原的彈性設計

---

## 技術堆疊

### 應用程式監測層
| 元件 | 技術 | 用途 | 主要特色 |
|-----------|------------|---------|--------------|
| **Java Apps** | OpenTelemetry Java Agent | 自動監測 | 零程式碼監測、JVM 指標、Kafka 客戶端追蹤 |
| **Python Apps** | OpenTelemetry Python SDK | 手動監測 | 自訂指標、結構化日誌、非同步支援 |
| **Go Apps** | OpenTelemetry Go SDK | 手動監測 | 高效能追蹤、自訂指標、低負擔 |

### 訊息串流平台
| 元件 | 技術 | 用途 | 主要特色 |
|-----------|------------|---------|--------------|
| **Apache Kafka** | Confluent Platform | 訊息代理伺服器 | 高吞吐量、耐久性、基於分區的擴展 |
| **Zookeeper** | Apache Zookeeper | 協調服務 | 叢集協調、配置管理 |
| **JMX Exporters** | Prometheus JMX Exporter | 指標收集 | 代理伺服器指標、JVM 統計、主題指標 |

### 可觀測性基礎設施
| 元件 | 技術 | 用途 | 主要特色 |
|-----------|------------|---------|--------------|
| **OpenTelemetry Collector** | OTEL Collector Contrib | 遙測管道 | 資料收集、處理、路由、匯出 |
| **Prometheus** | Prometheus TSDB | 指標儲存 | 時間序列資料庫、PromQL 查詢、告警 |
| **Loki** | Grafana Loki | 日誌聚合 | 日誌索引、LogQL 查詢、標籤組織 |
| **Tempo** | Grafana Tempo | 追蹤儲存 | 分散式追蹤、追蹤關聯、取樣 |
| **Grafana** | Grafana | 視覺化 | 儀表板、告警、資料探索 |

### 開發與部署
| 元件 | 技術 | 用途 | 主要特色 |
|-----------|------------|---------|--------------|
| **Docker** | 容器執行環境 | 容器化 | 一致的環境、資源隔離 |
| **Docker Compose** | 編排工具 | 服務管理 | 多服務部署、網路、儲存卷 |
| **Streamlit** | Python Web 框架 | 示範介面 | 互動式教學、即時監控 |

---

## APM 與可觀測性資料流

### 可觀測性三大支柱

#### 指標管道
```
Applications → OpenTelemetry SDK → OTLP → Collector → Prometheus → Grafana
JMX Exporters → Prometheus Format → Collector → Prometheus → Grafana
```

**主要指標類別：**
- **應用程式指標**：訊息吞吐量、處理延遲、錯誤率
- **Kafka 代理伺服器指標**：主題大小、分區分佈、消費者延遲
- **基礎設施指標**：CPU、記憶體、磁碟使用量、網路 I/O
- **JVM 指標**：垃圾回收、堆積使用量、執行緒池

#### 日誌管道
```
Applications → OpenTelemetry SDK → OTLP → Collector → Loki → Grafana
Kafka Brokers → JSON Logs → Collector → Loki → Grafana
```

**日誌增強功能：**
- **追蹤關聯**：自動注入追蹤 ID
- **結構化日誌**：一致欄位的 JSON 格式
- **上下文傳播**：跨服務關聯
- **錯誤分類**：自動錯誤偵測與分類

#### 追蹤管道
```
Applications → OpenTelemetry SDK → OTLP → Collector → Tempo → Grafana
```

**分散式追蹤功能：**
- **端到端追蹤**：生產者 → Kafka → 消費者 spans
- **跨語言關聯**：跨 Java、Python、Go 的統一追蹤視圖
- **效能分析**：詳細的時間分析
- **依賴映射**：服務互動視覺化

### 資料關聯策略

此解決方案實作跨所有遙測類型的**全面關聯**：

1. **追蹤-指標關聯**：將特定追蹤連結到效能指標
2. **日誌-追蹤關聯**：在日誌中自動注入追蹤 ID
3. **服務映射**：自動發現服務依賴關係
4. **錯誤關聯**：在指標、日誌和追蹤間連結錯誤

---

## 快速入門指南

### 前置需求

**系統需求：**
- Docker Engine 20.10+ with Compose V2
- 4GB+ RAM（建議示範環境使用 8GB）
- 5GB+ 可用磁碟空間
- 網路存取以下載 Docker 映像檔

**驗證：**
```bash
# 驗證 Docker 和 Compose 安裝
docker --version          # 應為 20.10+
docker compose version     # 應為 v2.x+

# 檢查系統資源
free -h                    # 驗證可用 RAM
df -h                      # 驗證磁碟空間
```

### 部署步驟

1. **複製與設定**
   ```bash
   git clone <repository_url>
   cd kakfa-o11y
   chmod +x start.sh
   ```

2. **啟動環境**
   ```bash
   ./start.sh
   ```
   
   腳本將會：
   - 驗證系統前置需求
   - 建置應用程式容器
   - 部署所有服務
   - 執行健康檢查
   - 顯示存取 URL

3. **驗證部署**
   ```bash
   # 檢查服務健康狀態
   docker compose ps
   
   # 檢視啟動日誌
   docker compose logs -f --tail=50
   
   # 驗證 Kafka 連線
   docker compose exec kafka kafka-topics --bootstrap-server localhost:9092 --list
   ```

### 存取端點

| 服務 | URL | 認證資訊 | 用途 |
|---------|-----|-------------|---------|
| **Grafana** | http://localhost:3000 | admin/admin | 主要監控介面 |
| **Prometheus** | http://localhost:9090 | - | 指標探索 |
| **Demo App** | http://localhost:8501 | - | 互動式教學 |
| **OTel Collector** | http://localhost:13133/health | - | Collector 健康檢查 |

---

## 監控與可觀測性指南

### 預建儀表板

#### 1. **Kafka O11y Overview - Enhanced Broker Monitoring**
*包含 50+ 關鍵指標的主要營運儀表板*

**主要區塊：**
- **叢集健康狀態**：控制器狀態、分區狀態、複製健康度
- **效能指標**：吞吐量、延遲、請求率
- **資源使用率**：CPU、記憶體、磁碟、網路使用量
- **錯誤監控**：失敗請求、例外率、逾時追蹤
- **消費者群組**：延遲監控、位移管理
- **應用程式指標**：跨所有語言的生產者/消費者速率

### 基本監控情境

#### **情境 1：效能調查**
```bash
# 產生負載並觀察
docker compose logs -f python-producer
```

**在 Grafana 中：**
1. 導航至 "Kafka O11y Overview" 儀表板
2. 觀察即時訊息吞吐量
3. 檢查生產者/消費者延遲指標
4. 與 JVM 記憶體使用量關聯

**需要觀察的關鍵指標：**
- `rate(kafka_messages_sent_total[1m])` - Python 生產者吞吐量
- `rate(go_producer_messages_sent[1m])` - Go 生產者吞吐量  
- `kafka_network_request_total_time_ms_mean` - 請求延遲
- `jvm_memory_used_bytes{area="heap"}` - 記憶體使用量

#### **情境 2：錯誤偵測與根本原因分析**
```bash
# 模擬網路問題
docker compose pause kafka
docker compose logs python-consumer
docker compose unpause kafka
```

**調查步驟：**
1. **指標**：在儀表板中檢查錯誤率峰值
2. **日誌**：使用 Loki 尋找錯誤訊息
   ```
   {service_name="python-kafka-consumer"} |= "ERROR"
   ```
3. **追蹤**：在 Tempo 中識別失敗的追蹤
4. **關聯**：在三大支柱間連結錯誤

#### **情境 3：容量規劃**
**監控時間趨勢：**
- 磁碟使用增長率
- 消費者延遲趨勢
- 網路頻寬使用率
- JVM 垃圾回收頻率

**容量規劃的 PromQL 查詢：**
```promql
# 儲存增長率
increase(kafka_log_log_size_bytes[1h])

# 消費者延遲趨勢
kafka_consumer_lag_sum

# 網路使用率
rate(kafka_network_io_bytes_total[5m])
```

### 範例告警規則

#### 告警配置範例
```yaml
# 高消費者延遲
- alert: KafkaConsumerLagHigh
  expr: kafka_consumer_lag_sum > 1000
  for: 2m
  
# 代理伺服器離線
- alert: KafkaBrokerDown
  expr: kafka_controller_active_count == 0
  for: 30s
  
# 高錯誤率
- alert: ApplicationErrorRateHigh
  expr: rate(application_errors_total[5m]) > 0.1
  for: 1m
```

---

## 自訂與擴展指南

### 擴展考量

#### **水平擴展（示範）**
```yaml
# 擴展生產者/消費者用於測試
docker compose up --scale python-producer=3 --scale java-consumer=2

# 注意：此示範使用單一 Kafka 代理伺服器
# 多代理伺服器設定需要額外配置
```

#### **資源最佳化（範例）**
```yaml
# 測試用 JVM 設定範例
environment:
  JAVA_OPTS: >-
    -XX:+UseG1GC
    -XX:MaxGCPauseMillis=20
    -XX:InitiatingHeapOccupancyPercent=35
    -Xms512m -Xmx1g
```

### 安全考量（參考）

#### **認證與授權**
```yaml
# 啟用 SASL 認證
kafka:
  environment:
    KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: SASL_PLAINTEXT:SASL_PLAINTEXT
    KAFKA_SASL_ENABLED_MECHANISMS: PLAIN
    KAFKA_SASL_MECHANISM_INTER_BROKER_PROTOCOL: PLAIN
```

#### **TLS 加密**
```yaml
# 為 OTLP 通訊啟用 TLS
otel-collector:
  volumes:
    - ./certs:/etc/ssl/certs
  environment:
    OTEL_EXPORTER_OTLP_CERTIFICATE: /etc/ssl/certs/cert.pem
```

### 整合範例

#### **外部 Prometheus/Grafana**
```yaml
# 配置外部端點
otel-collector:
  environment:
    PROMETHEUS_REMOTE_WRITE_ENDPOINT: "https://your-prometheus.com/api/v1/write"
    GRAFANA_CLOUD_URL: "https://your-grafana-cloud.com"
```

#### **企業監控整合**
- **Datadog**：使用 OTLP 匯出器配置
- **New Relic**：配置 OTLP 端點
- **Splunk**：使用 Splunk HEC 匯出器
- **Elastic Stack**：配置 Elasticsearch 匯出器

---

## 示範情境與教學

### 指導式逐步說明

#### **情境 A：正常營運監控**
1. 啟動環境並觀察基準指標
2. 瀏覽 Grafana 儀表板
3. 了解正常效能模式
4. 設定基本告警規則

#### **情境 B：效能故障排除**
1. 引入人工延遲
2. 觀察指標衰退
3. 使用日誌識別根本原因
4. 追蹤請求在系統中的流程
5. 實作效能改善

#### **情境 C：故障復原**
1. 模擬代理伺服器故障
2. 監控叢集復原
3. 分析消費者重新平衡
4. 驗證資料一致性

#### **情境 D：擴展營運**
1. 增加訊息負載
2. 監控資源使用率
3. 動態擴展消費者
4. 觀察效能改善

### 互動式教學存取

訪問 **Streamlit Demo App** http://localhost:8501 獲得：
- 逐步指導情境
- 互動式指標探索
- 即時系統狀態
- 最佳實務文件

---

## 營運與維護

### 日常營運

#### **健康檢查程序**
```bash
# 個別服務檢查
docker compose exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092
curl -f http://localhost:13133/health  # OTel Collector
curl -f http://localhost:3000/api/health  # Grafana
```

#### **備份與復原**
```bash
# 備份 Grafana 儀表板
docker compose exec grafana grafana-cli admin export-dashboard

# 備份 Prometheus 資料
docker run --rm -v prometheus_data:/data alpine tar czf - /data

# 備份應用程式配置
tar czf config-backup.tar.gz grafana/ prometheus/ loki/ tempo/
```

### 故障排除指南

#### **常見問題與解決方案**

| 問題 | 症狀 | 解決方案 |
|-------|----------|----------|
| **高記憶體使用量** | OOM 錯誤、回應緩慢 | 增加容器記憶體限制 |
| **消費者延遲** | 處理延遲 | 擴展消費者或最佳化處理 |
| **網路問題** | 連線逾時 | 檢查 Docker 網路、防火牆規則 |
| **儲存增長** | 磁碟空間警告 | 實作保留政策 |

#### **診斷指令**
```bash
# 檢視詳細日誌
docker compose logs --tail=100 -f [service-name]

# 檢查資源使用量
docker stats

# 網路連線性
docker compose exec python-producer ping kafka

# Kafka 叢集狀態
docker compose exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092
```

---

## 效能基準

### 基準效能指標

#### **訊息吞吐量**
- **Java Producer**：~5,000-10,000 訊息/秒
- **Python Producer**：~1,000-2,000 訊息/秒  
- **Go Producer**：~8,000-15,000 訊息/秒

#### **資源使用率**
- **記憶體使用量**：完整堆疊總計 ~4-6GB
- **CPU 使用量**：典型負載下 ~1-2 核心
- **網路**：典型吞吐量 ~10-50MB/s
- **儲存**：日誌保留 ~100-500MB/天

#### **延遲特性**
- **端到端延遲**：P95 < 100ms
- **生產者延遲**：P95 < 50ms  
- **消費者處理**：P95 < 20ms

---

## API 參考

### OpenTelemetry 端點

| 端點 | 用途 | 連接埠 |
|----------|---------|------|
| `http://localhost:4317` | OTLP gRPC | 4317 |
| `http://localhost:4318` | OTLP HTTP | 4318 |
| `http://localhost:13133/health` | 健康檢查 | 13133 |
| `http://localhost:55679` | zPages | 55679 |

### Grafana API
```bash
# 建立儀表板
curl -X POST http://admin:admin@localhost:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d @dashboard.json

# 查詢指標
curl -X GET "http://admin:admin@localhost:3000/api/datasources/proxy/1/api/v1/query?query=up"
```

### Prometheus API
```bash
# 查詢指標
curl "http://localhost:9090/api/v1/query?query=kafka_messages_sent_total"

# 範圍查詢
curl "http://localhost:9090/api/v1/query_range?query=rate(kafka_messages_sent_total[5m])&start=2024-01-01T00:00:00Z&end=2024-01-01T01:00:00Z&step=15s"
```

---

## 執行測試

### 單元測試

#### **Java 應用程式**
```bash
cd java-producer && mvn test
cd java-consumer && mvn test
```

#### **Python 應用程式**  
```bash
cd python-producer && pytest -v
cd python-consumer && pytest -v
cd streamlit-app && pytest -v
```

#### **Go 應用程式**
```bash
cd go-producer && go test -v ./...
cd go-consumer && go test -v ./...
```

### 整合測試
```bash
# 手動整合測試 - 驗證所有服務正在執行
docker compose ps

# 檢查訊息流
docker compose logs -f python-producer | head -20
docker compose logs -f go-consumer | head -20
```

---

## 貢獻與支援

### 開發設定
```bash
# 複製儲存庫
git clone <repository_url>
cd kakfa-o11y

# 建置並在開發模式下執行
docker compose up --build
```

### 支援管道
- **Issues**：GitHub Issues 用於錯誤回報
- **Discussions**：GitHub Discussions 用於問題討論
- **Wiki**：詳細文件與範例

### 發展藍圖
- [ ] Kubernetes 部署清單
- [ ] 增強告警規則
- [ ] 自訂 Grafana 外掛
- [ ] 效能最佳化指南
- [ ] 多叢集監控

---

## 附錄

### 指標參考

#### **應用程式指標**
| 指標 | 類型 | 描述 | 標籤 |
|--------|------|-------------|--------|
| `kafka_messages_sent_total` | Counter | 已傳送訊息總數 (Python) | `status`, `language`, `component`, `topic`, `partition` |
| `go.producer.messages_sent` | Counter | 已傳送訊息總數 (Go) | `status` |
| `kafka_messages_sent_bytes_total` | Counter | 已傳送位元組總數 (Python) | `status`, `language`, `component`, `topic`, `partition` |
| `kafka_message_send_duration_ms` | Histogram | 傳送操作持續時間 (Python) | `status`, `language`, `component`, `topic`, `partition` |
| `kafka_producer_active` | UpDownCounter | 生產者狀態 (Python) | `status`, `language`, `component` |

#### **Kafka 代理伺服器指標**
| 指標 | 類型 | 描述 |
|--------|------|-------------|
| `kafka_controller_active_count` | Gauge | 活躍控制器計數 |
| `kafka_server_replica_manager_under_replicated_partitions` | Gauge | 複製不足的分區 |
| `kafka_network_request_total_time_ms_mean` | Gauge | 平均請求處理時間 |

### 環境變數參考

#### **OpenTelemetry 配置**
```bash
OTEL_SERVICE_NAME=your-service-name
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
OTEL_RESOURCE_ATTRIBUTES=deployment.environment=production
OTEL_METRICS_EXPORTER=otlp
OTEL_LOGS_EXPORTER=otlp
OTEL_TRACES_EXPORTER=otlp
```

#### **Kafka 配置**
```bash
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_AUTO_OFFSET_RESET=earliest
KAFKA_CONSUMER_GROUP_ID=your-consumer-group
```

---

**如有問題、議題或想要貢獻，請訪問我們的 [GitHub 儲存庫](https://github.com/your-org/kafka-o11y-demo)**

*此示範展示現代可觀測性模式，供教育和評估目的使用。若要部署至正式環境，需要進行大幅度的修改。* 