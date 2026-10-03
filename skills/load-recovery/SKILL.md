---
name: load-recovery
description: 交叉解讀 COROS 訓練負荷、恢復、睡眠與 HRV，給出當日訓練強度建議。
---

# 負荷與恢復決策

## 何時使用

使用者問「今天能不能練」「要不要休息」「負荷會不會太高」。

## 步驟

1. 呼叫 MCP：
   - `queryTrainingLoadAssessment`
   - `queryRecoveryStatus`
   - `querySleepData`（建議 14 天）
   - `querySleepHrv`（若可用）
   - `queryRestingHeartRate`
   - 可選：`queryTrainingSchedule`（今天已排程內容）
2. 整理為 JSON（見 `sample_data/load_recovery.json`）。
3. 執行：

```bash
coros-analytics load-recovery --input <file>
```

4. 建議分級：`rest` / `easy` / `normal` / `quality`，並說明依據。
5. **預設不改課表**。若建議與今日排程衝突，先詢問是否調整，再依 `docs/MCP_WORKFLOWS.md` 寫入流程。

## 注意

- 恢復指標異常時優先建議保守選項。
- 醫療症狀（胸痛、暈眩等）應建議就醫，不做診斷。
