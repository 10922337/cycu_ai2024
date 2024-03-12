import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# File path
file_path = r'C:/Users/User/Desktop/cycu_ai2024/20240312/112年1-10月交通事故簡訊通報資料.csv'

# Read the CSV file and create a DataFrame
df = pd.read_csv(file_path, low_memory=False)

# Drop rows where '國道名稱' is missing, whitespace or '#VALUE!'
df = df[df['國道名稱'].str.strip().astype(bool) & (df['國道名稱'] != '#VALUE!')]

# Convert '里程' to numeric type and set invalid values to NaN
df['里程'] = pd.to_numeric(df['里程'], errors='coerce')

# Drop rows where '里程' is greater than 1000
df = df[df['里程'] <= 1000]

# Drop rows where '里程' is NaN
df = df.dropna(subset=['里程'])

# Drop rows where '里程' is NaN
df = df.dropna(subset=['里程'])

# Group by highway name
grouped = df.groupby('國道名稱')

# Create an empty DataFrame for the result
result = pd.DataFrame()

# Iterate over each highway group
for name, group in grouped:
    # Sort by mileage
    sorted_group = group.sort_values('里程')
    
    # Iterate over each item in the sorted group
    for index, row in sorted_group.iterrows():
        # Get highway name, mileage, direction, and accident type
        highway_name = row['國道名稱']
        mileage = row['里程']
        direction = row['方向']
        accident_type = row['事故類型']
        
        # Add data to the result DataFrame
        new_row = pd.DataFrame({'國道名稱': [highway_name], '里程': [mileage], '方向': [direction], '事故類型': [accident_type]})
        new_row = new_row.dropna(how='all')  # Drop rows where all items are missing
        result = pd.concat([result, new_row], ignore_index=True)

# Count the occurrence of each highway name
df = df.dropna(subset=['國道名稱'])
count = df['國道名稱'].value_counts()

# Output as Excel file
output_path = r'C:/Users/User/Desktop/cycu_ai2024/20240312/result.xlsx'
with pd.ExcelWriter(output_path) as writer:
    result.to_excel(writer, sheet_name='Result', index=False)
    count.to_excel(writer, sheet_name='Count')




font = FontProperties(fname=r"c:/windows/fonts/simsun.ttc", size=14)  # This is for SimSun font. Replace with the path to your font file.

# Group by highway name and mileage
grouped = df.groupby(['國道名稱', '里程'])

# Count the occurrence of each group
count = grouped.size().reset_index(name='次數')

# Create a new figure
plt.figure()

# Iterate over each highway name
for name in count['國道名稱'].unique():
    # Get the data for this highway
    data = count[count['國道名稱'] == name]
    
    # Plot the data
    plt.plot(data['里程'], data['次數'], label=name)

# Add a legend with Chinese font
plt.legend(prop=font)

# Show the plot
plt.show()
