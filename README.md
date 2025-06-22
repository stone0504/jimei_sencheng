# Jimei Sencheng

一個用於監控吉美君悅建案進度的 Python 專案。此腳本會定期檢查建案網站的更新，當有新進度時會透過 LINE 發送通知訊息。

## 功能特色

- 自動監控建案進度網站
- 檢測網站內容變化
- LINE 訊息推播通知
- 可自訂檢查間隔時間
- 台北時區時間記錄
## 安裝說明

1. 複製專案到本地：
```bash
git clone <repository-url>
cd Jimei_sencheng
```

2. 安裝所需套件：
```bash
pip install requests beautifulsoup4 backports.zoneinfo
```

### 依賴套件
- `requests` - HTTP 請求處理
- `beautifulsoup4` - HTML 解析
- `backports.zoneinfo` - 時區處理（Python < 3.9）

## 使用方法

執行監控腳本：
```bash
python jimei.py
```

腳本會持續運行並：
- 每隔指定時間檢查網站內容
- 在終端顯示檢查狀態和時間
- 當偵測到更新時發送 LINE 通知
- 按 `Ctrl+C` 可停止執行

## 設定檔配置

1. 複製範例設定檔：
```bash
cp config_sample.json config.json
```

2. 編輯 `config.json` 並填入你的資訊：
```json
{
  "LINE_ACCESS_TOKEN": "你的 LINE Bot Access Token",
  "USER_ID": "你的 LINE User ID",
  "LINE_API_URL": "https://api.line.me/v2/bot/message/push",
  "url": "http://www.sccoltd.com.tw/in-progress/123",
  "check_interval": 7200,
  "update_message": "吉美君悅有新進度更新！"
}
```

### 設定項目說明
- `LINE_ACCESS_TOKEN`: LINE Bot 的存取權杖
- `USER_ID`: 接收通知的 LINE 用戶 ID
- `LINE_API_URL`: LINE API 推播訊息的網址
- `url`: 要監控的建案進度網站
- `check_interval`: 檢查間隔（秒），預設 7200 秒（2小時）
- `update_message`: 自訂通知訊息內容

### 如何取得 LINE Bot 資訊
1. 前往 [LINE Developers Console](https://developers.line.biz/)
2. 建立新的 Messaging API Channel
3. 取得 Channel Access Token
4. 取得你的 LINE User ID（可使用 LINE Bot 或相關工具）

## 故障排除

### 常見錯誤
- **config.json not found**: 請確認已建立設定檔
- **config.json is malformed**: 檢查 JSON 格式是否正確
- **Missing essential configuration**: 確認所有必要欄位都已填寫
- **Error fetching URL**: 檢查網路連線或目標網站狀態
- **發送失敗，錯誤代碼**: 檢查 LINE Bot 設定和權杖是否正確

### 執行記錄
腳本會在終端顯示：
- 檢查時間（台北時區）
- 更新狀態（有更新/無更新）
- 錯誤訊息（如有）

## 注意事項

- 請勿將 `config.json` 提交到版本控制系統
- 建議設定適當的檢查間隔，避免對目標網站造成過大負載
- 確保網路連線穩定以避免誤報

## 貢獻
歡迎提交 Pull Request。請遵循 PEP8 程式碼風格指南。

## 授權
此專案僅供個人使用，請遵守相關網站的使用條款。
