# Kafka O11y Dashboard 監控指標說明

> **目標對象**：開發團隊、運維人員、系統監控負責人  
> **更新時間**：2024年1月  
> **Dashboard 位置**：Grafana → Kafka O11y Tutorial Overview - Enhanced Monitoring & Error Analysis

---

## Dashboard 面板總覽

| 面板編號 | 面板名稱 | 主要功能 | 重要程度 |
|---------|---------|---------|---------|
| 1 | Kafka Cluster Health Overview | 集群整體健康狀態 | Critical |
| 2 | Message Throughput | 消息吞吐量監控 | High |
| 3 | Network Performance | 網路性能監控 | High |
| 4 | Topic & Controller Metrics | 主題和控制器狀態 | Medium |
| 5 | Leader & Log Metrics | 領導者和日誌狀態 | Medium |
| 6 | Request Handling | 請求處理性能 | High |
| 7 | Error & Failure Rates | 錯誤率監控 | Critical |
| 8 | Consumer Lag & Processing | 消費者延遲監控 | Critical |
| 9 | JVM & Resource Utilization | JVM 資源使用 | High |
| 10 | Application Producers | 應用層生產者指標 | Medium |
| 11 | Application Consumers | 應用層消費者指標 | Medium |
| 12 | OTel Collector Throughput | 遙測數據收集器 | Medium |

---

## 詳細面板說明

### 1. **Kafka Cluster Health Overview** (集群健康總覽)
**用途**：一眼判斷 Kafka 集群是否健康運行

| 指標名稱 | 正常值 | 異常值 | 說明 |
|---------|-------|-------|------|
| **Active Controllers** | 1 | 0 或 >1 | 活躍控制器數量，應該正好是 1 個 |
| **Offline Partitions** | 0 | >0 | 離線分區數，任何 >0 都表示數據不可用 |
| **Under-replicated Partitions** | 0 | >0 | 副本不足的分區，影響數據安全性 |
| **Replica Imbalance** | 0 | >10 | 副本分佈不均，可能影響性能 |

**關鍵告警**：如果 Active Controllers ≠ 1 或其他指標 > 0，需要立即檢查

---

### 2. **Kafka Broker: Message Throughput** (消息吞吐量)
**用途**：監控 Kafka 集群的數據流量

| 指標名稱 | 單位 | 說明 | 正常範圍 |
|---------|-----|------|--------|
| **Messages In/sec** | messages/秒 | 每秒接收的消息數量 | 根據業務量而定 |
| **Bytes In/sec** | bytes/秒 | 每秒接收的數據量 | 通常與消息數量相關 |
| **Bytes Out/sec** | bytes/秒 | 每秒發送的數據量 | 通常比 In 大（多個消費者） |

**分析提示**：
- Bytes Out/In 比例通常是 1:多（一個消息被多個消費者讀取）
- 突然的流量下降可能表示生產者問題
- 突然的流量激增需要檢查是否正常業務

---

### 3. **Kafka Broker: Network Performance** (網路性能)
**用途**：監控網路請求處理性能

| 指標名稱 | 單位 | 說明 | 正常範圍 |
|---------|-----|------|--------|
| **Produce Local Time (ms)** | 毫秒 | 處理生產請求的時間 | < 50ms |
| **Fetch Local Time (ms)** | 毫秒 | 處理消費請求的時間 | < 100ms |
| **Network Processor Idle %** | 百分比 | 網路處理器空閒時間 | > 30% |

**注意事項**：
- Local Time 過高表示處理瓶頸
- Idle % 過低表示網路處理器過載

---

### 4. **Kafka Broker: Topic & Controller Metrics** (主題和控制器指標)
**用途**：監控集群規模和控制器狀態

| 指標名稱 | 說明 | 參考值 |
|---------|------|-------|
| **Total Topics** | 集群中的主題總數 | < 1000（建議） |
| **Total Partitions** | 所有分區總數 | < 10000（建議） |
| **Active Brokers** | 活躍的 Broker 數量 | 應等於實際 Broker 數 |

**規劃建議**：過多的 Topic 和 Partition 會影響性能

---

### 5. **Kafka Broker: Leader & Log Metrics** (領導者和日誌指標)
**用途**：監控分區領導者分佈和日誌寫入

| 指標名稱 | 說明 | 注意事項 |
|---------|------|---------|
| **Leader Partitions** | 此 Broker 作為領導者的分區數 | 各 Broker 應相對平均 |
| **Log Flush Rate** | 日誌刷盤頻率 | 過高可能表示存儲壓力 |

---

### 6. **Kafka Broker: Request Handling** (請求處理)
**用途**：監控不同類型請求的處理速率

| 指標名稱 | 單位 | 說明 | 正常表現 |
|---------|-----|------|--------|
| **Produce Requests/sec** | 請求/秒 | 生產請求頻率 | 穩定的業務相關數值 |
| **Fetch Requests/sec** | 請求/秒 | 消費請求頻率 | 通常比 Produce 高 |

