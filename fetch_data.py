import requests
import json
import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv

# 從 .env 檔案載入 API key
load_dotenv()
API_KEY = os.getenv("CWA_API_KEY")

# CWA API 網址 (根據要求使用 F-A0010-001 農業氣象預報)
URL = f"https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001?Authorization={API_KEY}&downloadType=WEB&format=JSON"

def fetch_and_process_data():
    # 1. 獲取天氣預報資料 (HW2-1)
    try:
        response = requests.get(URL, verify=False)
        if response.status_code != 200:
            print(f"無法從 API 獲取資料。狀態碼: {response.status_code}")
            return
        data = response.json()
        
        # 觀察獲得的資料 (滿足 HW2-1 的評分條件)
        # 由於完整資料龐大，我們使用 json.dumps 並只印出前 500 個字元作為觀察展示
        print("--- 觀察 API 回傳的 JSON 資料 ---")
        json_str = json.dumps(data, indent=4, ensure_ascii=False)
        print(json_str[:500] + "\n... [資料過長省略] ...\n")
    except Exception as e:
        print(f"發送請求或解析 JSON 時發生錯誤: {e}")
        return

    # 2. 分析資料，提取最高與最低氣溫 (HW2-2)
    processed_data = []
    
    try:
        # F-A0010-001 的正確路徑
        # cwaopendata -> resources -> resource -> data -> agrWeatherForecasts -> weatherForecasts -> location
        locations = data['cwaopendata']['resources']['resource']['data']['agrWeatherForecasts']['weatherForecasts']['location']
        
        for loc in locations:
            region_name = loc['locationName']
            weather_elements = loc['weatherElements']
            
            # 獲取 MinT 和 MaxT 的每日資料 (daily)
            min_t_daily = weather_elements.get('MinT', {}).get('daily', [])
            max_t_daily = weather_elements.get('MaxT', {}).get('daily', [])
            
            for min_t, max_t in zip(min_t_daily, max_t_daily):
                data_date = min_t.get('dataDate', '')
                mint_val = int(min_t.get('temperature', 0))
                maxt_val = int(max_t.get('temperature', 0))
                
                processed_data.append({
                    "regionName": region_name,
                    "dataDate": data_date,
                    "mint": mint_val,
                    "maxt": maxt_val
                })
                
    except KeyError as e:
        print(f"JSON 解析路徑錯誤: 找不到鍵值 {e}。這可能是因為 API 回傳結構已變更。")
        return
    except Exception as e:
        print(f"解析資料時發生意外錯誤: {e}")
        return

    if not processed_data:
        print("未找到任何氣溫資料。")
        return

    df = pd.DataFrame(processed_data)

    # 3. 儲存為 CSV 檔案
    df.to_csv("weather_data.csv", index=False, encoding='utf-8-sig')
    print("資料已儲存至 weather_data.csv")

    # 4. 將氣溫資料儲存到 SQLite3 資料庫 (HW2-3)
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    
    # 創建 Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TemperatureForecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            regionName TEXT,
            dataDate TEXT,
            mint INTEGER,
            maxt INTEGER
        )
    ''')
    
    # 清除舊資料並寫入新資料
    cursor.execute('DELETE FROM TemperatureForecasts')
    df.to_sql('TemperatureForecasts', conn, if_exists='append', index=False)
    
    # 驗證資料集
    print("\n--- 驗證 SQLite 資料庫寫入 ---")
    print("列出抓取到的地區名稱:")
    for row in cursor.execute('SELECT DISTINCT regionName FROM TemperatureForecasts'):
        print(f"- {row[0]}")
        
    conn.commit()
    conn.close()
    print("\n資料庫更新完成！")

if __name__ == "__main__":
    fetch_and_process_data()
