import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import os

# 獲取當前的工作目錄
current_dir = os.getcwd()

# 讀取檔案
df3 = pd.read_csv(os.path.join(current_dir, "cycu_ai2024/20240514/M03A_Temp.csv"), encoding='big5')

# 對時間和里程數據進行網格化
# 假設 x (時間) 和 y (里程) 已經是規則的網格數據
x = np.linspace(df3['Time'].min(), df3['Time'].max(), num=1000) # 調整 num 以匹配數據點的密度
y = np.linspace(df3['Door'].min(), df3['Door'].max(), num=1000)
x, y = np.meshgrid(x, y)

# 插值找到每個 (x, y) 點對應的 z (車流量)
z = griddata((df3['Time'], df3['Door']), df3['小客車'], (x, y), method='linear')
speed = griddata((df3['Time'], df3['Door']), df3['Speed'], (x, y), method='linear')

# 創建一個自定義的顏色映射
cmap = mcolors.ListedColormap(['purple', 'yellow', 'orange', 'yellow', 'green'])
norm = mcolors.BoundaryNorm([0, 20, 40, 60, 80, np.inf], cmap.N)

# 創建一個 ScalarMappable 對象
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])

fig = plt.figure(figsize=(10, 10))
ax1 = fig.add_subplot( projection='3d')
# 繪製曲面圖
surf = ax1.plot_surface(x, y, z, facecolors=sm.to_rgba(speed))

# 設置坐標軸標籤
ax1.set_xlabel('Time')
ax1.set_ylabel('Door')
ax1.set_zlabel('Traffic Flow')

plt.suptitle('cubicspline_3D')
plt.tight_layout()
plt.savefig(os.path.join(current_dir, "cycu_ai2024/20240514/20240514_3D.png"))
plt.show()