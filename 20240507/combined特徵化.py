import pandas as pd
import os

# 獲取當前的工作目錄
current_dir = os.getcwd()

# 讀取 csv 檔案
df3 = pd.read_csv(os.path.join(current_dir, "cycu_ai2024/20240507/combined.csv"))

#分別讀取colome:Time中的前兩個字和後兩個字，分別把它們轉換成int，前兩個字*60/5+後兩個字/5
df3['Time'] = df3['Time'].str[:2].astype(int) * 60 / 5 + df3['Time'].str[3:].astype(int) / 5

#儲存檔案，命名為combined特徵化.csv
df3.to_csv(os.path.join(current_dir, "cycu_ai2024/20240507/combined特徵化.csv"), index=False)