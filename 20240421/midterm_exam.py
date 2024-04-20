import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

# 讀取 CSV 檔案
df = pd.read_csv("c:/Users/user/Dropbox/我的電腦 (LAPTOP-CTNAGM22)/Desktop/檔案資料/AI於土木之應用/cycu_ai2024/20240421/地震活動彙整_638492782349653651.csv", encoding='big5', skiprows=1)

# 將 "地震時間" 轉換為 datetime 對象，並選擇在指定日期範圍內的地震數據
df["地震時間"] = pd.to_datetime(df["地震時間"])
df = df[(df["地震時間"] >= "2024-04-03") & (df["地震時間"] <= "2024-04-09")]

# 創建地圖對象，這裡以台灣為中心
m = folium.Map(location=[23.6978, 120.9605], zoom_start=7)

## 將 "地震時間" 轉換為 datetime 對象，並選擇在指定日期範圍內的地震數據
df["地震時間"] = pd.to_datetime(df["地震時間"])
df = df[(df["地震時間"] >= "2024-04-03") & (df["地震時間"] <= "2024-04-09")]

# 將所有在 "2024-04-03 00:00:00" 之前的事件的時間都設置為 "2024-04-03 00:00:00"
start_time = pd.to_datetime("2024-04-03 00:00:00")
df.loc[df["地震時間"] < start_time, "地震時間"] = start_time

# 創建地震事件的 GeoJSON 物件
features = [
    {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [row["經度"], row["緯度"]],
        },
        'properties': {
            'time': row["地震時間"].isoformat(),
            'style': {'color' : 'red'},
            'icon': 'circle',
            'popup': f"編號: {row['編號']}<br>規模: {row['規模']}<br>深度: {row['深度']}<br>位置: {row['位置']}<br>地震時間: {row['地震時間']}",
        }
    } for index, row in df.iterrows()
]

# 在地圖上以時間序列顯示地震事件
TimestampedGeoJson(
    {'type': 'FeatureCollection', 'features': features},
    period='PT2H',
    add_last_point=False,
    auto_play=False,
).add_to(m)

# 保存地圖
m.save('earthquakes_map.html')