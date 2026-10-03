---
name: running-weekly-review
description: 使用官方 COROS MCP 與本地 coros-analytics 產出過去 N 週跑步訓練週回顧。
---

# 跑步週回顧

## 何時使用

使用者要看週／月跑步量、配速趨勢、長跑比例、訓練負荷變化。

## 步驟

1. 向使用者確認日期範圍（預設過去 28 天）與單位（公里／英里）。
2. 呼叫 COROS MCP：
   - `querySportRecords`（範圍內跑步活動）
   - 抽樣關鍵課次 `getActivityDetail`（長跑、間歇各 1–2 堂）
   - `queryTrainingLoadAssessment`
   - `queryFitnessAssessmentOverview`
3. 將活動清單整理為 JSON（欄位對齊 `sample_data/activities_4w.json`），必要時寫入暫存檔。
4. 執行：

```bash
coros-analytics weekly-review --input <activities.json>
```

5. 依 `AGENTS.md` 輸出格式回報；標註資料缺口（例如未同步的手錶）。

## 注意

- 不要為了週回顧下載整段期間全部 FIT。
- 若活動為 0，檢查運動類型篩選與帳號是否同步，勿編造數據。
