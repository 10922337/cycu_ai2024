import pandas as pd
import os

# 獲取當前的工作目錄
current_dir = os.getcwd()
# 讀取檔案
df3 = pd.read_csv(os.path.join(current_dir, "cycu_ai2024/20240514/combined特徵化.csv"), encoding='big5')

# 只保留 Car column 為 31 的資料
df3 = df3[df3['Car'] == 31]

# Door column 只保留第四個到第七個字元
df3['Door'] = df3['Door'].str[0:3]

# Direction column 只保留資料為 S
df3 = df3[df3['Direction'] == 'S']

# 將 Door column 轉換為 int
df3['Door'] = df3['Door'].astype(int)

# 將 column Door 做遞增的排序
df3 = df3.sort_values(by='Door')

# 將 "Speed" 欄位的值設為對應的 "Car" 欄位等於 '31' 的行的 "Speed" 欄位的值
df3['Speed'] = df3[df3['Car'] == 31]['Speed']

#將 "Time" 欄位的值設為對應的 "Car" 欄位等於 '31' 的行的 "Time" 欄位的值
df3['Time'] = df3[df3['Car'] == 31]['Time']

# 將 "31" 欄位的值轉換為數字
df3["小客車"] = pd.to_numeric(df3["小客車"])

# 儲存結果到新的 csv 文件
df3.to_csv(os.path.join(current_dir, "cycu_ai2024/20240514/M03A_Temp.csv"), index=False, encoding='big5')