---
name: fit-deep-dive
description: 針對少數關鍵跑步課次下載 FIT，用本地 CLI 做配速／心率／爬升深度摘要。
---

# FIT 深度分析

## 何時使用

需要 GPS／逐秒級或跨課次分段對比；摘要工具不夠時。

## 步驟

1. `querySportRecords` 找出目標課次 ID。
2. 先 `getActivityDetail` + `queryActivityLapData`；若已足夠則停止，不下載 FIT。
3. 確認仍需 FIT 後，告知使用者額度（約 24h／50 檔），再呼叫：
   - `downloadActivityFitFiles` 或
   - `queryActivityFitFileDownloadUrls`
4. 將 FIT 存到工作目錄後執行：

```bash
coros-analytics fit-summary --fit <path.fit>
```

5. 結合官方 `analyzeActivityDetail`（可選）與本地摘要，給出教練式解讀。

## 注意

- 一次對話最多下載少量關鍵檔（建議 ≤ 3）。
- 客戶端若無法接收二進位，改用下載 URL 流程。
- 勿在回覆中貼上完整原始 FIT 十六進位。
