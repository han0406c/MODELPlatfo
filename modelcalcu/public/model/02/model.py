import os
import pandas as pd
import sys

def readxlsx(filename):
    try:
        # 读取上传的 Excel 文件
        data = pd.read_excel(filename)
        if data.empty:
            print("文件为空或格式不正确")
            return pd.DataFrame()  # 返回空数据框
        else:
            print("读取文件成功")
            return data
    except Exception as e:
        print(f"读取文件失败: {e}")
        return pd.DataFrame()

def main():
    if len(sys.argv) < 3:
        print("请提供输入文件路径和输出文件路径")
        sys.exit(1)

    input_file = sys.argv[1]  # 第一个参数是输入文件路径
    output_file = sys.argv[2]  # 第二个参数是输出文件路径

    data = readxlsx(input_file)

    # 添加一列新数据作为处理后的结果
    if not data.empty:
        data['Processed'] = 'Yes'

        # 确保输出目录存在
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 保存结果为 Excel 文件
        data.to_excel(output_file, sheet_name='ProcessedData', index=False)
        print(f"处理完成，结果保存为: {output_file}")
    else:
        print("没有数据进行处理")

if __name__ == '__main__':
    main()