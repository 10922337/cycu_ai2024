import pandas as pd

import os

# 獲取當前的工作目錄
current_dir = os.getcwd()

# 讀取檔案
df = pd.read_csv(os.path.join(current_dir, "cycu_ai2024/20240514/M03A.csv"), encoding='big5')

# 將第1,2,3個列分組，並將第五個列的值相加
df['T_flow'] = df.groupby(['Time', 'Door', 'Direction'])['Number'].transform('sum')

#只保留Car colomn為31的資料
df = df[df['Car'] == 31]

#Door colomn只保留第四個到第七個字元
df['Door'] = df['Door'].str[4:7]

#Direction colomn只保留資料為S
df = df[df['Direction'] == 'S']

#將Door colomn轉換為int
df['Door'] = df['Door'].astype(int)

#將colomn Door做遞增的排序
df = df.sort_values(by='Door')

# 將 "Number" 欄位的值設為對應的 "Car" 欄位等於 '31' 的行的 "Number" 欄位的值
df['Number'] = df[df['Car'] == 31]['Number']

# 儲存結果到新的 csv 文件
df.to_csv(os.path.join(current_dir, "cycu_ai2024/20240514/M03A_New.csv"), index=False)

#------------------------------------------------------------

import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import numpy as np

# 讀取 csv 文件
df2 = pd.read_csv(os.path.join(current_dir, "cycu_ai2024/20240514/M03A_New.csv"))

# 刪除重複的行
df2 = df2.drop_duplicates(subset='Door')

# 對 'Door' 列進行排序
df2 = df2.sort_values('Door')

# 創建 cubic spline 插值函數
cs = CubicSpline(df2['Door'], df2['T_flow'])

# 創建 x 軸的值
xnew = np.linspace(df2['Door'].min(), df2['Door'].max(), 500)

# 繪製圖形
plt.plot(xnew, cs(xnew))
plt.scatter(df2['Door'], df2['T_flow'], color='red')  # 原始數據點
plt.xlabel('Door')
plt.ylabel('T_flow')
plt.title('Cubic Spline Interpolation')

# 儲存圖片到/workspaces/cycu_ai2024/20240514
plt.savefig(os.path.join(current_dir, "cycu_ai2024/20240514/20240514_2D.png"))
