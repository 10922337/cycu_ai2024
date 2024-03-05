import requests
from bs4 import BeautifulSoup
import ssl
import pandas as pd

import matplotlib.pyplot as plt

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

urls = [
    "https://vipmbr.cpc.com.tw/mbwebs/ShowHistoryPrice_oil.aspx",
    "https://vipmbr.cpc.com.tw/mbwebs/ShowHistoryPrice_oil2019.aspx"
]

data_frames = []

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the first table on the page
    tables = soup.find_all('table')

    # Convert the table to a DataFrame
    data = pd.read_html(str(tables[1]))[0]
    data_frames.append(data)

# Combine the data frames
combined_data = pd.concat(data_frames)

#將nan值改為後一天的價格
combined_data = combined_data.fillna(method='bfill')

def convert_date(date_str):
    if '下午' in date_str:
        date_str = date_str.replace('下午', 'PM')
        return pd.to_datetime(date_str, format='%Y/%m/%d %p %I:%M:%S', errors='coerce')
    elif '上午' in date_str:
        date_str = date_str.replace('上午', 'AM')
        return pd.to_datetime(date_str, format='%Y/%m/%d %p %I:%M:%S', errors='coerce')
    else:
        return pd.to_datetime(date_str, format='%Y/%m/%d', errors='coerce')

# Convert the '調價日期' column to datetime
combined_data[combined_data.columns[0]] = combined_data[combined_data.columns[0]].apply(convert_date)

# Get the date part of the datetime
combined_data[combined_data.columns[0]] = combined_data[combined_data.columns[0]].dt.date

# Convert the '調價日期' column back to datetime (Timestamp)
combined_data[combined_data.columns[0]] = pd.to_datetime(combined_data[combined_data.columns[0]])

print(combined_data)


# Save the combined data frame to a CSV file with encoding='utf-8-sig'
combined_data.to_csv("C:/Users/USER/Desktop/oil.csv", index=False, encoding='utf-8-sig')

# 根據日期畫出所有油價走勢圖
plt.plot(combined_data[combined_data.columns[0]], combined_data[combined_data.columns[1]], label='92無鉛汽油')
plt.plot(combined_data[combined_data.columns[0]], combined_data[combined_data.columns[2]], label='95無鉛汽油')
plt.plot(combined_data[combined_data.columns[0]], combined_data[combined_data.columns[3]], label='98無鉛汽油')
plt.plot(combined_data[combined_data.columns[0]], combined_data[combined_data.columns[4]], label='超級柴油')

plt.title('油價走勢圖')
plt.xlabel('日期')
plt.ylabel('價格')
plt.xticks(rotation=45)
plt.legend(loc='upper left')
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 設定字體為微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
plt.show()

