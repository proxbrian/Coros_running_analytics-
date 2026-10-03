# 如何建立 COROS MCP 授權連線

本專案使用**官方 remote MCP**，授權是瀏覽器 OAuth，**不是**自己產生一組 API key，也**不必**自建 OAuth App（個人在 Cursor 使用時）。

## 前置條件

1. COROS 帳號可正常登入 [Training Hub](https://t.coros.com)（App 資料需已同步到雲端）
2. 本機安裝 **Cursor Desktop**（建議付費方案；免費方案對 MCP／Connectors 常有限制）
3. 用 Cursor 開啟本 repo（需讀到專案內 [`.cursor/mcp.json`](../.cursor/mcp.json)）

目前設定內容：

```json
{
  "mcpServers": {
    "coros": {
      "url": "https://mcp.coros.com/mcp"
    }
  }
}
```

這條 URL 就是授權入口；Cursor 會依 MCP／OAuth 協定自動打開登入頁。

## 步驟 A：在 Cursor 完成授權（推薦）

1. 用 Cursor 開啟本專案根目錄  
2. 開啟 MCP 設定（任一路徑即可）：
   - **Cursor Settings → MCP**，或  
   - 側邊欄 **Customize → MCP**
3. 確認列表出現伺服器 **`coros`**（來源為專案 `.cursor/mcp.json`）
4. 將 `coros` **啟用（toggle on）**
5. 若顯示 **Connect / Login / Authenticate**，點下去  
6. 系統會開啟瀏覽器 → 登入 COROS → 同意授權  
7. 授權成功後回到 Cursor；`coros` 狀態應為已連線／tools 可載入  
8. 開一個 **新的 Agent 對話**，測試：

```text
請呼叫 COROS MCP，列出我過去 14 天的跑步活動摘要。
```

有真實里程／日期即表示授權成功。

### 授權流程示意

```text
Cursor 讀取 mcp.json 的 url
        ↓
連線 https://mcp.coros.com/mcp
        ↓
觸發 OAuth（瀏覽器登入 COROS）
        ↓
同意授權 → Cursor 保存連線狀態
        ↓
Agent 可呼叫 querySportRecords 等工具
```

## 步驟 B：區域 URL 備援（授權頁打不開／Invalid URL）

`mcp.coros.com` 會依帳號區域轉址。若你的環境不支援轉址，把 [`.cursor/mcp.json`](../.cursor/mcp.json) 改成對應區域（可參考 [`.cursor/mcp.regions.example.json`](../.cursor/mcp.regions.example.json)）：

| 帳號區域 | URL |
| --- | --- |
| 中國大陸 | `https://mcpcn.coros.com/mcp` |
| 歐洲 | `https://mcpeu.coros.com/mcp` |
| 美國 | `https://mcpus.coros.com/mcp` |

改完後重開 Cursor 或重新 toggle MCP，再走一次 Connect。

## 步驟 C：用官方 CLI 產生登入連結（進階／除錯）

若 Cursor UI 沒有跳出授權，或你要在終端機先驗證帳號，可用官方 helper：

```bash
npx coros-mcp@latest login-start
```

終端機會印出**瀏覽器登入連結**。用手機或電腦打開該連結完成 COROS 登入後，在同一台機器執行：

```bash
npx coros-mcp@latest login-finish
npx coros-mcp@latest list-tools
```

這條路主要服務 CLI／OpenClaw 類 Agent；**Cursor 日常使用仍以步驟 A 為主**。CLI 授權快取與 Cursor 桌面 OAuth 不一定共用。

## 你不需要做的事

| 誤解 | 實際情況 |
| --- | --- |
| 自己去 COROS 後台「建立授權連結」 | 個人整合無此後台；連結由 MCP OAuth 流程產生 |
| 先申請 Partner API | 僅多使用者／webhook 才需要 |
| 在 `mcp.json` 填帳號密碼 | 禁止；只用 `url`，由 OAuth 處理 |
| 自填 `CLIENT_ID`／`CLIENT_SECRET` | 個人接 Cursor **通常不需要**（COROS 走動態 OAuth） |

只有在你要做「自己的產品 App、且 COROS／平台要求固定 OAuth client」時，才需要在 `mcp.json` 加 `auth.CLIENT_ID` 等欄位，並向平台登記 redirect：

- Desktop：`http://localhost:8787/callback`
- Web／Cloud Agents：`https://www.cursor.com/agents/mcp/oauth/callback`

一般個人分析 Agent **跳過這段即可**。

## 常見問題

**授權後對話仍沒資料**  
先確認 App／Training Hub 看得到該段活動；再開新對話並明確說「請呼叫 COROS MCP」。

**找不到 MCP／Connectors**  
多半是方案權限；確認 Cursor 版本與 MCP 功能是否可用。

**一直 session expired**  
移除連線後重授；若用過舊版 `coros-mcp` skill／CLI，先 `npm install -g coros-mcp@latest`。

**想撤銷授權**  
在 Cursor MCP 設定中 Disconnect／移除 `coros`；並在 COROS 帳號安全／已授權應用（若有）解除。本專案不保存你的密碼。

## 驗證清單

- [ ] Training Hub 可登入且有跑步資料  
- [ ] Cursor 看到 `coros` MCP 且已啟用  
- [ ] 瀏覽器 OAuth 完成  
- [ ] 新對話能查到過去 14 天跑步紀錄  
- [ ] （可選）`npx coros-mcp list-tools` 看得到 `querySportRecords`
