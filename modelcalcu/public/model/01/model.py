# import xlrd
# import xlwt
import sys
import pandas as pd
from pandas import DataFrame




# def readxlsx(filename):


#     data = xlrd.open_workbook(filename)

#     table = data.sheets()[0]             #通过索引顺序获取
#     # table = data.sheet_by_index(sheet_indx)  #通过索引顺序获取
#     # table = data.sheet_by_name(sheet_name)  #通过名称获取
    
#     # 以上三个函数都会返回一个xlrd.sheet.Sheet()对象
    
#     # names = data.sheet_names()        #返回book中所有工作表的名字
#     # data.sheet_loaded(sheet_name or indx)    # 检查某个sheet是否导入完毕

#     nrows = table.nrows
#         # 获取该sheet中的行数，注，这里table.nrows后面不带().
#     print(nrows)
#     print(table.row_values(0))

#     list1 = table.row_values(0)

#     return list1 

# def writenew(data):
#     # 创建新的workbook（其实就是创建新的excel）
#     workbook = xlwt.Workbook(encoding= 'uft-8')
 
#     # 创建新的sheet表
#     worksheet = workbook.add_sheet("My new Sheet")
#      # 往表格写入内容
#     worksheet.write(0,0, data)

 
#     # 保存
#     workbook.save("./public/output/newtest.xlsx")


def readxlsx(filename):
    data = pd.read_excel(filename)
    print(data)
    # print(data.loc[1])

    DataFrame(data).to_excel('./public/data/output/result.xlsx', sheet_name='Sheet1', index=False, header=True)


def main():

    # filename = "./public/upload/test.xlsx"
    filename = sys.argv[1]
    towrite = readxlsx(filename)
    # writenew(towrite)
    result ="okay"
    return result

main()