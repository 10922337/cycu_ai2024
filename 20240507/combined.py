import pandas as pd
import os

# 獲取當前的工作目錄
current_dir = os.getcwd()

# 讀取檔案
df = pd.read_csv(os.path.join(current_dir, "cycu_ai2024/20240507/03A特徵化.csv"))

df2 = pd.read_csv(os.path.join(current_dir, "cycu_ai2024/20240507/05A特徵化.csv"))

# 使用 'Time' 和 'Door' 欄位合併兩個 DataFrame
combined_df = pd.merge(df, df2[['Time', 'Door', 'Speed']], on=['Time', 'Door'], how='left')

# 儲存結果到新的 csv 檔案
combined_df.to_csv(os.path.join(current_dir, "cycu_ai2024/20240507/combined.csv"), index=False)