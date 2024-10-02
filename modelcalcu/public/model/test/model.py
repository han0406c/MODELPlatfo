import pandas as pd

# Load the Excel file
file_path ='/Users/vincentchen/Desktop/Jupyter Code/温度序列统计/冷通道湿度.xlsx'
data = pd.read_excel(file_path, header=None)

# Define humidity ranges
ranges = {
    "below_10": (0, 10),
    "between_60_70": (60, 70),
    "above_70": (70, 100),
    "above_80": (80, 100)
}

# Convert data to numeric and handle merged cells
numeric_data = data.iloc[3:, 1:].apply(pd.to_numeric, errors='coerce')
bcd_columns = data.iloc[3:, [1, 2, 3]].ffill()

# Function to calculate durations and intervals
def calculate_durations_and_intervals(row, time_labels):
    current_intervals = {key: [] for key in ranges}
    last_value = None
    last_index = -1

    for index, value in enumerate(row):
        for range_name, (low, high) in ranges.items():
            if low <= value <= high:
                if last_value is not None and not (low <= last_value <= high):
                    # Rising into the range
                    current_intervals[range_name].append(time_labels[index])
                last_index = index
            else:
                if last_value is not None and (low <= last_value <= high):
                    # Falling out of the range, extend by one time label (5 minutes)
                    if index < len(time_labels):  # Check to avoid index error
                        current_intervals[range_name].append(time_labels[index])
                    else:
                        current_intervals[range_name].append(time_labels[-1])
            last_value = value

    # Calculate durations from intervals
    durations = {}
    for key, times in current_intervals.items():
        if times:
            durations[key] = sum((pd.to_datetime(times[i+1]) - pd.to_datetime(times[i])).total_seconds() / 60 for i in range(0, len(times), 2))
        else:
            durations[key] = 0

    return pd.Series([durations[k] for k in sorted(durations)])

# Calculate results for each row
results_df = numeric_data.apply(lambda row: calculate_durations_and_intervals(row, data.iloc[1, 1:].tolist()), axis=1)
results_df.columns = ['Below 10% (min)', '60-70% (min)', 'Above 70% (min)', 'Above 80% (min)']

# Combine BCD columns with results
combined_df = pd.concat([bcd_columns.reset_index(drop=True), results_df], axis=1)

# Save to Excel
output_file_path = '/Users/vincentchen/Desktop/Jupyter Code/温度序列统计/冷通道湿度处理_final1.xlsx'
combined_df.to_excel(output_file_path, index=False)

print("File saved successfully to", output_file_path)