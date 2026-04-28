# 🌤️ 台灣分區氣溫預報儀表板 (Taiwan Weather Forecast Dashboard)

這是一個基於 Python 與 Streamlit 建立的互動式氣象儀表板。專案透過氣象署 (CWA) 開放資料 API 抓取台灣各分區（北部、中部、南部、東北部、東部、東南部）的一週氣溫預報，並將數據儲存為 CSV 與 SQLite 資料庫。最後透過 Streamlit 搭配 Folium 動態地圖呈現直觀的視覺化結果。

## ✨ 專案特色 (Features)

- **自動化資料獲取**：使用 `requests` 向 CWA API (F-A0010-001) 取得最新氣象 JSON 資料。
- **資料儲存**：將解析後的氣象資料匯出為 `weather_data.csv`，並存入本機端 SQLite 資料庫 (`data.db`)。
- **動態互動地圖**：使用 `folium` 繪製台灣地圖，根據各地區的平均溫度動態改變地圖上的溫度標記顏色，並仿照氣象署官方樣式設計。
- **資料視覺化版面**：採用 Streamlit 左右排版設計 (Left-Right Layout)，左側為地圖，右側為詳細數據表格與一週氣溫趨勢圖 (Line Chart)。
- **動態過濾**：可透過側邊欄選擇不同預報日期，即時更新地圖與數據。

## 📂 專案結構 (Project Structure)

```text
HW2/
│
├── fetch_data.py          # 負責呼叫 CWA API 抓取資料並存入 CSV 與 SQLite
├── app.py                 # Streamlit 儀表板主程式 (前端介面與地圖)
├── weather_data.csv       # 抓取並解析後產生的天氣預報資料
├── data.db                # SQLite 資料庫，提供給 Streamlit 讀取
├── .env                   # 放置 CWA API_KEY (請自行建立)
├── .gitignore             # 忽略推播的敏感檔案與快取
└── README.md              # 專案說明文件
```

## 🚀 快速開始 (Quick Start)

### 1. 安裝套件
確保你的環境中已經安裝了以下套件：
```bash
pip install requests pandas streamlit folium streamlit-folium python-dotenv
```

### 2. 環境變數設定
在專案根目錄下建立一個 `.env` 檔案，並填入你從氣象署申請的 API Key：
```env
CWA_API_KEY=你的_API_KEY
```

### 3. 獲取資料
執行資料抓取腳本，這將會產生 `weather_data.csv` 和 `data.db`：
```bash
python fetch_data.py
```

### 4. 啟動儀表板
啟動 Streamlit 應用程式：
```bash
streamlit run app.py
```
啟動後，瀏覽器將會自動開啟 `http://localhost:8501` 展示動態氣象儀表板。

---
*此專案為物聯網 (IoT) 課程作業 (HW2)*
