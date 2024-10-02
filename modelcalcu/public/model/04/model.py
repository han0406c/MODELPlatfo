import os
import pandas as pd
import sys

# 定义湿度范围
ranges = {
    "below_10": (0, 10),
    "between_60_70": (60, 70),
    "above_70": (70, 100),
    "above_80": (80, 100)
}

# 计算湿度范围的持续时间和间隔
def calculate_durations_and_intervals(row, time_labels):
    current_intervals = {key: [] for key in ranges}
    last_value = None
    last_index = -1

    for index, value in enumerate(row):
        for range_name, (low, high) in ranges.items():
            if low <= value <= high:
                if last_value is not None and not (low <= last_value <= high):
                    # 上升到范围内
                    current_intervals[range_name].append(time_labels[index])
                last_index = index
            else:
                if last_value is not None and (low <= last_value <= high):
                    # 从范围内下降，延长一个时间标签
                    if index < len(time_labels):  # 防止索引错误
                        current_intervals[range_name].append(time_labels[index])
                    else:
                        current_intervals[range_name].append(time_labels[-1])
            last_value = value

    # 从区间计算持续时间
    durations = {}
    for key, times in current_intervals.items():
        if times:
            durations[key] = sum((pd.to_datetime(times[i+1]) - pd.to_datetime(times[i])).total_seconds() / 60 for i in range(0, len(times), 2))
        else:
            durations[key] = 0

    return pd.Series([durations[k] for k in sorted(durations)])

# 主处理函数
def process_humidity_data(input_file, output_file):
    try:
        # 读取上传的 Excel 文件
        data = pd.read_excel(input_file, header=None)

        # 转换为数字，并处理合并的单元格
        numeric_data = data.iloc[3:, 1:].apply(pd.to_numeric, errors='coerce')
        bcd_columns = data.iloc[3:, [1, 2, 3]].ffill()

        # 计算每一行的结果
        results_df = numeric_data.apply(lambda row: calculate_durations_and_intervals(row, data.iloc[1, 1:].tolist()), axis=1)
        results_df.columns = ['Below 10% (min)', '60-70% (min)', 'Above 70% (min)', 'Above 80% (min)']

        # 合并结果和原始 BCD 列
        combined_df = pd.concat([bcd_columns.reset_index(drop=True), results_df], axis=1)

        # 保存结果为新的 Excel 文件
        combined_df.to_excel(output_file, index=False)
        print(f"处理完成，结果保存为: {output_file}")

    except Exception as e:
        print(f"处理文件时出错: {e}")

def main():
    if len(sys.argv) < 3:
        print("请提供输入和输出文件路径")
        sys.exit(1)

    input_file = sys.argv[1]  # 输入文件路径
    output_file = sys.argv[2]  # 输出文件路径

    # 调用处理函数
    process_humidity_data(input_file, output_file)

if __name__ == "__main__":
    main()