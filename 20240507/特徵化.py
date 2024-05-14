#讀取檔案
import pandas as pd
import os

# 獲取當前的工作目錄
current_dir = os.getcwd()

# 讀取檔案
df = pd.read_csv(os.path.join(current_dir, "cycu_ai2024/20240507/03A.csv"))

#將第二欄中前兩個字為01的數據篩選出來，並將資料轉換成第四個字到第七個字
df = df[df['Door'].str[:2] == '01']
df['Door'] = df['Door'].str[3:8]

#篩選出Time Door Direction 皆相同的橫列合併，新增欄位31.0,32.0,41.0,42.0,5.0，將相同Time Door Direction的Number放入欄位
df = df.groupby(['Time', 'Door', 'Direction']).agg({'Car': 'first', 'Number': list}).reset_index()
df['31.0'] = df['Number'].apply(lambda x: x[0] if len(x) > 0 else 0)
df['32.0'] = df['Number'].apply(lambda x: x[1] if len(x) > 1 else 0)
df['41.0'] = df['Number'].apply(lambda x: x[2] if len(x) > 2 else 0)
df['42.0'] = df['Number'].apply(lambda x: x[3] if len(x) > 3 else 0)
df['5.0'] = df['Number'].apply(lambda x: x[4] if len(x) > 4 else 0)
df = df.drop(columns=['Number'])

#儲存檔案
df.to_csv(os.path.join(current_dir, "cycu_ai2024/20240507/03A特徵化.csv"), index=False)

print(df)

#------------------------------------------------------------

# 讀取檔案
df2 = pd.read_csv(os.path.join(current_dir, "cycu_ai2024/20240507/05A.csv"))

#將第二欄中前兩個字為01的數據篩選出來，並將資料轉換成第四個字到第七個字
df2 = df2[df2['Door'].str[:2] == '01']
df2['Door'] = df2['Door'].str[3:8]

#篩選欄位Car為31的數據
df2 = df2[df2['Car'] == 31]

#輸出Time Door Car Speed
df2 = df2[['Time', 'Door', 'Car', 'Speed']]
df2.to_csv(os.path.join(current_dir, "cycu_ai2024/20240507/05A特徵化.csv"), index=False)

#------------------------------------------------------------

# 讀取 csv 檔案
df3 = pd.read_csv(os.path.join(current_dir, "cycu_ai2024/20240507/timeyet.csv"))

#分別讀取colome:Time中的前兩個字和後兩個字，分別把它們轉換成int，前兩個字*60/5+後兩個字/5
df3['Time'] = df3['Time'].str[:2].astype(int) * 60 / 5 + df3['Time'].str[3:].astype(int) / 5

#儲存檔案，命名為time特徵化.csv
df3.to_csv(os.path.join(current_dir, "cycu_ai2024/20240507/timeyet特徵化.csv"), index=False)