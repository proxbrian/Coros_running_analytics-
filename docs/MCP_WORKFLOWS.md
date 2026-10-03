# 官方 COROS MCP 工具對照與工作流

端點：`https://mcp.coros.com/mcp`（Streamable HTTP + OAuth）

區域備援：

| 區域 | URL |
| --- | --- |
| 中國大陸 | `https://mcpcn.coros.com/mcp` |
| 歐洲 | `https://mcpeu.coros.com/mcp` |
| 美國 | `https://mcpus.coros.com/mcp` |

## 工具分組（跑步分析常用）

### 活動

| Tool | 用途 |
| --- | --- |
| `querySportRecords` | 依日期／運動類型列出活動 ID |
| `getActivityDetail` | 心率、配速、爬升等摘要 |
| `analyzeActivityDetail` | 官方教練風格單次分析 |
| `queryActivityLapData` | 預設圈／分段 |
| `queryCustomActivityLapData` | 自訂時間窗分段 |
| `downloadActivityFitFiles` | 下載 FIT（深度分析） |
| `queryActivityFitFileDownloadUrls` | FIT 下載連結備援 |

### 健康與恢復

| Tool | 用途 |
| --- | --- |
| `queryDailyHealthData` | 步數、卡路里、壓力、睡眠摘要 |
| `querySleepData` / `querySleepHrv` | 睡眠與睡眠 HRV |
| `queryRestingHeartRate` / `queryAvgHeartRate` | 心率趨勢 |
| `queryStressLevel` / `queryStressTimeSeries` | 壓力 |
| `queryRecoveryStatus` | 恢復百分比與預估 |

### 訓練狀態與課表

| Tool | 用途 |
| --- | --- |
| `queryFitnessAssessmentOverview` | VO2max、閾值配速、完賽預測 |
| `queryTrainingLoadAssessment` | 短／長期負荷與比值 |
| `queryTrainingSchedule` | 行事曆 |
| `queryTrainingPlanLibrary` / `Details` / `create` / `update` | 多週課表 |
| `queryWorkoutLibrary` / `Details` / `createSingleWorkout` / `updateWorkoutDetails` | 課表庫模板 |
| `scheduleWorkout` / `createScheduledWorkout` / `updateScheduledWorkout` | 當日行程 |

### 其他

| Tool | 用途 |
| --- | --- |
| `queryUserInfo` | 身高體重等基本資料 |
| `queryDevices` | 綁定裝置 |

> 實際參數以連線後工具 schema 為準；文件可能落後於伺服器。

## 標準工作流

### 1. 四週跑步週回顧

1. `querySportRecords`（過去 28 天，跑步類型）
2. 對代表性課次 `getActivityDetail`（避免一次拉全部 FIT）
3. `queryTrainingLoadAssessment` + `queryFitnessAssessmentOverview`
4. 將活動 JSON 存檔後執行：  
   `coros-analytics weekly-review --input <file>`
5. 產出：週里程、長跑%、配速趨勢、負荷解讀

### 2. 負荷 × 恢復決策

1. `queryTrainingLoadAssessment`
2. `queryRecoveryStatus`
3. `querySleepData`（最近 14 天）+ `querySleepHrv`
4. `queryRestingHeartRate`
5. `coros-analytics load-recovery --input <file>`
6. 建議：今日強度（恢復跑／正常／休息），**不自動寫入課表**

### 3. 賽事就緒

1. `queryFitnessAssessmentOverview`（取得預測與閾值）
2. `querySportRecords`（備賽期里程）
3. `queryTrainingLoadAssessment`
4. `coros-analytics race-readiness --input <file> --target half|marathon|10k|5k`
5. 回報 readiness 分數、風險、缺口訓練類型

### 4. FIT 深度分析（省額度）

1. 先用 `querySportRecords` + `getActivityDetail` 選定 1–3 堂關鍵課
2. `downloadActivityFitFiles`（注意 24h／50 檔）
3. `coros-analytics fit-summary --fit <path>`
4. 解讀配速／心率／爬升時間序列摘要

### 5. 寫入課表（高風險）

僅在使用者明確說「請存到 COROS／排程」時：

1. 先讀：`queryTrainingSchedule`、必要時 library／plan details
2. 區分：多週 plan vs 庫模板 vs 當日 standalone
3. 寫入對應 tool
4. 再查一次驗證；逾時先查狀態，不盲目重試
5. 刪除／移動部分操作仍導向 COROS App

## 運動類型備註

- **活動紀錄** sport code 與 **課表 course** sport code 不同（官方文件：course 常用 1／2／5；活動紀錄如 100／200 等）
- 呼叫前用 `describe-tool` 或平台工具說明確認枚舉值
