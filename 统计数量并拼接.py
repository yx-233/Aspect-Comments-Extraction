# -*- coding: utf-8 -*-
"""
@Time ： 2023/9/3 22:54
@Auth ： Philo
@File ：统计数量并拼接.py
@IDE ：PyCharm
"""
import os
import pandas as pd
import glob
from tqdm import tqdm

# 获取目录下所有xlsx文件的数量
dir_path = r'C:\Users\18079\Desktop\workspace\爬虫\json_data\result'
all_xlsx_files = 0
for root, dirs, files in os.walk(dir_path):
    for file in files:
        if file.endswith('.xlsx'):
            all_xlsx_files += 1
print(f'总共有 {all_xlsx_files} 个xlsx文件')

folder_path = r'C:\Users\18079\Desktop\workspace\爬虫\json_data\result'
provinces = [folder for folder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, folder))]
# 创建一个空列表，用于存储所有的数据框
all_dataframes = []
# 遍历省份的列表，使用tqdm包装器显示进度条
for province in tqdm(provinces):
    try:
        # 创建一个空列表，用于存储每个省份的数据框
        province_dataframes = []
        # 获取省份路径，将省份名称添加到文件夹路径中
        province_path = os.path.join(folder_path, province)
        # 获取省份路径下的所有文件名（这里是图书馆的Excel文件）
        library_name = os.listdir(province_path)
        # 遍历每个图书馆文件
        for library in library_name:
            try:
                # 获取图书馆文件的完整路径
                library_path = os.path.join(province_path, library)
                # 读取Excel文件并将其存储为数据框
                df = pd.read_excel(library_path)
                # 在数据框中添加一个名为"名称"的列，其值为文件名（去掉.xlsx后缀）
                df["图书馆名称"] = library.split(".")[-2]
                # 将数据框添加到省份数据框列表中
                province_dataframes.append(df)
                # 将同一省份的所有数据框合并为一个数据框
            except:
                print(f"{library}文件出错")
        province_review = pd.concat(province_dataframes)
        # 在合并后的数据框中添加一个名为"省份"的列，其值为当前省份的名称
        province_review["省份"] = province
        # 将合并后的数据框添加到所有数据框列表中
        all_dataframes.append(province_review)
    except:
        print(f"{province}文件夹出错")

# 将所有数据框合并为一个数据框，存储到all_data变量中
all_data = pd.concat(all_dataframes)
all_data = all_data.drop_duplicates()

print(f"文件长度为：{len(all_data)}")
all_data.to_excel("data/sorce/一级公共图书馆.xlsx",index=False)
# 对"图书馆名称"列进行value_counts，然后将其转换为DataFrame
df = all_data['图书馆名称'].value_counts().reset_index()
df.columns = ['图书馆名称', '评论数量']  # 重命名列名
df.to_excel("data/sorce/各图书馆评论数量统计.xlsx",index=False)


# 打印图书馆统计数据框的前几行以检查数据
# print(df)