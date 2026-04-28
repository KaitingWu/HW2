# 📝 台灣氣溫預報儀表板 - 開發日誌 (Development Log)

本文件紀錄《物聯網 HW2：台灣分區氣溫預報儀表板》專案的開發過程、重要決策與遇到的問題解決方案。

## 📅 開發歷程

### 第一階段：需求分析與環境建置 (Initial Setup)
- **目標**：從中央氣象署 (CWA) 獲取台灣各分區（北部、中部、南部、東北部、東部及東南部地區）的一週天氣預報資料。
- **實作**：
  - 確認使用 CWA API 代碼 `F-A0010-001`（農業氣象預報），因其包含所需之分區與一週氣溫資料。
  - 使用 `requests` 套件發送 GET 請求。
  - **解決問題**：API 請求遇到 SSL 憑證驗證問題，透過加入 `verify=False` 參數暫時忽略驗證以順利獲取資料。
  - **評分需求對齊**：依據作業要求，利用 `response.json()` 取得資料後，加入 `json.dumps(..., indent=4, ensure_ascii=False)` 以滿足「觀察獲得的資料」之評分標準。

### 第二階段：資料解析與儲存 (Data Parsing & Storage)
- **目標**：將複雜的 JSON 結構轉化為乾淨、易於分析的結構化資料，並匯出保存。
- **實作**：
  - 成功解析深層 JSON 路徑：`cwaopendata -> resources -> resource -> data -> agrWeatherForecasts -> weatherForecasts -> location`。
  - 提取各地區每日的 `MinT` (最低溫) 與 `MaxT` (最高溫) 及日期 (`dataDate`)。
  - 轉換為 Pandas DataFrame，並匯出為 `weather_data.csv` (指定 `utf-8-sig` 編碼防止中文亂碼)。
  - **擴充功能**：為了後續網頁端讀取更具彈性，除了 CSV，額外透過 `sqlite3` 將資料寫入本機資料庫 `data.db` 的 `TemperatureForecasts` 資料表。

### 第三階段：動態視覺化網頁開發 (Streamlit Web App)
- **目標**：建立一個可以動態展示地圖及數據的網頁儀表板，需有左右排版設計。
- **實作**：
  - 使用 `streamlit` 建立基礎網頁框架，並以 `st.columns([1.5, 1])` 實作左（地圖）右（數據）的排版設計。
  - **地圖整合**：整合 `folium` 與 `streamlit_folium`。根據解析出的地區名稱（如：台北、北部地區等），手動定義 `REGION_COORDS` 對應其近似經緯度。
  - **視覺化巧思**：
    - 撰寫 `get_color()` 函式，依據日均溫動態回傳不同顏色（紅、橘、綠、藍）。
    - 捨棄預設標記，改用 `folium.features.DivIcon`，透過自定義 HTML/CSS 刻出類似氣象署 (CWA) 官網帶有顏色的圓形溫度標籤，大幅提升視覺質感。
  - **互動功能**：在側邊欄加入日期選擇器 (`selectbox`)，讓使用者可以切換不同日期的全台預報，並即時更新地圖上的標記與右側表格。
  - 右側下半部加入 `st.line_chart` 來展示單一地區的一週高低溫趨勢。

### 第四階段：版本控制與文件完善 (Version Control & Documentation)
- **目標**：將程式碼推播至 GitHub 並完善專案文件。
- **實作**：
  - 初始化 Git 儲存庫，並建立 `.gitignore` 檔案。
  - 將 `.env` (保護 API Key)、`data.db`、`weather_data.csv` 及快取資料夾加入忽略名單，確保敏感與執行期生成的檔案不被推播。
  - 撰寫完整的 `README.md`，說明專案特色、目錄結構與執行步驟。
  - 順利將程式碼推送至使用者的 GitHub 儲存庫：[KaitingWu/HW2](https://github.com/KaitingWu/HW2)。
  - 建立此 `DEVELOPMENT_LOG.md` 以紀錄完整開發軌跡。

---
## 💡 未來可擴充方向 (Future Work)
- 整合真實的 GeoJSON 邊界資料，實作 Choropleth Map（面量圖）讓各縣市/分區的填色範圍更精確。
- 新增降雨機率 (PoP) 與天氣現象 (Wx) 的圖示顯示。
- 將應用程式部署至 Streamlit Community Cloud 或 Render 等雲端平台。
