import streamlit as st
import pandas as pd
import sqlite3
import folium
from streamlit_folium import st_folium
import os
from folium.features import DivIcon

# --- 頁面設定與資料載入 ---
st.set_page_config(page_title="台灣氣溫預報儀表板", layout="wide", page_icon="🌤️")

# 自定義 CSS 以強化視覺效果
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .stHeader {
        font-family: 'Segoe UI', sans-serif;
        color: #1e3a8a;
    }
</style>
""", unsafe_allow_html=True)

# 各地區的近似經緯度 (用於地圖標示)
REGION_COORDS = {
    "台北": [25.0330, 121.5654],
    "北部地區": [25.0330, 121.5654],
    "台中": [24.1477, 120.6736],
    "中部地區": [24.1477, 120.6736],
    "台南": [22.9997, 120.2270],
    "南部地區": [22.9997, 120.2270],
    "高雄": [22.6273, 120.3014],
    "宜蘭": [24.7021, 121.7705],
    "東北部地區": [24.7021, 121.7705],
    "花蓮": [23.9772, 121.6055],
    "東部地區": [23.9772, 121.6055],
    "台東": [22.7554, 121.1444],
    "東南部地區": [22.7554, 121.1444]
}

def load_data_from_db():
    if not os.path.exists("data.db"):
        return pd.DataFrame()
    try:
        conn = sqlite3.connect("data.db")
        df = pd.read_sql_query("SELECT * FROM TemperatureForecasts", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

def get_color(avg_temp):
    if avg_temp < 20: return "#3b82f6" # Blue
    elif 20 <= avg_temp <= 25: return "#10b981" # Green
    elif 25 < avg_temp <= 28: return "#f59e0b" # Orange
    else: return "#ef4444" # Red

df = load_data_from_db()

# --- UI 介面設計 ---
st.title("🌤️ 台灣分區氣溫趨勢儀表板")
st.markdown("仿照 CWA 氣象署樣式的動態互動地圖")

if df.empty:
    st.error("找不到資料資料庫，請先執行 `python fetch_data.py`。")
    st.stop()

# 側邊欄控制
st.sidebar.header("🛠️ 儀表板控制")
available_dates = sorted(df['dataDate'].unique())
selected_date = st.sidebar.selectbox("📅 選擇預報日期", available_dates)

# 過濾資料
filtered_df = df[df['dataDate'] == selected_date].copy()

# 左右排版: 左邊是地圖 (佔 60%) / 右邊是表格與圖表 (佔 40%)
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader(f"📍 觀測/預報分佈圖 ({selected_date})")
    
    # 初始化 Folium 地圖
    m = folium.Map(location=[23.6978, 120.9605], zoom_start=7, tiles="CartoDB positron")
    
    for _, row in filtered_df.iterrows():
        region = row['regionName']
        matched_key = next((k for k in REGION_COORDS.keys() if k in region), None)
        
        if matched_key:
            coords = REGION_COORDS[matched_key]
            avg_t = (row['mint'] + row['maxt']) / 2
            color = get_color(avg_t)
            
            # 建立類似 CWA 的溫度標籤
            folium.Marker(
                location=coords,
                icon=DivIcon(
                    icon_size=(40,40),
                    icon_anchor=(20,20),
                    html=f"""
                    <div style="
                        background-color: {color};
                        color: white;
                        border-radius: 50%;
                        width: 40px;
                        height: 40px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: bold;
                        font-family: sans-serif;
                        font-size: 14px;
                        border: 2px solid white;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
                        pointer-events: auto;
                    " title="{region}">
                        {int(avg_t)}
                    </div>
                    """
                ),
                popup=folium.Popup(f"<b>{region}</b><br>最低: {row['mint']}°C<br>最高: {row['maxt']}°C", max_width=150)
            ).add_to(m)

    st_folium(m, width=None, height=550, use_container_width=True)

with col2:
    st.subheader("📋 數據細節")
    display_df = filtered_df[['regionName', 'mint', 'maxt']].rename(
        columns={"regionName": "地區", "mint": "最低溫", "maxt": "最高溫"}
    )
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.subheader("📈 地區一週趨勢")
    selected_region = st.selectbox("請選擇查看地區:", sorted(df['regionName'].unique()))
    trend_df = df[df['regionName'] == selected_region].sort_values('dataDate')
    
    st.line_chart(
        trend_df.set_index('dataDate')[['mint', 'maxt']].rename(columns={"mint": "Low", "maxt": "High"}),
        color=["#3b82f6", "#ef4444"]
    )

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 統計摘要")
st.sidebar.write(f"今日全台最高溫: `{filtered_df['maxt'].max()}°C`")
st.sidebar.write(f"今日全台最低溫: `{filtered_df['mint'].min()}°C`")