---

### 7. **Kafka Broker: Error & Failure Rates** (錯誤和失敗率) - 重要！
**用途**：監控系統錯誤，這是最關鍵的健康指標

| 指標名稱 | 單位 | 說明 | 正常值 |
|---------|-----|------|-------|
| **Failed Produce Requests/sec** | 錯誤/秒 | 生產失敗次數 | 接近 0 |
| **Failed Fetch Requests/sec** | 錯誤/秒 | 消費失敗次數 | 接近 0 |
| **Network Request Errors/sec** | 錯誤/秒 | 網路層錯誤（按請求類型） | 接近 0 |
| **Produce Error Rate %** | 百分比 | 生產錯誤率 | < 1% |
| **Fetch Error Rate %** | 百分比 | 消費錯誤率 | < 1% |

**關鍵指標說明**：
- 這裡修正了之前顯示"每秒 30 個錯誤"的問題
- 現在顯示真實的錯誤統計和錯誤率百分比
- 任何持續的錯誤都需要立即調查

---

### 8. **Kafka Consumer Lag & Processing** (消費者延遲和處理) - 新增！
**用途**：監控消費者是否跟上生產速度

| 指標名稱 | 單位 | 說明 | 告警閾值 |
|---------|-----|------|---------|
| **Consumer Lag** | 消息數 | 消費者落後的消息數量 | > 10,000 (警告) |
| **Messages Consumed/sec** | 消息/秒 | 消費處理速度 | 應匹配生產速度 |
| **Active Consumer Groups** | 數量 | 活躍的消費者組數 | 監控數量變化 |

**Lag 分析**：
- Lag = 0：消費者跟上了生產速度
- Lag > 0：消費者處理較慢，可能需要擴容
- Lag 持續增長：嚴重問題，需要立即處理

---

### 9. **Kafka JVM & Resource Utilization** (JVM 和資源使用) - 新增！
**用途**：監控 Kafka Broker 的 JVM 健康狀況

| 指標名稱 | 單位 | 說明 | 正常範圍 |
|---------|-----|------|--------|
| **JVM Heap Usage (MB)** | MB | Java 堆記憶體使用量 | < 80% 最大值 |
| **GC Time/sec** | 時間/秒 | 垃圾回收佔用時間 | < 10% |
| **Request Handler Idle %** | 百分比 | 請求處理器空閒率 | > 20% |
| **Active Connections** | 數量 | 活躍連接數 | 監控異常增長 |

**性能調優指標**：這些指標幫助識別性能瓶頸

---

### 10-11. **Application Producers & Consumers** (應用層指標)
**用途**：監控應用層面的生產者和消費者

| 指標類型 | 說明 | 監控重點 |
|---------|------|---------|
| **Python/Go/Java Producer** | 各語言生產者的發送速率 | 按狀態分類的成功/失敗 |
| **Python/Go/Java Consumer** | 各語言消費者的接收速率 | 處理速度和錯誤率 |

---

### 12. **OTel Collector: Telemetry Throughput** (遙測收集器)
**用途**：監控 OpenTelemetry 數據收集

| 指標名稱 | 說明 |
|---------|------|
| **Spans/sec** | 追蹤數據接收速率 |
| **Metrics/sec** | 指標數據接收速率 |
| **Logs/sec** | 日誌數據接收速率 |

---

## 關鍵告警閾值

### 立即需要關注 (Critical)
- Active Controllers ≠ 1
- Offline Partitions > 0
- Error Rate > 5%
- Consumer Lag > 50,000

### 需要監控 (Warning)  
- Under-replicated Partitions > 0
- Network latency > 100ms
- JVM Heap > 80%
- Consumer Lag > 10,000

### 資訊性監控 (Info)
- 吞吐量異常變化
- 連接數異常增長
- GC 時間 > 10%

---

## 故障排除指南

### 1. 當看到錯誤率上升時：
1. 檢查 Error & Failure Rates 面板
2. 確認是哪種類型的錯誤（Produce/Fetch/Network）
3. 查看應用層面板確認是否特定語言/服務
4. 檢查 JVM 面板看是否資源不足

### 2. 當看到 Consumer Lag 增長時：
1. 確認生產速度是否正常
2. 檢查消費者處理速度
3. 考慮增加消費者實例
4. 檢查消費者應用的健康狀況

### 3. 當看到性能下降時：
1. 檢查 Network Performance 面板
2. 查看 JVM 資源使用情況
3. 確認網路處理器不過載
4. 檢查連接數是否異常

---

## 聯絡資訊

**監控負責人**：[您的姓名]  
**更新頻率**：Dashboard 每 10 秒刷新  
**數據保留**：Prometheus 預設保留 15 天

**相關文檔**：
- [OPTIMIZATION_SUMMARY.md](./OPTIMIZATION_SUMMARY.md) - 詳細的優化說明
- Grafana Dashboard - 實時監控面板
- Prometheus Alerts - 告警規則配置 