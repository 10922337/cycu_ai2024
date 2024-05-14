import pandas as pd
import plotly.express as px
import os

# 獲取當前的工作目錄
current_dir = os.getcwd()
# 讀取 csv 檔案
df = pd.read_csv(os.path.join(current_dir, "cycu_ai2024/20240507/combined特徵化.csv"))

# 創建一個新的欄位 'color'，根據 'speed' 欄位的值來設定顏色
def color(speed):
    if speed > 80:
        return 'green'
    elif 60 < speed <= 80:
        return 'yellow'
    elif 40 < speed <= 60:
        return 'orange'
    elif 20 < speed <= 40:
        return 'red'
    else:
        return 'purple'

df['color'] = df['Speed'].apply(color)

#將31.0的名稱改成小客車
df = df.rename(columns={'31.0':'小客車'})

# 創建三維圖
color_map = {'green': 'green', 'yellow': 'yellow', 'orange': 'orange', 'red': 'red', 'purple': 'purple'}

fig = px.scatter_3d(df, x='Time', y='Door', z='小客車', color='color', color_discrete_map=color_map)
fig.update_traces(marker=dict(size=2))
# fig.show()

#製作可以旋轉的圖，將圖存成.spt檔
fig.write_html(os.path.join(current_dir, "cycu_ai2024/20240507/plot.html"))