# -*- coding: utf-8 -*-
import pandas as pd
import xlrd
import xlwt

def excel_to_csv(in_finename, out_filename):
    """
    excel转换成csv格式
    :return:
    """
    df = pd.read_excel(in_finename, index_col=0)
    df.to_csv(out_filename, encoding='utf_8_sig')  # encoding='utf_8_sig' 转换成中文编码


filename = f"E:/GMWork/01 Project/corpus/storage_data/result.xlsx"
df = pd.read_excel(filename)
df.to_csv(f"E:/GMWork/01 Project/corpus/storage_data/result.csv")
filename = f"E:/GMWork/01 Project/corpus/storage_data/result.xlsx"
def pd_merge_excel_sheet(sheet_name):
    write = pd.ExcelWriter(filename)
    df.to_excel(write, sheet_name=sheet_name)
    write.save()

# myExcel = xlwt.Workbook()
# def savefile(filepath, tags, name):
#   sheet1 = myExcel.add_sheet(name, cell_overwrite_ok=True)
#   for i in range(0, len(tags)):
#     sheet1.write(i, 0, tags[i])
#   myExcel.save(filepath)


myExcel = xlwt.Workbook()
def savefile():
    sheet_name = ['拔罐', '点穴', '丰胸', '刮痧', '火疗', '疾病方药', '减肥', '美容', '捏背',
                  '偏方妙方', '气功', '祛湿', '推拿', '药酒', '用药禁忌', '针灸', '足疗']
    sheet1 = myExcel.add_sheet(sheet_name, cell_overwrite_ok=True)
    for i in range(0, len(sheet_name)):
        df.to_csv(filename, sheet_name=i)
        # sheet1.write(i, 0, sheet_name[i])
    # myExcel.save(filename)


if __name__ == "__main__":
    # excel_to_csv()
    savefile()
    # pd_merge_excel_sheet()
    # with open('E:/GMWork/01 Project/corpus/storage_data/test.txt', 'r') as f:
    #     print(f)
    # savefile()
    # sheet_name = ['拔罐', '点穴']
    # for i in sheet_name:
    #     pd_merge_excel_sheet(i)
    #     print(i)
    # pd_merge_excel_sheet()

# dfs = []
# for fn in (filename + '/拔罐.xls', filename + '/点穴.xls'):
#     dfs.append(pd.read_excel(fn))
# df = pd.concat(dfs)
# df.to_excel(filename + '/result.xlsx', index=False)


