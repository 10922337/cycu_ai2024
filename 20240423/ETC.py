import requests
from xml.etree import ElementTree as ET
import pandas as pd
from datetime import datetime, timedelta

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

    # 將數據添加到列表中
    data.append([location, time, speed])

# 將數據轉換為pandas DataFrame
df = pd.DataFrame(data, columns=['Location', 'Time', 'Speed'])

import pytz

# 將時間列轉換為datetime對象，並只保留最近一周的數據
df['Time'] = pd.to_datetime(df['Time'])
one_week_ago = datetime.now().replace(tzinfo=pytz.UTC) - timedelta(weeks=1)
df = df[df['Time'] > one_week_ago]

# 根據車速創建新的標籤列
df['Label'] = df['Speed'].apply(lambda x: '順暢' if int(x) > 70 else '車多')

# 顯示DataFrame
print(df)

# 移除時區信息
df['Time'] = df['Time'].dt.tz_localize(None)

# 選擇 'Location' 列開頭為 '01' 的行
df = df[df['Location'].str.startswith('01')]

# 將 DataFrame 輸出為 Excel 文件
df.to_excel("output.xlsx", index=False)