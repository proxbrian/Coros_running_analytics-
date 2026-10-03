---
name: race-readiness
description: 依 COROS 體能評估、備賽期跑量與負荷，評估 5K／10K／半馬／全馬就緒程度。
---

# 賽事就緒評估

## 何時使用

使用者提到比賽日、目標完賽時間，或問「我準備好了嗎」。

## 步驟

1. 確認：目標距離（`5k`／`10k`／`half`／`marathon`）、比賽日、可選目標配速。
2. 呼叫 MCP：
   - `queryFitnessAssessmentOverview`
   - `querySportRecords`（備賽期，預設比賽前 8–12 週）
   - `queryTrainingLoadAssessment`
   - 可選：`queryRecoveryStatus`
3. 整理 JSON（見 `sample_data/race_readiness.json`）。
4. 執行：

```bash
coros-analytics race-readiness --input <file> --target half
```

5. 報告：readiness 分數、官方預測 vs 目標、風險（傷／減量不足）、建議訓練重點。
6. 若要產生課表，先給草稿；使用者說「請存到 COROS」後才呼叫 `createTrainingPlan` 等寫入工具。

## 注意

- 預測時間來自 COROS 官方評估時應標明來源。
- 減量（taper）週勿建議突然加量。
