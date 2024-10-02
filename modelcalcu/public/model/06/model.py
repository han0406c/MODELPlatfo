import sys
import pandas as pd
import os

def read_and_process_file(input_file, output_file):
    try:
        # 读取 Excel 文件
        data = pd.read_excel(input_file)
        print("文件读取成功:", input_file)
        
        # 假设 Excel 文件有一列 'Numbers'，我们计算每个数的平方
        data['Square'] = data['Numbers'] ** 2
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 将结果保存为新的 Excel 文件
        data.to_excel(output_file, index=False)
        print(f"处理完成，结果保存为: {output_file}")
        
    except Exception as e:
        print(f"处理文件时出错: {e}")

def main():
    if len(sys.argv) != 3:
        print("用法: python model.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    read_and_process_file(input_file, output_file)

if __name__ == "__main__":
    main()