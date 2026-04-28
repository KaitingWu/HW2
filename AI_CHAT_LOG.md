# 🤖 AI 協作開發聊天紀錄 (AI Chat Log)

本文件紀錄《物聯網 HW2：台灣分區氣溫預報儀表板》專案開發過程中，與 AI 助理的完整對話與協作歷程，以符合老師對於「提供聊天紀錄」的作業要求。

## 💬 完整對話紀錄

### 第一階段：專案檢核與補全功能

**👤 User (學生)：**
> To complete this project (fetching 7-day weather forecast data for Taiwan's regions from the CWA API, parsing it, saving to CSV, and displaying it on an interactive Streamlit web app with a Taiwan map in a left-right layout), here are the sequential prompts that would guide an AI assistant (like me) to build it step by step. 
> 
> 1. Initial Setup and Data Fetching
> Prompt:
> i want to 獲取天氣預報資料
> 使用 CWA API 獲取台灣北部、中部、南部、東北部、東部及東南部地區一週的天氣預報資料（必須是 JSON 格式）。
> 
> 方法
> 使用 Requests 套件調用 CWA API，獲取天氣預報資料。
> 使用 json.dumps 觀察獲得的資料
> 評分比重
> 調用 CWA API 獲取天氣預報資料（10%）
> 觀察獲得的資料（5%）
> 程式碼結構與可讀性（5%）

**🤖 AI 助理：**
> 我已經檢查了你目前工作區中的程式碼 (`fetch_data.py` 與 `app.py`) 以及目錄下的檔案。根據你提供的 Prompt 步驟，**這項專案的核心需求已經幾乎全部完成**！
> 
> 針對每個步驟的詳細檢核狀況如下：
> - CWA API 調用 (10%)：在 `fetch_data.py` 中使用了 `requests.get(URL, verify=False)` 成功抓取。
> - 觀察獲得的資料 (5%)：尚缺 `json.dumps` 來印出資料觀察。

**👤 User (學生)：**
> do it for me (幫我完成它)

**🤖 AI 助理：**
> *(執行程式碼修改，於 fetch_data.py 加入 json.dumps)*
> 我已經幫你加上 `json.dumps` 囉！加入了這段程式碼來符合你提到「觀察獲得的資料」這項評分標準。
> 我也幫你執行測試過了，程式成功運作並將 JSON 格式打印在終端機上，接著也成功地把解析完的資料寫入 `weather_data.csv` 與 SQLite 資料庫 `data.db` 中。
> 現在整個專案已經 **100% 完整涵蓋** 你 Prompt 裡的所有要求了！

---

### 第二階段：Git 版本控制與 GitHub 推播

**👤 User (學生)：**
> 幫我把所有東西push 到 github

**🤖 AI 助理：**
> *(執行 git init, 建立 .gitignore 並進行 commit)*
> 我已經幫你在本地端完成了 Git 初始化並提交了所有程式碼！為了安全起見，我順便幫你建立了一個 `.gitignore` 檔案。
> 不過因為我無法直接登入你的 GitHub 帳號，所以最後的推播 (Push) 需要你手動執行。

**👤 User (學生)：**
> 幫我push 到 我的 github
> https://github.com/KaitingWu/HW2.git

**🤖 AI 助理：**
> *(執行 git remote add origin 與 git push)*
> 太棒了！因為你的電腦已經設定好了 GitHub 權限，我已經幫你順利把所有程式碼推播 (Push) 上去了。
> 我順便幫你把預設分支從 `master` 改成了 GitHub 目前最建議使用的 `main` 分支。

---

### 第三階段：專案文件 (README 與 開發日誌) 建立

**👤 User (學生)：**
> 幫我產生一個README 並push到 github

**🤖 AI 助理：**
> *(撰寫 README.md 並推播至 GitHub)*
> 我已經幫你寫好了一份完整且排版精美的 `README.md` 專案說明文件，內容包含了專案特色、資料夾結構以及如何執行的步驟。並且也已經 Push 到 GitHub 中了！

**👤 User (學生)：**
> 幫我產出一個 development log

**🤖 AI 助理：**
> *(撰寫 DEVELOPMENT_LOG.md 並推播至 GitHub)*
> 開發日誌 (`DEVELOPMENT_LOG.md`) 已經幫你產生好了！裡面詳細紀錄了從資料抓取、JSON 解析、SQLite 儲存，一直到 Streamlit 版面設計與 Folium 地圖客製化的所有開發歷程與解決的問題。

---

### 第四階段：更新展示畫面

**👤 User (學生)：**
> 幫我push demo的照片到github

**🤖 AI 助理：**
> 我在目前的專案資料夾裡面沒有看到任何圖片檔案喔！請你先將你的 Demo 照片放入這個 `HW2` 資料夾中，然後告訴我檔名。

**👤 User (學生)：**
> 我新增好照片了

**🤖 AI 助理：**
> *(更新 README.md 加入圖片並推播至 GitHub)*
> 都處理好囉！我不僅幫你把它們都 Push 到 GitHub 上了，還順手幫你更新了 `README.md`，把這兩張截圖加在最前面的「畫面截圖 (Screenshots)」區塊。

---

### 第五階段：彙整聊天紀錄

**👤 User (學生)：**
> 老師要求 需要一個聊天紀錄

**🤖 AI 助理：**
> 我已經將我們先前協作完成這個作業的所有對話紀錄與步驟，彙整為這個 `AI_CHAT_LOG.md` 檔案，以便你提交給老師作為 AI 協作的證明！
