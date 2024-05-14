import requests
from xml.etree import ElementTree as ET
import pandas as pd
from datetime import datetime, timedelta
import pytz

# 獲取XML數據
response = requests.get("https://tisvcloud.freeway.gov.tw/history/motc20/ETagPairLive.xml")

# 解析XML數據
root = ET.fromstring(response.content)

# 初始化列表來存儲數據
data = []

# 從XML數據中提取所需的信息
for child in root.iter('{http://traffic.transportdata.tw/standard/traffic/schema/}ETagPairLive'):
    location = child.find('{http://traffic.transportdata.tw/standard/traffic/schema/}ETagPairID').text
    time = child.find('{http://traffic.transportdata.tw/standard/traffic/schema/}DataCollectTime').text
    for flow in child.iter('{http://traffic.transportdata.tw/standard/traffic/schema/}Flow'):
        speed = flow.find('{http://traffic.transportdata.tw/standard/traffic/schema/}SpaceMeanSpeed').text
        vehicle_type = flow.find('{http://traffic.transportdata.tw/standard/traffic/schema/}VehicleType').text

    # 將數據添加到列表中
    data.append([location, time, speed, vehicle_type])

# 將數據轉換為pandas DataFrame
df = pd.DataFrame(data, columns=['Location', 'Time', 'Speed', 'VehicleType'])

# 將時間列轉換為datetime對象，並只選擇特定日期範圍的數據
df['Time'] = pd.to_datetime(df['Time'])
start_date = pd.Timestamp('2024-04-29 00:00:00+08:00')
end_date = pd.Timestamp('2024-04-29 23:59:59+08:00')
df = df[df['Time'].between(start_date, end_date)]

# 選擇特定位置的數據
df = df[df['Location'].isin(['M03A', 'M04A'])]

# 計算每種車型在每個位置的平均速度，最大速度和最小速度
df['Speed'] = df['Speed'].astype(int)
df_features = df.groupby(['Location', 'VehicleType'])['Speed'].agg(['mean', 'max', 'min']).reset_index()

# 顯示特徵化後的DataFrame
print(df_features)

# 將 DataFrame 輸出為 Excel 文件
if not df_features.empty:
    df_features.to_excel("output_features.xlsx", index=False)
else:
    print("No data to write to Excel.")