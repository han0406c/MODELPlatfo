import sys
import pandas as pd

# 读取 Excel 文件并将内容保存到另一个 Excel 文件中
def read_and_process_excel(input_file, output_file):
    try:
        # 读取输入文件
        data = pd.read_excel(input_file)
        print("读取文件成功")
        
        # 将内容写入到输出文件
        data.to_excel(output_file, sheet_name='ProcessedData', index=False)
        print("处理并保存文件成功")
        
    except Exception as e:
        print(f"处理过程中出错: {e}")

def main():
    # 获取传递的文件路径
    input_file = sys.argv[1]  # 第一个参数为输入文件路径
    output_file = sys.argv[2]  # 第二个参数为输出文件路径

    # 处理 Excel 文件
    read_and_process_excel(input_file, output_file)

if __name__ == "__main__":
    main()