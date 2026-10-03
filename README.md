# COROS 跑步訓練分析 Agent

以**官方 COROS MCP**（`https://mcp.coros.com/mcp`）為唯一資料源，再疊加自訂跑步分析邏輯、Agent Skills 與報告工作流的分析 Agent。

## 架構一覽

```text
Cursor / Agent
    │  OAuth + Streamable HTTP
    ▼
官方 COROS MCP  ──► 活動 / 健康 / 負荷 / 課表 / FIT
    │
    ▼
本專案分析層（Python）
    │  週回顧、負荷恢復、賽事就緒、FIT 深度分析
    ▼
結構化報告 / 訓練建議（寫回 COROS 需使用者明確授權）
```

| 層級 | 職責 | 本 repo |
| --- | --- | --- |
| 資料存取 | OAuth、活動／健康／課表／FIT | 官方 MCP（不自建 server） |
| 分析層 | ACWR、配速趨勢、就緒分數、FIT 摘要 | `src/coros_analytics/` |
| Agent 行為 | 工具路由、寫入安全、報告格式 | `skills/`、`AGENTS.md` |

## 快速開始

### 1. 連線官方 COROS MCP（Cursor）

專案已提供 [`.cursor/mcp.json`](.cursor/mcp.json)。完整圖文步驟見 **[授權設定指南](docs/AUTH_SETUP.md)**。

簡要流程：

1. 用 Cursor 開啟本 repo → **Settings → MCP**，確認 `coros` 出現並啟用
2. 點 **Connect／Authenticate**，在瀏覽器登入 COROS 並同意授權
3. 新開對話測試：「請呼叫 COROS MCP，列出我過去 14 天跑步活動」
4. 若 `mcp.coros.com` 轉址失敗，改用區域端點（見 [`docs/AUTH_SETUP.md`](docs/AUTH_SETUP.md)）

### 2. 安裝本機分析層

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

### 3. 使用 Agent

在 Cursor Agent 對話中直接問，例如：

- 「用 COROS MCP 做過去 4 週跑步週回顧」
- 「依負荷與恢復，評估我現在適不適合長跑」
- 「下載上週長跑的 FIT 並做配速／心率分段分析」

Agent 會依 [`AGENTS.md`](AGENTS.md) 與 [`skills/`](skills/) 先呼叫官方 MCP，再視需要跑本地分析 CLI。

### 4. 本地分析 CLI（可選）

MCP 拉回的 JSON／FIT 可交給 CLI：

```bash
coros-analytics weekly-review --input sample_data/activities_4w.json
coros-analytics load-recovery --input sample_data/load_recovery.json
coros-analytics race-readiness --input sample_data/race_readiness.json
coros-analytics fit-summary --fit sample_data/sample_run.fit
```

## 文件

- [授權設定指南](docs/AUTH_SETUP.md)
- [執行計畫與風險評估](docs/EXECUTION_PLAN.md)
- [MCP 工具對照與工作流](docs/MCP_WORKFLOWS.md)
- [Agent 行為規範](AGENTS.md)

## 限制（官方 MCP）

- 單使用者 OAuth 範圍；無 webhook，需主動查詢
- FIT 下載：每 24 小時約 50 檔上限
- 課表寫入會改動 COROS 帳號；僅在使用者明確要求時執行
- 刪除課表／移動部分行程仍需 COROS App

## 授權與隱私

使用官方 COROS MCP 須遵守 [COROS 服務條款](https://coros.com/terms) 與[隱私政策](https://coros.com/privacy)。本專案不儲存帳密；OAuth 權杖由 Cursor／官方 MCP 客戶端管理。
