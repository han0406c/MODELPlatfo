import sys
import pandas as pd
import os

# 读取 Excel 文件并计算年薪
def process_salary(input_file, output_file):
    try:
        # 检查文件是否存在
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"输入文件 {input_file} 不存在")
        
        # 检查文件类型是否为 Excel
        if not input_file.endswith(('.xlsx', '.xls')):
            raise ValueError(f"输入文件 {input_file} 不是 Excel 文件")
        
        # 读取输入文件
        data = pd.read_excel(input_file)
        print("读取文件成功")

        # 确保 'Salary' 列存在
        if 'Salary' not in data.columns:
            raise KeyError("输入文件中缺少 'Salary' 列")
        
        # 计算年薪 (假设年薪为月薪乘以 12)
        data['Annual Salary'] = data['Salary'] * 12

        # 将数据写入新的 Excel 文件
        data.to_excel(output_file, index=False)
        print(f"处理成功，结果保存至: {output_file}")
        
    except FileNotFoundError as fnf_error:
        print(f"文件未找到: {fnf_error}")
    except KeyError as key_error:
        print(f"数据处理出错: {key_error}")
    except Exception as e:
        print(f"处理过程中出错: {e}")

def main():
    # 获取传递的文件路径
    input_file = sys.argv[1]  # 输入文件路径
    output_file = sys.argv[2]  # 输出文件路径

    # 处理数据
    process_salary(input_file, output_file)

if __name__ == "__main__":
    main()